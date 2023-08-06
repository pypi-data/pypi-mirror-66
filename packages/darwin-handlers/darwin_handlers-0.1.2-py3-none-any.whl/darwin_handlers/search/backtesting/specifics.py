import uuid
import maya

from typing import Optional
from jamboree import Jamboree
from jamboree.base.processors.abstracts import Processor
from darwin_handlers.search import PrototypeSearchFeatures

from loguru import logger




class CoreBacktestSearch(PrototypeSearchFeatures):
    """ 
        # Core Backtest Search  

        Use to find backtesting information.

        Examples:

        ```py

            backtest_manager.create.backtest.init(**kwargs)


            backtest_manager.update.backtest.time(id, **kwargs)
            backtest_manager.update.backtest.portfolio(id, **kwargs)
            backtest_manager.update.backtest.description(id, **kwargs)
            backtest_manager.update.backtest.strategy(id, **kwargs)

            backtest_manager.info.backtest.by_id(id)
            backtest_manager.info.backtest.by_user(userid)
            backtest_manager.info.backtest.by_exchange(exchange)
            backtest_manager.info.backtest.by_strategy(strategy_id)
            backtest_manager.info.backtest.by_universe(universe_id)

            backtest_manager.info.backtest.start_before('...')
            backtest_manager.info.backtest.start_after('...')
            backtest_manager.info.backtest.start_between(start='...', end='...')

            backtest_manager.info.backtest.end_before('...')
            backtest_manager.info.backtest.end_after('...')
            backtest_manager.info.backtest.end_between(start='...', end='...')


            backtest_manager.remove.backtest.by_user(userid)
            backtest_manager.remove.backtest.by_exchange(exchange)
            backtest_manager.remove.backtest.by_strategy(strategy_id)
            backtest_manager.remove.backtest.by_universe(universe_id)

            backtest_manager.info.backtest.over_cutoff(backtestid, current_time)
        ```
    """

    # Backtesting is basically a
    def __init__(self):
        super().__init__()
        self.entity = "core_backtest"
        self.dreq = {
            "userid": str,
            "name": str,
            "description": str,

            # Time series information.
            "start_epoch": float,
            "end_epoch": float,
            "step_size": float,

            "start_cash": float,
            "exchange": str,
            "strategy": str,
            "universe": str,
        }
        self.must_have = ['name', 'description', 'userid']
        self.time_forced_args = ["start_epoch", "end_epoch", "step_size"]
        self.portfolio_forced_args = ["start_cash", "exchange"]

    def find_by_user(self, userid: str):
        """ Find all backtests by user id. """
        backtests = self.Find(userid=userid)
        return backtests

    def add_time(self, identity:str, **kwargs):
        self.check_other_forced(self.time_forced_args, kwargs)
        self.UpdateID(identity, **kwargs)



class BacktestEpisodeStatus(PrototypeSearchFeatures):
    """ 
        Use to find backtest information by episodes, and episodes by backtest

        - Is there any backtest that's running right now?
        - Is the episode still running?
        - Update the episode's status
        - Start an episode
        - Get the number of episodes that are running

        ```py
            # Start a new backtest
            backtest_manager.create.episodes.init(backtest_id)

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
        self.entity = "episode_backtest_status"
        self.dreq = {"episode": str, "backtest": str, "status":str}
        self.must_have = ['episode', 'backtest']


class StrategyStatusSearch(PrototypeSearchFeatures):
    """ 
        
        Used to do the following:

        - Determine if a strategy is live
        - Attach the stategy to a broker
        - Turn a strategy on and off

        

        ```py

            backtest_manager.create.status.init(strategy_id, **kwargs)

            
            backtest_manager.info.status.active
            backtest_manager.info.status.inactive

            backtest_manager.info.strategy.by_user(userid)
            backtest_manager.info.strategy.by_broker(brokerid)
            backtest_manager.info.strategy.by_complex(**kwargs)


            backtest_manager.info.strategy.is_live(strategy_id)
            backtest_manager.info.strategy.broker_by(strategy_id)

            # Get all of the strategies with a given asset id over a current_time
            backtest_manager.info.strategy.live_with(asset_id=asset_id, over=current_time)
        ```
    """
    def __init__(self):
        super().__init__()
        self.entity = "stategy_online"
        self.dreq = {"strategy": str, "broker": str, "user":str, "live": bool}
        self.must_have = ['episode', 'backtest']


# Get all of the active strategies with an asset.

class UniverseAssetSearch(PrototypeSearchFeatures):
    """ Used to find all strategies that are deployed"""
    def __init__(self):
        super().__init__()
        self.dreq = {"universe": str, "strategy": str, "asset": str}


"""
backtest_manager.create.status.init(strategy_id, **kwargs)

            
backtest_manager.info.status.active
backtest_manager.info.status.inactive

backtest_manager.info.strategy.by_user(userid)
backtest_manager.info.strategy.by_broker(brokerid)
backtest_manager.info.strategy.by_complex(**kwargs)


backtest_manager.info.strategy.is_live(strategy_id)
backtest_manager.info.strategy.broker_by(strategy_id)

# Get all of the strategies with a given asset id over a current_time
backtest_manager.info.strategy.live_with(asset_id=asset_id, over=current_time)
"""