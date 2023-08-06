import hashlib
import inspect
import os
import pandas as pd

from slobad._wrappers import callit, timeit


class Slobad():
    #default values
    cache_dir = os.path.join(os.getcwd(), 'cache/')
    filetype = 'feather'

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def _cache_id(self):
        return self.name + '_' + self._id

    @property
    def _cache_fp(self):
        fname = self._cache_id + '.' + self.filetype
        cache_id = os.path.join(self.cache_dir, fname)
        return cache_id

    def _hash(self, _str):
        return hashlib.sha1(_str.encode()).hexdigest()

    @property
    def _id(self):
        '''
        by finding all components of an object we can describe with a string
        Create a string that describes in entirety what is identified as 
        a consistent object.
        '''
        #add to hash string the object vars
        attrs = list([[k, v] for k, v in vars(self).items()])
        attrs = ''.join(str(x) for x in attrs)
        #string of the artifact object
        cls = inspect.getsource(type(self))
        hash_str = self._hash(attrs + cls)
        return hash_str

    @timeit('Load from cache')
    def _load_from_cache(self):
        if self.filetype == 'feather':
            df = pd.read_feather(self._cache_fp)
        elif self.filetype == 'csv':
            df = pd.read_csv(self._cache_fp)
        return df

    def _find_name_cache_id(self):
        '''
        Search the cache for a filename that starts with se
        '''
        _list_dir = os.listdir(self.cache_dir)
        _ids = [f for f in _list_dir if f.endswith(self.filetype)]
        name_id = [k for k in _ids if k.startswith(self.name)]
        if len(name_id) > 1:
            raise Exception('Multiple keys found.')
        elif len(name_id) == 0:
            return None
        else:
            return name_id[0]

    def _clear_old(self):
        '''
        Remove old cache entry for artifact of the same name.
        '''
        old = self._find_name_cache_id()
        if old:
            os.remove(os.path.join(self.cache_dir, old))

    @timeit('Write to cache')
    def _write_to_cache(self, df):
        #TODO - add warning that mulitindex not supported
        if type(df) != type(pd.DataFrame()):
            raise TypeError('No DataFrame to write to cache.')
        elif df.empty:
            raise ValueError('Non-empty DataFrame required.')

        if self.filetype == 'feather':
            df.to_feather(self._cache_fp)
        elif self.filetype == 'csv':
            df.to_csv(self._cache_fp, header=True)
        else:
            raise ValueError('Invalid filetype provided.')

    @timeit('Execute create')
    def _create(self, *args, **kwargs):
        '''
        Naive way to add decorator to user defined method.
        '''
        df = self.create(*args, **kwargs)
        return df

    def _run_checks(self):
        #check if user-made create method exists
        if not hasattr(self, 'create'):
            raise RuntimeError('No create method found for slobad object.')
        #check if cache dir exists
        if not os.path.exists(self.cache_dir):
            #TODO - add warning that cache dir is being created
            os.makedirs(self.cache_dir)

    def is_cached(self):
        return os.path.isfile(self._cache_fp)

    @callit
    def run(self, *args, **kwargs):
        self._run_checks()
        if self.is_cached():
            df = self._load_from_cache()
        else:
            df = self._create(*args, **kwargs)
            self._clear_old()
            self._write_to_cache(df)
            #reload from cache to ensure consistency
            del df
            df = self._load_from_cache()
        return df
