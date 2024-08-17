###TEXT TO IMAGE MODEL
import openai

import json

openai.api_key = json.load(open("cfg.json"))['openai']

from components import abc_model

class GeminiAI(abc_model.AIModel):
    def __init__(self):
        pass

    def generate(self, payload: dict | list, callback: None = None, async_callback: None = None, asyncio_loop: None = None, error_callback: None = None) -> bool:
        async_call = super().generate(payload, callback, async_callback, asyncio_loop, error_callback)
        abc_model.thrd.Thread(target=self.threadedGenerate, args=(payload, callback, async_callback, asyncio_loop, error_callback, async_call)).start()
        return True

    def threadedGenerate(self, payload: dict | list, callback: None = None, async_callback: None = None, asyncio_loop: None = None, error_callback: None = None, async_call: bool = False) -> bool:
        try: 
            resp = openai.Image.create(
                model="dall-e-3",
                quality="standard",
                prompt=payload['prompt'],
                n=1,
                size="1024x1024"
            )
            if not callback is None:
                callback(resp["data"][0]["url"])
            if async_call:
                abc_model.asyncio.ensure_future(async_callback(resp["data"][0]["url"]), loop=asyncio_loop)
            return True
        except Exception as e:
            if not error_callback is None: error_callback(e)
            print(e)