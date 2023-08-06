import logging
from functools import partial
from urllib.parse import urljoin

import aiohttp
from aiohttp import ClientSession

from .base_http_client import BaseApiRequest, BaseHttpApi as HttpApi

logger = logging.getLogger()

__all__ = ('get', 'post', 'patch', 'delete', 'ws', 'HttpApi', 'ApiRequest', 'WSRequest')


class ApiRequest(BaseApiRequest):

    async def __call__(self, **kwargs):
        if not self.method:
            raise NotImplementedError('Not known method')
        if not self.session:
            self.session = ClientSession(raise_for_status=True)
        req_opt = self.get_request_options(**kwargs)

        logger.debug('Make request to %s\nParams:\n\tmethod: %s\n\tbody: %s\n\theaders: %s',
                     req_opt.url, req_opt.method, req_opt.json, req_opt.headers)

        async with self.session.request(**req_opt.get_options()) as resp:
            try:
                res = await resp.json()
                logger.debug('Received data: %s', res)
                return res
            except Exception as e:
                logger.error('Error with request to to %s\nParams:\n\tmethod: %s\n\tbody: %s\n\theaders: %s\n\tErr: %s',
                             req_opt.url, req_opt.method, req_opt.json, req_opt.headers, e)
                raise


class WSRequest(BaseApiRequest):

    async def __call__(self, **kwargs):
        self.path_params = self.get_path_params(self.path_template, **kwargs)
        path = self.format_path(self.path_template, self.path_params)
        url = urljoin(self.base_url, path)
        async with self.session.ws_connect(url) as ws:
            logger.debug('Connected ws to %s', url)
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    if msg.data == 'close cmd':
                        await ws.close()
                        break
                    else:
                        yield msg.json()
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break
        logger.debug('WS connection to %s is closed', url)


get = partial(ApiRequest, method='GET')
post = partial(ApiRequest, method='POST')
delete = partial(ApiRequest, method='DELETE')
patch = partial(ApiRequest, method='PATCH')
ws = WSRequest
