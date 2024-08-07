import abc

import threading as thrd
import asyncio

class AIModel(abc.ABC):

    @abc.abstractmethod
    def generate(self, payload: dict, callback: None = None, async_callback: None = None, asyncio_loop: None = None, error_callback: None = None) -> bool:
        async_call = False
        if ( not async_callback is None ) or ( not asyncio_loop is None ):
            if not ( not async_callback is None and not asyncio_loop is None):
                raise "He достаточно аргументов: async_callback и asyncio_loop должны быть переданы вместе"
            async_call = True
        return async_call
    
    @abc.abstractmethod
    def threadedGenerate(self, payload: dict, callback: None = None, async_callback: None = None, asyncio_loop: None = None, error_callback: None = None, async_call: bool = False) -> bool:
        pass