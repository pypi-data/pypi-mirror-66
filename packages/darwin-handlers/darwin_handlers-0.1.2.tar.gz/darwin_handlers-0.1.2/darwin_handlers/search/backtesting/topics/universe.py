import uuid
import maya
import random
from cytoolz.curried import pipe, map, filter, get
from cytoolz.itertoolz import unique

from typing import Optional, List
from jamboree import Jamboree
from jamboree.base.processors.abstracts import Processor
from darwin_handlers.search import PrototypeSearchFeatures

from loguru import logger

class BacktestUniverseManagement(PrototypeSearchFeatures):
    """ 
        Use to find strategies by asset and universe and vice versa. 
        
        We should be able to find universes and assets by strategy as well

        - Is there any backtest that's running right now?
        - Is the episode still running?
        - Update the episode's status
        - Start an episode
        - Get the number of episodes that are running

        ```py
            # Start a new backtest
            backtest_manager.create.universe.init(universe: str, strategy: str, asset:str)

            backtest_manager.update.episodes.status(backtest_id, "...")

            # Get the difference
            backtest_manager.info.episodes.by_backtest(backtest_id)
            backtest_manager.info.episodes.by_episode(episode_id)

            
            # General running episodes
            backtest_manager.info.episodes.total
            backtest_manager.info.episodes.total_active
            backtest_manager.info.episodes.total_inactive



            backtest_manager.info.episodes.active_by(backtest)
            backtest_manager.info.episodes.inactive_by(backtest)
            backtest_manager.info.episodes.is_running(backtest_id, by="backtest")
            backtest_manager.info.episodes.is_running(episode_id, by="episode")

            backtest_manager.info.episodes.status(episode_id, by="episode")
            backtest_manager.info.episodes.status(backtest_id, by="backtest")
        ```
    """
    def __init__(self):
        super().__init__()
        self.entity = "universe_strat"
        self.dreq = {"universe": str, "strategy": str, "asset": str}
        self.allowed = ["RUNNING", "DONE"]

class UniverseCreate(BacktestUniverseManagement):
    """ 
        Used to find stategies and universes by asset or universe. 

        - Get the 

        ```py
            # Match a strategy with a universe and asset
            backtest_manager.create.universe.init(universe: str, strategy: str, asset:str)
        ```
    """
    def __init__(self):
        super().__init__()
    
    def init(self, universe: str, strategy: str, asset:str):
        universe_mix_id = self.Create(no_overwrite_reqs=True, universe=universe, strategy=strategy, asset=asset)
        return universe_mix_id

    
    
class UniverseUpdate(BacktestUniverseManagement):
    """ 
        Use to find backtest information by episodes, and episodes by backtest

        ```py
            # Start a new backtest
            backtest_manager.create.universe.init(backtest_id)

            
        ```
    """
    def __init__(self):
        super().__init__()
        
    
    def status(self, episode_id:str, status="RUNNING"):
        """ Update episode status """
        self.UpdateMany({"episode": episode_id}, status=status)
        

    


class UniverseInfo(BacktestUniverseManagement):
    """ 
        Use to find backtest information by episodes, and episodes by backtest

        - Is there any backtest that's running right now?
        - Find all of the unique universes

        ```py
            # Get the difference
            backtest_manager.info.episodes.by_backtest(backtest_id)
            
        ```
    """
    def __init__(self):
        super().__init__()
        self.allowed = ["backtest", "episode"]
    
    @property
    def universes(self) -> List[dict]:
        """ get all episodes """
        universes = self.Find("*")
        unis = pipe(universes, map(lambda uni: uni['universe']), unique, list)
        return unis
    
    @property
    def assets(self) -> List[dict]:
        """ Get all active episodes"""
        assets = self.Find("*")
        unis = pipe(assets, map(lambda uni: uni['asset']), unique, list)
        return unis
    
    @property
    def strategies(self) -> List[str]:
        """ Return a list of list of strategy IDs"""
        strategies = self.Find("*")
        unis = pipe(strategies, map(lambda uni: uni['strategy']), unique, list)
        return unis



    @property
    def total_universes(self) -> int:
        return len(self.universes)

    @property
    def total_strategies(self) -> int:
        return len(self.strategies)
    
    @property
    def total_assets(self) -> int:
        return len(self.assets)

    
    def strategy_by_asset(self, assetid:str):
        """ Get all strategies by asset ID """
        strategy_list = self.Find(asset=assetid)
        strats = pipe(strategy_list, map(lambda uni: uni['strategy']), unique, list)
        return strats
        

    def strategy_by_universe(self, univeseid):
        """ Get all strategies by universe """
        strategies = self.Find(universe=univeseid)
        strats = pipe(strategies, map(lambda uni: uni['strategy']), unique, list)
        return strats

    def asset_by_strategy(self, strategy:str):
        assets = self.Find(strategy=strategy)
        _assets = pipe(assets, map(lambda assss: assss['asset']), unique, list)
        return _assets
    
    def asset_by_universe(self, universe:str):
        assets = self.Find(universe=universe)
        _assets = pipe(assets, map(lambda assss: assss['asset']), unique, list)
        return _assets

class UniverseRemove(BacktestUniverseManagement):
    """ 
        
    """
    def __init__(self):
        super().__init__()

    def by_strat_uni(self, strategy:str, universe:str):
        """ Remove episode by id"""
        self.Remove(strategy=strategy, universe=universe)

    def by_strat_asset(self, strategy:str, asset:str):
        self.Remove(strategy=strategy, asset=asset)


def manage_assets():
    strat_id = uuid.uuid4().hex
    universe_ids = [uuid.uuid4().hex for x in range(10)]
    asset_ids = [uuid.uuid4().hex for x in range(200)]
    
    proc = Jamboree()
    universe_create =    UniverseCreate()
    universe_update =    UniverseUpdate()
    universe_info =      UniverseInfo()
    universe_remove =    UniverseRemove()
    
    universe_create.processor = proc
    universe_update.processor = proc
    universe_info.processor = proc
    universe_remove.processor = proc

    for assetid in asset_ids:
        for _ in range(10):
            universeid = random.choice(universe_ids)
            strat_uni_id = universe_create.init(universeid, strat_id, assetid)
        strategies = universe_info.strategy_by_asset(assetid)
        for x in strategies:
            logger.success(f"Sending command to strategy: {x}. Looking for strategy.") 
            logger.debug(assetid)

        logger.error(strat_uni_id)
        assets = universe_info.asset_by_universe(universeid)
        logger.warning(assets)

if __name__ == "__main__":
    manage_assets()