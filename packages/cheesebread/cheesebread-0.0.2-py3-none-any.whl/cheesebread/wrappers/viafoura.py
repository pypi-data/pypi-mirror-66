#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module implements a wrapper around Viafoura"""

import datetime
import os
import uuid

import pandas as pd
import requests

from .. import logger
from ..config import VIA_CLIENT_ID, VIA_SECRET
from ..wrappers import Wrapper

class Viafoura(Wrapper):
    """
    Helper and wrapper around Viafoura's User Engagement API

    :param str AFFILIATE: affiliate 
    :param str DIR: working directory
    """
    def __init__(self, AFFILIATE, DIR='.'):
        super().__init__(AFFILIATE, DIR) 

        try:
            self.VIA_SCOPE = Viafoura.SCOPES[AFFILIATE]
        except KeyError:
            raise Exception(f"{AFFILIATE} does not have a valid scope.")

        self.TOKEN = self.token

    API_URL = 'https://data.viafoura.io/data/v1/'
    """Viafoura API endpoint"""

    CONCURRENCY = 5

    RESOURCES = {
        '/engagement/indicator/clicks/total',
        '/engagement/visitors/attention',
        '/users/comments',
        '/users/dislikes',
        '/users/follows/pages',
        '/users/follows/users',
        '/users/likes',
        '/users/logins',       
        '/users/visits',
    }
    """Viafoura API resources"""

    SCOPES = {
        'al' : '00000000-0000-4000-8000-03c76f429dfe',
        'cleveland' : '00000000-0000-4000-8000-0912b7efe619',
        'gulflive' : '00000000-0000-4000-8000-05f6bd89bb11',
        'lehighvalleylive' : '00000000-0000-4000-8000-07efd7dab981',
        'mardigras' : '00000000-0000-4000-8000-058c3e5f9df0',
        'masslive' : '00000000-0000-4000-8000-038ec97343a4',
        'mlive' : '00000000-0000-4000-8000-08a1bfc37204',
        'newyorkupstate' : '00000000-0000-4000-8000-022cc4967ea9',
        'nj' : '00000000-0000-4000-8000-0457ac567772',
        'nola' : '00000000-0000-4000-8000-02f0abef9d13',
        'oregonlive' : '00000000-0000-4000-8000-06b08a0b664a',
        'pennlive' : '00000000-0000-4000-8000-0914f42445e4',
        'silive' : '00000000-0000-4000-8000-09ee64eb614d',
        'syracuse' : '00000000-0000-4000-8000-09144749c930'
    }
    """Viafoura API scopes"""

    @property
    def session_id(self):
        return int(uuid.UUID(self.VIA_SCOPE, version=4).node)

    @property
    def token(self):
        """
        Viafoura API access token
        """
        response = requests.post('https://auth.viafoura.io/authorize_client', 
                                auth=(VIA_CLIENT_ID, VIA_SECRET), 
                                data={'grant_type': 'client_credentials', 'scope': self.VIA_SCOPE})
        try:
            return response.json()['access_token']
        except:
            return ''
            
    def _get_resource_url(self, resource):
        if not resource in self.RESOURCES:
            raise Exception(f'{resource} is not a valid resource')
        return f'{self.API_URL}{self.VIA_SCOPE}{resource}'

    def get_sync(self, resource, headers={}, params={}):
        """
        Get resource synchronously

        :param str resource: resource
        :param dict headers: headers
        :param dict params: params

        :return: Response
        :rtype: :class:`requests.Response`
        """
        headers.update({'Authorization': f'Bearer {self.token}'})

        return super().get_sync(resource, headers, params)

    async def _get_async(self, session, resource, headers={}, params={}, name_function=None):
        headers.update({'Authorization': f'Bearer {self.TOKEN}'})
        name_function = lambda x: datetime.datetime.fromtimestamp(x.get('from')/1000).strftime('%Y-%m-%d') + '.json'

        return await super()._get_async(session, resource, headers, params, name_function)

    async def on_retry(self, err, next_try):
        """
        On retry
        """
        logger.info(f'{err}. Next try in {next_try}ms')
        if err.code == 401:
            self.TOKEN = self.token
            logger.info(f'Renewing token...')

    def get_uid(self, user_uuid):
        """
        Get UID from Viafoura

        :param str user_uuid: Viafoura user UUID
        :return: UID 
        :rtype: str
        """
        uuid_node = int(uuid.UUID(user_uuid, version=4).node)
        endpoint = f'https://api.viafoura.com/v2/{self.session_id()}/users/{uuid_node}'
        r = requests.get(endpoint)

        data = r.json()
        try:
            return data['result']['social_login_id']
        except KeyError:
            return None

    def batch(self, indexes):
        """
        Request Viafoura user information in batch
        """
        import json
        from ..helpers import chunks

        responses = list()
        errors = dict()

        # get responses and respect Viafoura API limit
        for chunk in chunks(indexes, 50):
            payloads = dict()
            for user in chunk:
                uuid_node = int(uuid.UUID(user, version=4).node)
                payloads[user] = dict(route=f'/users/{uuid_node}', verb='get')

            payload = {'site': self.session_id, 'requests' : payloads}
            url = f'https://api.viafoura.co/v2/?json={json.dumps(payload, separators=(",",":"))}'

            response = requests.get(url)
            responses.append(response)
        
        # pluck key
        users = dict()
        for response in responses:

            try:
                response = response.json()

                for k, v in response['responses'].items():
                    if 'result' in v:
                        users[k] = v['result']['social_login_id']
                    else:
                        users[k] = v['error']
                        errors[k] = v['error']
            except:
                # this will be 
                pass

        # fix bad responses
        for u in set(indexes) - set(users):
            uuid_node = int(uuid.UUID(u, version=4).node)
            url = f'https://api.viafoura.co/v2/{self._get_session_id()}/users/{uuid_node}'
            response = requests.get(url).json()
            if 'result' in response:
                users[u] = response['result']['social_login_id']
            else:
                users[k] = 'User not found.'
                errors[k] = 'error'

        df = pd.DataFrame.from_dict(users, orient='index', columns=['uid'])
        df.to_json(f'{self.DIR}/{self.AFFILIATE}.json.gz')

        import json

        with open(f'{self.DIR}/errors_{self.AFFILIATE}.json', 'w') as fp:
            json.dump(errors, fp)