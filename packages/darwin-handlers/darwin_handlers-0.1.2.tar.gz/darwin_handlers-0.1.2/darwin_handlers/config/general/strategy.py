from darwin_handlers.config.configuration import Configuration
from jamboree.utils.core import consistent_hash

class StrategyConfig(Configuration):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """ """

    @property
    def handler(self):
        pass

    def init_required(self, **kwargs):
        pass


    def init_handler(self, **kwargs):
        pass

    def init_search(self, **kwargs):
        pass
    
    def to_dict(self):
        return {}

    def to_hash(self):
        return consistent_hash(self.to_dict()) 