""" 
    Create a price handler. Used to do all price commands that run throughout the application.
    This price handler should use lists, as it will be faster to handle.
"""

from jamboree import Jamboree, DBHandler
from crayons import (magenta)


# # TODO: Rethink design here and come back to this.

class TradeHandler(DBHandler):
    def __init__(self, limit=500):
        super().__init__()
        self.entity = "trades"
        self.required = {
            "episode": str,
            "exchange": str,
            "user_id": str,
            "live": bool
        }
        self._limit = 500
        self._search_handler = None
    

    """ 
        ---------------------------------------------------------------------------------
        ----------------------------------- Properties ----------------------------------
        ---------------------------------------------------------------------------------
    """

    @property
    def limit(self):
        return self._limit

    def limit(self, _limit):
        self._limit = _limit


    @property
    def search(self):
        return self._search_handler

    """ 
        ----------------------------------------------------------------------------------
        ------------------------------- Accessor Functions -------------------------------
        ----------------------------------------------------------------------------------
    """


    def save_trade(self, trade):
        """ Save trade in 2 ways to make it easy to access those trades later. """

        pass
    
    
    def latest_trade(self):
        return {}



    def latest_trade_by_user(self):
        return {}


    def latest_trade_by_asset(self):
        return {}


    
    def get_total_slippage(self):
        """ Search through all user's closed trades and get the total slippage """
        pass
    
    def change_trade_status(self):
        """ Change the status of the trade """
        pass

    
    """ 
        ----------------------------------------------------------------------------------
        ------------------------------- Counting Functions -------------------------------
        ----------------------------------------------------------------------------------
    """
    

    def trade_count(self, alt={}) -> int:
        """ Get the number of trades we have active in the given exchange. """
        count = self.count(alt=alt)
        return count
    
    def trade_exchange_count(self, exchange:str):
        alt = {"exchange": exchange}
        count = self.count(alt=alt)
        return count