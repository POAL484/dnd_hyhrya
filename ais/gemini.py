###TEXT TO IMAGE MODEL
from g4f.client import Client

import json

from components import abc_model

class GeminiAI(abc_model.AIModel):
    def __init__(self, model: str = "bing"):
        self.model = model
        self.client = Client()
        self.cookie = json.load(open("cfg.json"))['cookie_gemini']

    def generate(self, payload: dict | list, callback: None = None, async_callback: None = None, asyncio_loop: None = None, error_callback: None = None) -> bool:
        async_call = super().generate(payload, callback, async_callback, asyncio_loop, error_callback)
        abc_model.thrd.Thread(target=self.threadedGenerate, args=(payload, callback, async_callback, asyncio_loop, error_callback, async_call)).start()
        return True

    def threadedGenerate(self, payload: dict | list, callback: None = None, async_callback: None = None, asyncio_loop: None = None, error_callback: None = None, async_call: bool = False) -> bool:
        resp = self.client.images.generate(
            model=self.model,
            prompt=payload['prompt'],
        
            #cookies={"__Secure-1PSID": self.cookie}
        )
        if not callback is None:
            callback(resp.data[0].url)
        if async_call:
            abc_model.asyncio.ensure_future(async_callback, loop=asyncio_loop)
        return True