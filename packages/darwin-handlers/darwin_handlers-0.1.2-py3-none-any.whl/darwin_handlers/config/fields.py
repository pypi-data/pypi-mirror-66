import maya
import uuid
from typing import Union, Optional
from dataclasses import dataclass, field, fields
from jamboree.utils.core import consistent_hash
from addict import Dict as ADict


class TimeField:
    def __init__(self, time=None, timezone="UTC"):
        self.time: Optional[str, float, int] = time
        self.timezone: Optional[str] = timezone

    def to_epoch(self) -> float:
        if not self.timezone or not self.time:
            raise ValueError("Timezone and time should not be None")

        _dt = maya.when(self.time, timezone=self.timezone)
        return _dt._epoch


class StepField:
    """ Use to deal with step information """
    def __init__(self):
        self.milliseconds = 0
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.days = 0
        self.weeks = 0

    def to_dict(self):
        return {
            "microseconds": self.milliseconds,
            "seconds": self.seconds,
            "minutes": self.minutes,
            "hours": self.hours,
            "days": self.days,
            "weeks": self.weeks
        }
    def to_epoch(self):
        current_time = maya.now()
        next_time = maya.now()
        next_time = next_time.add(**self.to_dict())
        return next_time._epoch - current_time._epoch

class LookbackField:
    def __init__(self):
        self.milliseconds = 0
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.days = 0
        self.weeks = 0

    def to_dict(self):
        return {
            "milliseconds": self.milliseconds,
            "seconds": self.seconds,
            "minutes": self.minutes,
            "hours": self.hours,
            "days": self.days,
            "weeks": self.weeks
        }


""" Portfolio Related Fields """

class UserField:
    identity: str = uuid.uuid4().hex
    

@dataclass
class PortfolioField:
    starting_price: float = 10000.0
    exchange: str = "binance"


    def to_dict(self):
        _dict = ADict()
        _dict.exchange = self.exchange
        _dict.starting_price = self.starting_price
        _res = _dict.to_dict()
        return _res
    
    def to_hash(self):
        return consistent_hash(self.to_dict()) 


if __name__ == "__main__":
    example_portfolio = PortfolioField(starting_price=1000.0)
    print(example_portfolio.to_hash())