#!/usr/bin/env python
# -*- coding: utf-8 -*-

import aiofiles
import aiohttp

from riprova import retry, ExponentialBackOff

from .. import logger

BACKOFF=ExponentialBackOff(factor=.5)

# Custom error object
class FailedRequestError(Exception):
    def __init__(self, code):
        self.code = code
    def __str__(self):
        return repr(f'Failed request ({self.code})')

# Retry evaluator function used to determine if the operated failed or not
async def evaluator(status):
    if status > 400:
        return FailedRequestError(status)
    return False

# On retry even subcriptor
async def on_retry(err, next_try):
    logger.error(f'{err}. Next try in {next_try}ms')

# Register retriable operation with custom evaluator
@retry(backoff=BACKOFF, evaluator=evaluator, on_retry=on_retry)
async def fetch(filename, url, headers, params):
    """
    Asynchronously save response to file

    Parameters:
        :param (str) filename
        :param (str) url
        :param (dict) headers
        :param (dict) params
    """        
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url=url, params=params) as response:
            async with aiofiles.open(filename, 'w+') as f:
                data = await response.text()
                await f.write(data)
            return response.status