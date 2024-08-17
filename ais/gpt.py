### LLM MODEL
import openai

import json
openai.api_key = json.load(open("cfg.json"))['openai']

from components import abc_model

class GptAI(abc_model.AIModel):
    def __init__(self, model: str = "gpt-4-turbo"):
        self.model = model

    def generate(self, payload: dict | list, callback: None = None, async_callback: None = None, asyncio_loop: None = None, error_callback: None = None) -> bool:
        async_call = super().generate(payload, callback, async_callback, asyncio_loop, error_callback)
        abc_model.thrd.Thread(target=self.threadedGenerate, args=(payload, callback, async_callback, asyncio_loop, error_callback, async_call)).start()
        return True

    def threadedGenerate(self, payload: dict | list, callback: None = None, async_callback: None = None, asyncio_loop: None = None, error_callback: None = None, async_call: bool = False) -> bool:
        try:
            resp = openai.ChatCompletion.create(
                model=self.model,
                messages=payload
            )
            if not callback is None:
                callback(resp.choices[0].message['content'])
            if async_call:
                abc_model.asyncio.ensure_future(async_callback(resp.choices[0].message['content']), loop=asyncio_loop)
            return True
        except Exception as e:
            if not error_callback is None: error_callback(e)
            print(e)