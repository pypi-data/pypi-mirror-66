import uuid
import maya

from typing import Optional
from jamboree import Jamboree
from jamboree.base.processors.abstracts import Processor
from darwin_handlers.search import PrototypeSearchFeatures
from darwin_handlers.search.backtesting.topics import backtests as bts
from darwin_handlers.search.backtesting.topics import episodes as eps
from darwin_handlers.search.backtesting.topics import strategy as sst
from darwin_handlers.search.backtesting.topics import universe as uni

class CreateAccessor:
    def __init__(self):
        self._processor: Optional[Processor] = None
        self._backtest = bts.BacktestCreate()
        self._episodes = eps.EpisodeCreate()
        self._strategy = sst.StrategyCreate()
        self._universe = uni.UniverseCreate()

    @property
    def processor(self):
        if self._processor is None:
            raise AttributeError("Processor hasn't been set for create calls in search.")
        return self._processor

    @processor.setter
    def processor(self, _processor):
        self._processor = _processor

    @property
    def backtest(self):
        self._backtest.processor = self.processor
        return self._backtest
    
    @property
    def episodes(self):
        self._episodes.processor = self.processor
        return self._episodes
    
    @property
    def strategy(self):
        self._strategy.processor = self.processor
        return self._strategy

    @property
    def universe(self):
        self._universe.processor = self.processor
        return self._universe