import logging
from functools import partial
from typing import Mapping
from urllib.parse import urljoin

import aiohttp
from aiohttp import ClientSession, WSMsgType

from .base_http_client import BaseApiRequest, BaseHttpApi as HttpApi

logger = logging.getLogger()

__all__ = ('get', 'post', 'patch', 'delete', 'ws', 'HttpApi', 'ApiRequest', 'WSRequest')


class ApiRequest(BaseApiRequest):

    async def __call__(self, **kwargs):
        return await self.request(**kwargs)

    async def request(self, **kwargs) -> Mapping:
        if not self.method:
            raise NotImplementedError('Not known method')
        if not self.session:
            self.session = ClientSession(raise_for_status=True)

        request_options = self.get_request_options(**kwargs)
        async with self.session.request(**request_options.get_options()) as resp:
            return await resp.json()


class WSRequest(BaseApiRequest):

    async def __call__(self, **kwargs):
        self.path_params = self.get_path_params(self.path_template, **kwargs)
        path = self.format_path(self.path_template, self.path_params)
        url = urljoin(self.base_url, path)
        async with self.session.ws_connect(url) as ws:
            while True:
                msg = await ws.receive()
                if msg.type == aiohttp.WSMsgType.TEXT:
                    if msg.data == 'close cmd':
                        await ws.close()
                        break
                    else:
                        yield msg.json()
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break


get = partial(ApiRequest, method='GET')
post = partial(ApiRequest, method='POST')
delete = partial(ApiRequest, method='DELETE')
patch = partial(ApiRequest, method='PATCH')
ws = WSRequest
