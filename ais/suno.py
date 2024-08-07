### TEXT TO MUSIC MODEL
import requests as req

import time

from components import abc_model

class SunoAI(abc_model.AIModel):
    def __init__(self, port: int|str = 45540):
        self.baseurl = f"http://localhost:{port}/"

    def generate(self, payload: dict, callback: None = None, async_callback: None = None, asyncio_loop: None = None, error_callback: None = None):
        async_call = super().generate(payload=payload, callback=callback, async_callback=async_callback, asyncio_loop=asyncio_loop)
        payloadC = payload.copy()
        payloadC['wait_audio'] = True
        abc_model.thrd.Thread(target=self.threadedGenerate, args=(payloadC, callback, async_callback, asyncio_loop, error_callback, async_call)).start()
        return True
    
    def threadedGenerate(self, payload: dict, callback: None = None, async_callback: None = None, asyncio_loop: None = None, error_callback: None = None, async_call: bool = False):
        resp1 = req.post(self.baseurl+"api/generate", json=payload).json()
        if isinstance(resp1, dict):
            if not error_callback is None:
                error_callback()
                print(f"error while threadedGenerate: {resp1}")
            return False
        time.sleep(5)
        resp = req.get(self.baseurl+f"api/get?ids={resp1[0]['id']}").json()
        if not callback is None:
            callback(resp[0])
        if async_call:
            abc_model.asyncio.ensure_future(async_callback(resp[0]), loop=asyncio_loop)
        return True
