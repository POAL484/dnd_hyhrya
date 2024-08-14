###TEXT TO MUSIC: SUNO

import ais.suno

import asyncio

import utils as u

class MusicAI:
    def __init__(self):
        self.AIClient = ais.suno.SunoAI(45540)

    def get_param_sync(self, fn: callable, return_param: list | None = None):
        def wrapper_get_param_sync(resp: dict):
            if not return_param:
                fn(resp)
                return
            r = []
            for param in return_param:
                r.append(u.get_by_keys(resp, param))
            fn(r)
        return wrapper_get_param_sync
    
    def get_param_async(self, fn: callable, return_param: list | None = None):
        async def wrapper_get_param_async(resp: dict):
            if not return_param:
                await fn(resp)
                return
            r = []
            for param in return_param:
                if not isinstance(param, list): param = [param]
                r.append(u.get_by_keys(resp, param))
            await fn(r)
        return wrapper_get_param_async


    def generate(self, prompt: str, make_instrumental: bool = False, models: str = "chirp-v3-5", callback = None, async_callback = None, asyncio_loop = None, error_callback = None, return_param: list = []):
        assert (async_callback is None and asyncio_loop is None) or (not async_callback is None and not asyncio_loop is None)
        self.AIClient.generate({
            "prompt": prompt,
            "make_instrumental": make_instrumental,
            "models": models
        }, self.get_param_sync(callback, return_param) if not callback is None else None,
           self.get_param_async(async_callback, return_param) if not async_callback is None else None,
           asyncio_loop,
           error_callback)