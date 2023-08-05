__version__ = '1.0'

import os
import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class Config:
    def __init__(self, file_obj=None):
        self._cached_config = {}
        self._cast_func_mapping = {}
        if file_obj:
            self.load(file_obj)

    def load(self, file_obj):
        # file_obj may be filename
        if isinstance(file_obj, str):
            filename = file_obj
            with open(filename) as file_obj:
                config = yaml.load(file_obj, Loader=Loader)
        else:
            config = yaml.load(file_obj, Loader=Loader)
        self.merge_config(config)

    def load_env(self):
        self.merge_config(os.environ)

    def set_cast_func(self, key_str, cast_func):
        self._cast_func_mapping[key_str.upper()] = cast_func

    def _set_config(self, key_str, value):
        nested_key_lst = key_str.upper().lstrip('.').split('.')
        config_dict = self._cached_config
        for index, key in enumerate(nested_key_lst):
            if index < len(nested_key_lst) - 1:
                if not isinstance(config_dict.get(key), dict):
                    config_dict[key] = {}
                config_dict = config_dict[key]
            else:
                config_dict[key] = value

    def merge_config(self, new_config, prefix_str=''):
        for key, value in new_config.items():
            key_str = '{prefix_str}.{key}'.format(prefix_str=prefix_str,
                                                  key=key)
            if isinstance(value, dict):
                self.merge_config(value, prefix_str=key_str)
            else:
                self._set_config(key_str, value)

    def __getitem__(self, key_str):
        config = self._cached_config
        for key in key_str.upper().split('.'):
            config = config[key]
        cast_func = self._cast_func_mapping.get(key_str.upper())
        if cast_func:
            config = cast_func(config)
        return config
