#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from time import time
from functools import wraps
from typing  import Callable, Any
from asyncio import (
    set_event_loop_policy, WindowsSelectorEventLoopPolicy
)

from utils.log import LOGGING_CONFIG


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('pg_poll')


def patch_event_loop_policy():
    ''' Patch for Win NameResolver issue
    '''
    if os.name == 'nt':
        set_event_loop_policy(WindowsSelectorEventLoopPolicy())


def print_runtime_statistics(name: str, function: Callable) -> None:
    '''Prints runtime statistic attributes for function parameter
    '''
    summary = 'TOTAL EXECUTION TIME' if name == 'Main' else 'synchronous duration'

    print( '=' * 80, '\n',
          f'[{name}] '
          f' total calls: {function.calls}, '
          f' longest call: {round(function.max, 2)}, '
          f' {summary}: {round(function.total, 2)}'
        )


def stats_collector(function: Callable) -> Callable:
    '''Collects runtime statistic for decorated functions
    '''
    @wraps(function)
    async def collected(instance, *args, **kwargs) -> Any:

        logger.debug(f'Starting {function} with args: {args} {kwargs}')
        start = time()

        try:
            return await function(instance, *args, **kwargs)
        finally:
            duration = time() - start
            logger.debug(f'Finished {function} in {duration:.4f} second(s)')

            collected.calls += 1
            collected.total += duration

            if duration > collected.max:
                collected.max = duration

            if function.__name__ == 'make_query':
            # if durate: 
                collected.durations[instance._db_name] = duration

    collected.calls = collected.total = collected.max = 0
    collected.durations = {}

    return collected

    
class TtlCache():

    def __init__(self, function: Callable):
        self.cached = function
        # update_wrapper(self, cached)
        self.past = time()
        self.cache = {}
   
    
    async def __call__(self, *args, **kwargs) -> Any:  
        logger.debug(f'Starting {self.cached} with args: {args} {kwargs}')
        key = str(args) + str(kwargs)
        now = time()
        if (now - self.past < 60) and key in self.cache:
            logger.debug(f'Finished {self.cached} <= cache')
            return self.cache[key]
        else:
            try:
                result = await self.cached(*args, **kwargs)
                self.past = time()
                self.cache[key] = result
                return result
            finally:
                logger.debug(f'Finished {self.cached} => cache')
