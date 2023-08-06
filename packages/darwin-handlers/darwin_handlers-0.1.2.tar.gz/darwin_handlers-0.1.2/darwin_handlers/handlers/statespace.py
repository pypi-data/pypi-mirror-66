""" 
    Create a price handler. Used to do all price commands that run throughout the application.
    This price handler should use lists, as it will be faster to handle.
"""


import uuid
from uuid import uuid1
from jamboree import Jamboree, DBHandler
from jamboree.handlers.complex.backtest import BacktestDBHandler
from typing import Dict, Any, List


# NOTE: I'm probably going to have to separate everything here from

class StateSpaceHandler(BacktestDBHandler):
    """ Use this handler to manage the settings for things like data collection. """
    def __init__(self, limit=500):
        super().__init__()
        self.entity = "state_space"
        self.required = {
            "name": str,
            "episode": str,
            "live": bool
        }
        self._limit = 500
    

    """ 
        ---------------------------------------------------------------------------------
        ----------------------------------- Properties ----------------------------------
        ---------------------------------------------------------------------------------
    """

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, _limit):
        self._limit = _limit


    

    def reset(self):
        """ No idea what goes here. But it should reset something."""
        super().reset()

def main():
    jam = Jamboree()
    statespace_handler = StateSpaceHandler()
    statespace_handler['name'] = "main_space"
    statespace_handler['episode'] = uuid.uuid4().hex
    statespace_handler['live'] = False
    statespace_handler.processor = jam


if __name__ == "__main__":
    main()