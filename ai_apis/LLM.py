###LLM: ChatGpt

import ais.gpt



import utils as u

class LLMAI:
    def __init__(self):
        self.AIClient = ais.gpt.GptAI()

    def generate_plot_with_ai(self, callback, async_callback, asyncio_loop, error_callback):
        prompt = (
            "Создай сюжет для квеста в стиле Dungeons & Dragons 5e. "
            "Квест должен быть рассчитан на одну игровую сессию(4 часа) и первоуровневых персонажей"
        )
        
        self.AIClient.generate(messages=[
                {"role": "system", "content": "You are a creative storyteller."},
                {"role": "user", "content": prompt}
            ], callback=callback, asyncio_loop=asyncio_loop, async_callback=async_callback, error_callback=error_callback)
        
    def extract_json(self, fn: callable):
        def wrapper_extract_json(msg: str):
            fn(eval(msg))
        return wrapper_extract_json
    
    def extract_json_async(self, fn: callable):
        async def wrapper_extract_json_async(msg: str):
            await fn(eval(msg))
        return wrapper_extract_json_async
    
    def generate_character_with_ai(self, plot, callback, async_callback, asyncio_loop, error_callback):
        prompt = (
            f"Создай персонажа для Dungeons & Dragons 5e, основываясь на следующем сюжете:\n\n{plot}\n\n"
            "Опиши персонажа в формате JSON со следующими ключами:\n"
            "- name: Имя персонажа\n"
            "- race: Раса персонажа\n"
            "- class: Класс персонажа\n"
            "- attributes: Базовые характеристики (Сила, Ловкость, Телосложение, Интеллект, Мудрость, Харизма)\n"
            "- speed: Скорость персонажа\n"
            "- languages: Языки, которыми владеет персонаж\n"
            "- features: Особенности и способности расы\n"
            "- armor_proficiencies: Владение доспехами\n"
            "- weapon_proficiencies: Владение оружием\n"
            "- skills: Навыки класса\n"
            "- hit_points: Очки здоровья (вычисляются как сумма хита класса и модификатора Телосложения)\n"
            "- saving_throws: Спасброски класса\n"
            "- inventory: Инвентарь персонажа, перечисляй вещи вот так: \n"
            "- background: Предыстория персонажа, связанная с сюжетом\n"
            "- personal_goal: Личная цель персонажа, основанная на сюжете"
        )
        
        self.AIClient.generate([
                {"role": "system", "content": "You are a creative character generator for Dungeons & Dragons."},
                {"role": "user", "content": prompt}
            ], self.extract_json(callback) if not callback is None else None,
            self.extract_json_async(callback) if not async_callback is None else None,
            asyncio_loop, error_callback
        )