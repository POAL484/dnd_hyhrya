###TEXT TO IMAGE MODEL: GEMINI

import ais.gemini

from translate import Translator

class ImagesAI:
    def __init__(self):
        self.AIClient = ais.gemini.GeminiAI()
        self.translator = Translator(from_lang="ru", to_lang="en")

    def generateImage(self, prompt_ru: str | None = None, prompt_en: str | None = None, callback = None, async_callback = None, asyncio_loop = None, error_callback = None):
        if not prompt_ru and not prompt_en: raise
        if prompt_ru and not prompt_ru is None: prompt = self.translator.translate(prompt_ru)
        if prompt_en and not prompt_en is None: prompt = prompt_en

        self.AIClient.generate({"prompt": prompt}, callback=callback, async_callback=async_callback, asyncio_loop=asyncio_loop, error_callback=error_callback)