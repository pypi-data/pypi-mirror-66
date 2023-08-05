#!/usr/bin/env python
# -*- coding: utf-8 -*-

import importlib
import os

from .. import logger
from ..config import AFFILIATES, DATA_DIR


def str_to_class(module_name, class_name, *args, **kwargs):
    try:
        module_ = importlib.import_module(module_name)
        try:
            class_ = getattr(module_, class_name)(*args, **kwargs)
        except AttributeError:
            print('Class does not exist')
    except ImportError:
        print('Module does not exist')
    return class_ or None

def check_data_dependencies(objects={}):
    def func_decorator(func):
        def func_wrapper(*args, **kwargs):
            results = list()
            for k, v in objects.items():
                c = str_to_class(k, v)
                results.append(c.check())
            if not all(results):
                raise Exception(f'Missing local data the function {func.__name__} depends on. Check documentation.')
            res = func(*args, **kwargs)
            return res
        return func_wrapper
    return func_decorator

class Catalog:
    """
    Facilitator for handling local datasets
    
    :param str dir: local directory to store datasets

    """

    def __init__(self, dir=DATA_DIR):
        self.dir = dir

    def __repr__(self):
        return f'Local datasets are stored at {self.dir}'

    LATEST = {}

    @property
    def dir(self): 
         return self._dir 
       
    @dir.setter 
    def dir(self, dir): 
        if not all((os.path.exists(dir), os.path.isdir(dir))):
            raise FileNotFoundError(f'{dir} is not a directory')
        self._dir = os.path.abspath(dir)

    @property
    def all(self):
        yield from filter(self._is_file, os.listdir(self.dir))

    def create(self): 
        return [str_to_class(v, k, dir=self.dir) for k, v in self.LATEST.items()]

    def delete(self, file_name):
        full_path = os.path.join(self.dir, file_name)
        if not all((os.path.exists(full_path), os.path.isfile(full_path))):
            raise FileNotFoundError('{} is not a file'.format(full_path))

        os.remove(full_path)

    def _is_file(self, filename):
        full_path = os.path.join(self.dir, filename)
        return os.path.isdir(full_path)

class Dataset:
    """
    Abstract facilitator for handling local datasets
    """
    BUCKET = None

    def __init__(self, dir=DATA_DIR):
        name = os.path.join(dir, self.__class__.__name__)
        os.makedirs(name, exist_ok=True)
        os.makedirs(os.path.join(name, 'data'), exist_ok=True)
        os.makedirs(os.path.join(name, 'raw'), exist_ok=True)
        self.dir = name

    def __repr__(self):
        return f'{self.__class__.__name__} is stored at {self.dir}'

    @property
    def dir(self): 
         return self._dir 
       
    @dir.setter 
    def dir(self, dir): 
        if not all((os.path.exists(dir), os.path.isdir(dir))):
            raise FileNotFoundError(f'{dir} is not a directory')
        self._dir = os.path.abspath(dir)

    def get(self, affiliate):
        """
        Get dataframe from dataset

        :param affiliate: affiliate
        :type affiliate: str
        :rtype: :class:`pandas.DataFrame`
        """
        raise NotImplementedError

    def check(self, subset=AFFILIATES):
        """
        Check local data of a subset of affiliates

        :param subset: subset of affiliates
        :type subset: set 
        :rtype: bool
        """
        return(all([os.path.exists(self._get_filename(s)) for s in subset]))

    def fetch(self, subset=AFFILIATES, **kwargs):
        raise NotImplementedError

    def consolidate(self, subset=AFFILIATES, **kwargs):
        """
        Consolidate raw data into data directory 

        :param subset: subset of affiliates
        :type subset: set 
        """
        raise NotImplementedError

    def download(self):  
        """
        Download from corresponding S3 bucket
        """     
        from ..helpers.aws import download_matching_s3_keys
        download_matching_s3_keys(self.dir, **self.BUCKET)

    def upload(self):
        """
        Upload to corresponding S3 bucket
        """
        from ..helpers.aws import upload_matching_keys
        upload_matching_keys(self.dir, **self.BUCKET)

    def _get_filename(self, name):
        """
        Get filename 

        :rtype: str
        """
        return f'{self.dir}/{self.BUCKET["prefix"]}/{name}{self.BUCKET["suffix"]}'

    def _get_s3_key(self, name):
        """
        Get S3 key 

        :rtype: str
        """
        return  f's3://{self.BUCKET["bucket"]}/{self.BUCKET["prefix"]}/{name}{self.BUCKET["suffix"]}'