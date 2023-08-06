from typing import Optional

from addict import Dict
from loguru import logger

from darwin_handlers.config.general import TimeConfig


class BacktestEnvironment(object):
    """ Use to setup and start a backtest """
    def __init__(self,
                 name: str,
                 time_conf:TimeConfig=None,
                 portfolio_conf=None,
                 price_conf=None,
                 user_conf=None,
                 strategy_conf=None,
                 *args,
                 **kwargs):
        # Search for all backtest
        self._search = None
        # Set multi data config
        self.time_conf = time_conf
        self.portfolio_conf = portfolio_conf
        self.price_conf = price_conf
        self.user_conf = user_conf
        self.strategy_conf = strategy_conf
        self.create()

    @property
    def search(self):
        return self._search

    @property
    def monitor(self):
        """ What we use to aggrgate the information about the backtest."""
        pass

    def performance(self):
        """ Get the performance of the backtest """
        pass

    def status(self):
        """ Get the current status of the backtest. Is it finished? How much time left?"""
        pass

    def resources(self):
        pass

    def create(self):
        self.extract_configs()

    def connect(self):
        """ Input settings of a place to send the start command to remote service"""
        logger.debug(
            "Checking http connection of remote service. Crashes if it's not there."
        )

    def deploy(self):
        pass

    def extract_configs(self):
        logger.info("Pulling configuration information")
        logger.info("Create an exact search query")
        is_exist = self.check_existing()
        if is_exist:
            logger.error(
                "Can't create an existing backtest. Loading that instead.")
        else:
            logger.success("Doesn't exist. Creating it in database")

    def check_existing(self) -> bool:
        logger.info("Checking to see if the thing exists")
        return True

    def check_existing_runs(self):
        pass

    def push_backtest_to_system(self):
        pass

    def check_all_configurations(self):
        all_conf = [
            self.time_conf, self.portfolio_conf, self.price_conf,
            self.user_conf, self.strategy_conf
        ]
        if None in all_conf:
            raise AttributeError(
                "One of the configurations has not been assigned. ")
        # Call the time config and pull the information

        

    def start(self):
        self.check_all_configurations()
        self.check_existing_runs()
        self.connect()
        self.push_backtest_to_system()


def main():
    bt = BacktestEnvironment("Name of backtest")
    bt.start()


if __name__ == "__main__":
    main()
