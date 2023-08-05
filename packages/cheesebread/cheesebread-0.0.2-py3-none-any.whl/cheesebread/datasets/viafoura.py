#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import json
import os
import shutil

import itertools

import asyncio
import pandas as pd

from tqdm.auto import tqdm

from .. import logger
from ..config import AFFILIATES, DATA_DIR
from ..datasets import Dataset
from ..helpers import get_timestamp_pairs
from ..wrappers.viafoura import Viafoura


class ViafouraEngagementDataset(Dataset):
    """Facilitator for handling the dataset"""
    
    BUCKET = {
        'bucket' : 'ada-data-viafoura-engagement',
        'prefix' : 'data',
        'suffix' : '.xz'
    }

    def get(self, affiliate, local=True):
        
        if local:
            df = pd.read_csv(self._get_filename(affiliate))
        else:
            df = pd.read_csv(self._get_s3_key(affiliate))

        # set index
        df = df.set_index(['index', 'date', 'uid'])

        # otimize memory
        df[df.columns] = df[df.columns].fillna(0.0).apply(pd.to_numeric, downcast='integer', errors='coerce')

        return df

    def fetch(self, subset=AFFILIATES, start='', end=''):
        """
        Fetch asynchronously new data of subset of affiliates for given interval 

        :param subset: subset of affiliates
        :type subset: set
        :param between: tuple containing start and end. Expected format %Y-%m-%d
        :type tuple:
        """
        pbar = tqdm(subset)
        for affiliate in pbar:
            pbar.set_description(f'Fetching {affiliate}...')

            args = {
                'AFFILIATE' : affiliate,
                'DIR' : os.path.join(self.dir, 'raw'),
            }
            wrapper = Viafoura(**args)

            # pass all resources and parameters
            resources = wrapper.RESOURCES
            params = [{'from':int(i)*1000,'to':int(j)*1000} for i, j in get_timestamp_pairs(start, end)]
            resources, params = zip(*itertools.product(resources, params))

            coros = wrapper.get_async(resources=resources, params=params)
            
            asyncio.run(coros)

    def consolidate(self, subset=AFFILIATES):
        """
        Concatenate objects into dataframe

        :param subset: subset of affiliates
        :type subset: set
        """
        pbar = tqdm(subset)
        for affiliate in pbar:
            pbar.set_description(f'Consolidating {affiliate}...')

            dataframes_resource = list()
            for resource in Viafoura.RESOURCES:
                dataframes_date = list()
                for file in glob.glob(f'{self.dir}/raw/{affiliate}{resource}/*.json'):
                    name, _ = os.path.splitext(os.path.basename(file))
                    with open(file, 'r') as f:
                        data = json.load(f)
                        if 'result' in data.keys():
                            df = pd.DataFrame(data['result'])
                            if not df.empty:
                                df = df.rename({'user': 'index', 'aggregate': f'{name}'}, axis=1)
                                df = df.set_index('index')
                                dataframes_date.append(df)

                if dataframes_date:
                    df = pd.concat(dataframes_date, axis=1, ignore_index=False, sort=False)
                    df = df.reset_index()
                    df = pd.melt(df, id_vars=['index'], var_name=['date'], value_name=resource)
                    dataframes_resource.append(df)

            if dataframes_resource:
                df = dataframes_resource[0]

                for di in dataframes_resource[1:]:
                    df = pd.merge(df, di, on=['index', 'date'], how='outer')  

                # apply pipe
                df = df.set_index(['index', 'date'])
                df = df[~df[df.columns].isnull().all(axis=1)]
                df = df[sorted(df.columns)]
                df = df.sort_values('date')
                
                # get uid
                df = self._get_uid(df, affiliate)

                df.to_csv(self._get_filename(affiliate))

    def _get_uid(self, df, affiliate):
        """
        Create column with corresponding Gygia UID

        :param affiliate: affiliate
        :type affiliate: str
        :param df: dataframe
        :type: :class:`pd.DataFrame`

        :rtype: :class:`pd.DataFrame`
        """
        identity = ViafouraUserDataset()

        # fetch ViafouraUserDataset if not available
        if not identity.check([affiliate]):
            indexes = df.index.get_level_values('index').unique()
            identity.fetch([affiliate], indexes)

        users = identity.get(affiliate, local=True).to_dict()['uid']
        
        # create column
        df['uid'] = df.index.get_level_values('index').map(lambda x: users.get(x, 'User not found.'))

        return df

class ViafouraUserDataset(Dataset):
    """Facilitator for handling the dataset"""
    BUCKET = {
        'bucket' : 'ada-data-viafoura-user',
        'prefix' : 'data',
        'suffix' : '.json.gz'
    }

    def get(self, affiliate, local=True):
        df = pd.read_json(self._get_filename(affiliate), orient='columns')
        return df

    def fetch(self, subset=AFFILIATES, indexes=[]):
        """
        Fetch 

        :param subset:
        :type subset: set
        :param indexes: list of indexes
        :type indexes: list
        """
        pbar = tqdm(subset)
        for affiliate in pbar:
            pbar.set_description(f'Fetching {affiliate}...')

            args = {
                'DIR' : os.path.join(self.dir, 'raw'),
                'MARKET' : affiliate,
            }
            v = Viafoura(**args)
            v.batch(indexes)

        self.consolidate(subset)

    def consolidate(self, subset=AFFILIATES):
        for affiliate in subset:
            shutil.copy(os.path.join(self.dir, 'raw', f"{affiliate}{self.BUCKET['suffix']}"),  self._get_filename(affiliate))  
