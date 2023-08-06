from abc import ABC
import uuid
"""
    Configuration Abstract
"""

class Configuration(ABC):
    def __init__(self, *args, **kwargs):
        self._id:str = kwargs.get("id", uuid.uuid4().hex)
        self.initialize(**kwargs)
    
    @property
    def identity(self):
        return self._id

    @property
    def handler(self):
        raise NotImplementedError("All configurations must have a handler attached")

    def initialize(self, **kwargs):
        self.init_required(**kwargs)
        self.init_handler(**kwargs)
        self.init_search(**kwargs)
    
    def init_load_settings(self, **kwargs):
        raise NotImplementedError("Load settings")

    def init_required(self, **kwargs):
        raise NotImplementedError("All configurations need to have a set of require information")

    def init_handler(self, **kwargs):
        raise NotImplementedError("You need to have a handler to access")

    def init_search(self, **kwargs):
        raise NotImplementedError("You need to have a means to search")

    
    def save_config(self):
        raise NotImplementedError("Each configuration has a customized save function")

    def load_config(self):
        raise NotImplementedError("Each configuration must have its own load procedure")

    def by_id(self, _id:str):
        raise NotImplementedError("Find implementation by ID")