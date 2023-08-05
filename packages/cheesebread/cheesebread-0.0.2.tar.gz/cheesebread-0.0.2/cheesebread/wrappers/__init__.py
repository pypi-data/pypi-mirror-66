#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import aiofiles
import aiohttp
import asyncio
import requests
import riprova

from .. import logger
from ..config import AFFILIATES
from ..helpers import get_timestamp_pairs

import functools

from tqdm.auto import tqdm

async def wrapper(func):
    @functools.wraps(func)
    async def wrap(self, *args, **kwargs):
        print("inside wrap")
        #retrier = riprova.AsyncRetrier(evaluator=self.evaluator, on_retry=self.on_retry)
        #return await retrier.run(func, self , *args, **kwargs)
        #return func(self, *args, **kwargs)
    return await wrap

# Custom error object
class FailedRequestError(Exception):
    def __init__(self, code):
        self.code = code
    def __str__(self):
        return repr(f'Failed request ({self.code})')

class Wrapper(object):
    """
    Abstract facilitator for handling wrappers
    
    :param str AFFILIATE: affiliate
    :param str DIR: working directory
    """
    def __init__(self, AFFILIATE, DIR='.'):

        if not AFFILIATE in AFFILIATES:
            raise Exception(f"{AFFILIATE} is not a valid affiliate.")

        if not os.access(DIR, os.W_OK):
            raise Exception(f"{DIR} is not a valid directory.")

        self.AFFILIATE = AFFILIATE
        self.DIR = DIR

    API_URL = ''
    """API endpoint"""

    CONCURRENCY = 100

    RESOURCES = {}
    """API resources"""

    def _get_resource_url(self, resource):
        if not resource in self.RESOURCES:
            raise Exception(f'{resource} is not a valid resource')
        return f'{self.API_URL}{resource[1:]}'

    def get_sync(self, resource, headers, params):
        """
        Get resource synchronously

        :param str resource: resource
        :param dict headers: headers
        :param dict params: params

        :return: Response
        :rtype: :class:`requests.Response`
        """
        url = self._get_resource_url(resource)
   
        return requests.get(url, headers=headers, params=params)

    def _get_filename(self, resource, name):
        """
        :param str AFFILIATE: affiliate
        :param str DIR: working directory

        :return: Filename
        :rtype: str
        """
        filename = os.path.join(self.DIR, 
                                self.AFFILIATE, 
                                resource[1:], 
                                name)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        return filename

    async def _get_async(self, session, resource, headers={}, params={}, name_function=None):
        """
        Fetch resource asynchronously

        :param list resources: resources
        :param list headers: headers
        :param list params: params
        """
        url = self._get_resource_url(resource)
        async with session.get(url=url, headers=headers, params=params) as response:
            if response.status == 200:   
                data = await response.text()
                name = name_function(params)
                filename = self._get_filename(resource, name)
                async with aiofiles.open(filename, 'w+') as f:
                    await f.write(data)

            return response

    async def evaluator(self, response):
        """
        Retry evaluator function used to determine if the operation failed or not
        """
        if response.status >= 400:
            return FailedRequestError(response.status)
        return False

    async def on_retry(self, err, next_try):
        """
        On retry
        """
        logger.info(f'{err}. Next try in {next_try}ms')

    async def _get_async_with_retry(self, *args, **kwargs):
        """
        Fetch with retry
        """
        retrier = riprova.AsyncRetrier(
            backoff=riprova.ExponentialBackOff(factor=.5),
            evaluator=self.evaluator,
            on_retry=self.on_retry)
        return await retrier.run(self._get_async, *args, **kwargs)

    async def _get_async_bounded(self, semaphore, *args, **kwargs):
        """
        Fetch with semaphore
        """
        async with semaphore:
            return await self._get_async_with_retry(*args, **kwargs)

    async def get_async(self, resources=[], headers={}, params=[]):
        """
        Get resource asynchronously

        :param list resources: resources
        :param list headers: headers
        :param list params: params

        :return: List of responses
        :rtype: :class:`aiohttp.client_reqrep.ClientResponse`
        """
        semaphore = asyncio.Semaphore(self.CONCURRENCY)

        async with aiohttp.ClientSession() as session:
            tasks = []
            for r, p in zip(resources, params):
                # pass semaphore and session to every GET request
                task = asyncio.ensure_future(self._get_async_bounded(semaphore, session, r, headers, p))
                tasks.append(task)

            responses = [await f for f in tqdm(asyncio.as_completed(tasks), total=len(tasks))]
            return responses





