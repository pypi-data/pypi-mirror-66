#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Aaron-Yang [code@jieyu.ai]
Contributors:

"""
import json
import logging
import pickle
import uuid
from typing import Any

from pyemit.emit import rpc_send, rpc_respond

logger = logging.getLogger(__name__)


class Remote(object):
    def __init__(self):
        self._sn_ = uuid.uuid4().hex
        self._ver_ = '0.1'

    def __str__(self):
        def default(obj):
            return obj.__str__()

        return json.dumps(self.__dict__, default=default, indent=2)

    def __repr__(self):
        return f"{self.__class__} 0x{id(self):0x}\n{self.__str__()}"

    def serialize(self):
        """
        pickle_protocol 4 support from python 3.4
        """
        return pickle.dumps(self, protocol=4)

    @staticmethod
    def loads(s) -> 'Remote':
        return pickle.loads(s)

    async def __call__(self):
        return await rpc_send(self)

    async def server_impl(self):
        raise NotImplementedError

    async def respond(self, result: Any):
        response = {
            '_sn_':   self._sn_,
            '_data_': pickle.dumps(result, protocol=4)
        }

        await rpc_respond(response)
