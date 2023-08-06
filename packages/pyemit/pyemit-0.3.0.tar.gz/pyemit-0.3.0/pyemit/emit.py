import asyncio
import logging
import pickle
import time
import uuid
from enum import IntEnum
from typing import Callable, Any

logger = logging.getLogger(__name__)


class Engine(IntEnum):
    IN_PROCESS = 0
    REDIS = 1


# for aio-redis mq only
_pub_conn = None
_sub_conn = None

# msg => {"queue": aioredis.Channel, "handlers": handlers}
_registry = {}
_heart_beat = 0
_started = False
_engine = Engine.IN_PROCESS
__rpc_calls__ = {}
_rpc_client_channel = '__emit_rpc_client_channel__'
_rpc_server_channel = '__emit_rpc_server_channel__'


def on(event):
    """
    提供了消息注册的装饰器实现
    Args:
        event:
    Returns:

    """

    def decorator(func):
        register(event, func)

    return decorator


def register(event: str, handler: Callable):
    """
    :param event:
    :param handler:
    :return:
    """
    global _registry

    item = _registry.get(event, {"handlers": set()})
    item['handlers'].add(handler)
    _registry[event] = item

    if _started:
        # in this case, we need manually bind msg, handler with a queue/channel
        asyncio.create_task(_bind(event))


async def _bind(event: str):
    global _registry, _engine, _sub_conn, _pub_conn

    item = _registry.get(event)
    if _engine == Engine.IN_PROCESS:
        if item.get('queue') is None:
            queue = asyncio.Queue()
            await queue.join()
            logger.info("msg %s is bound to local queue %s", event, queue)
            item['queue'] = queue
        else:
            logger.info("msg %s is already bound to local queue, skipped", event)
    else:
        if item.get('queue') is None:
            response = await _sub_conn.subscribe(event)
            if response:
                item['queue'] = response[0]
                logger.info("msg %s is bound to remote queue %s", event, response[0])
            else:
                logger.warning("failed to bind msg %s to remote queue", event)
        else:
            logger.info("msg %s is already bound to remote queue, skipped", event)

    asyncio.create_task(_listen(event))


async def _listen(event: str):
    global _registry, _engine
    logger.info("listening on msg %s", event)

    async def get_and_invoke(name, message: dict):
        # handlers may add later, so we put call in the loop
        handlers = _registry.get(name, {}).get("handlers", [])
        if not handlers:
            logger.debug("discarded msg due to no handlers attached: %s", message)

        for func in handlers:
            await func(message)

    queue = _registry.get(event, {}).get('queue')
    if queue is None:
        logger.warning("failed to found queue to listen for msg %s", event)
        return

    if _engine == Engine.IN_PROCESS:
        while True:
            msg = await queue.get()
            try:
                msg = pickle.loads(msg)
                await get_and_invoke(event, msg)
            except Exception as e:
                logger.warning("msg %s caused exception", msg)
                logger.exception(e)
            finally:
                queue.task_done()
    else:
        while await queue.wait_message():
            try:
                msg = await queue.get()
            except Exception as e:
                logger.warning("connection error?")
                # todo: try reconnect?
                continue
            try:
                msg = pickle.loads(msg)
                await get_and_invoke(event, msg)
            except Exception as e:
                logger.warning("msg %s caused exception", msg)
                logger.exception(e)


async def _client_handle_rpc_call(msg: dict):
    sn = msg.get("_sn_")
    if sn is None:
        logger.warning("rpc call msg must contains _sn_ key: %s", msg)
        return

    waited = __rpc_calls__.get(sn)
    if waited is not None:
        msg.pop('_sn_')
        waited['result'] = msg
        waited['event'].set()
    else:
        logger.warning("emit received unsolicited message: %s", msg)


async def start(engine: Engine = Engine.IN_PROCESS, heart_beat=0, **kwargs):
    """

    :param engine: one of IN_PROCESS or AIO_REDIS
    :param heart_beat: if engine is AIO_REDIS, and heart_beat > 0, then emit will send heartbeat automatically
    :param kwargs:
    :return:

    Args:
        heart_beat:
    """
    global _started, _pub_conn, _sub_conn, _registry, _heart_beat, _engine, _rpc_client_channel
    if _started:
        logger.info("emit is already started.")
        return

    logger.info("starting emit")

    _engine = engine
    _heart_beat = heart_beat

    register(_rpc_client_channel, _client_handle_rpc_call)
    register(_rpc_server_channel, _server_rpc_handler)

    if _engine == Engine.REDIS:
        dsn = kwargs.get("dsn")
        if not dsn:
            raise SyntaxError("when in aio-redis mode, dsn is required")

        import aioredis
        _pub_conn = await aioredis.create_redis(dsn)
        _sub_conn = await aioredis.create_redis(dsn)

        if _heart_beat > 0:
            register('heartbeat', _on_heart_beat)
    # bind registered channels
    for channel in _registry.keys():
        await _bind(channel)

    if _heart_beat > 0 and engine == Engine.REDIS:
        await emit("heartbeat", {"msg": 'heartbeat', "time": time.time()})

    _started = True


async def emit(channel: str, message: Any = None):
    """
    publish a message to channel.
    :param channel: the name of channel
    :param message:
    :return:
    """
    global _registry, _engine, _pub_conn

    message = pickle.dumps(message, protocol=4)
    if _engine == Engine.IN_PROCESS:
        queue = _registry.get(channel, {}).get("queue", None)
        if queue is None:
            logger.warning(f"channel {channel} has no listener registered, skipped.")
            return
        queue.put_nowait(message)
    elif _engine == Engine.REDIS:
        await _pub_conn.publish(f"{channel}", message)


async def rpc_send(remote: Any):
    """
    emit msg and wait response back. The func will add __emit_sn__ to the dict, and the server should echo the serial
    number
    back.
    Args:
        msg:

    Returns:

    """
    global __rpc_calls__
    sn = remote._sn_

    event = asyncio.Event()

    __rpc_calls__[sn] = {
        "event":  event,
        "result": None
    }

    await emit(_rpc_server_channel, pickle.dumps(remote, protocol=4))
    await event.wait()
    response = __rpc_calls__.get(sn, {}).get("result")
    return pickle.loads(response.get('_data_'))


async def rpc_respond(msg: dict):
    global __rpc_calls__
    await emit(_rpc_client_channel, msg)


async def _server_rpc_handler(obj: bytes):
    remote = pickle.loads(obj)
    await remote.server_impl()


def unsubscribe(channel: str, handler: Callable):
    """
    stop subscribe message from channel
    :param channel:
    :param handler:
    :return:
    """
    global _registry, _engine

    if channel not in _registry.keys():
        logger.warning("%s is not registered", channel)
        return

    handlers: set = _registry.get(channel, {}).get("handlers", set())
    try:
        handlers.remove(handler)
    except KeyError:
        logger.warning("%s is not registered as handler of %s", handler.__name__, channel)

    _registry[channel]["handlers"] = handlers


async def _on_heart_beat(msg):
    """
    :param msg:
    :return:
    """
    logger.debug("mq received heart beat: %s", msg)
    await asyncio.sleep(_heart_beat)
    await emit("heartbeat", {"msg": 'heartbeat', "time": time.time()})


async def stop():
    global _started, _engine, _registry
    logger.info("stopping emit...")
    try:
        _started = False
        for binding in _registry.values():
            binding['queue'] = None

        if _engine == Engine.REDIS:
            _sub_conn.close()
            await _sub_conn.wait_closed()
    except Exception as e:
        logger.exception(e)

    logger.info("emit stopped.")
