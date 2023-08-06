import maya
import uuid
from typing import Union, Optional
import darwin_handlers.config.fields as fd
from jamboree.handlers.default import TimeHandler
from jamboree.utils.core import consistent_hash
from darwin_handlers.config.configuration import Configuration
from loguru import logger


class TimeConfig(Configuration):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """ """

    @property
    def handler(self):
        _time = TimeHandler()
        _time['live'] = False
        _time['episode'] = uuid.uuid4().hex
        return _time

    def init_required(self, **kwargs):
        self.start: fd.TimeField = kwargs.get("start")
        self.end: fd.TimeField = kwargs.get("end")
        self.steps: fd.StepField = kwargs.get("steps")
        self.lookback = kwargs.get("lookback")

    def init_handler(self, **kwargs):
        pass

    def init_search(self, **kwargs):
        pass
    
    def to_dict(self):
        return {
            "start": self.start.to_epoch(),
            "end": self.end.to_epoch(),
            "steps": self.steps.to_dict(),
            "lookback": self.lookback.to_dict()
        }

    def to_hash(self):
        return consistent_hash(self.to_dict()) 

@logger.catch
def main():
    start = fd.TimeField()
    start.time = "2007-05-02"
    start.timezone = "UTC"


    end = fd.TimeField()
    end.time = "2020-04-02"
    end.timezone = "UTC"

    

    step = fd.StepField()
    step.hours = 10
    # step

    time_conf = TimeConfig(start=start, end=end, steps=step, lookback=step)
    print(time_conf.handler)


if __name__ == "__main__":
    main()