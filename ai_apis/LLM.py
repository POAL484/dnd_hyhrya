###LLM: ChatGpt

import ais.gpt



import utils as u

class LLMAI:
    def __init__(self):
        self.AIClient = ais.gpt.GptAI()

    def generate_plot_with_ai(self, callback = None, async_callback = None, asyncio_loop = None, error_callback = None):
        prompt = (
            "Создай сюжет для квеста в стиле Dungeons & Dragons 5e. "
            "Квест должен быть рассчитан на одну игровую сессию(4 часа) и первоуровневых персонажей"
        )
        
        self.AIClient.generate([
                {"role": "system", "content": "You are a creative storyteller."},
                {"role": "user", "content": prompt}
            ], callback=callback, asyncio_loop=asyncio_loop, async_callback=async_callback, error_callback=error_callback)
        
    def extract_json(self, fn: callable, plot: str, error_callback):
        def wrapper_extract_json(msg: str):
            try: eval(msg)
            except Exception:
                self.generate_character_with_ai(plot, fn, error_callback=error_callback)
                return
            fn(eval(msg))
        return wrapper_extract_json
    
    def extract_json_async(self, fn: callable):
        async def wrapper_extract_json_async(msg: str):
            await fn(eval(msg))
        return wrapper_extract_json_async
    
    def generate_character_with_ai(self, plot: str, callback = None, async_callback = None, asyncio_loop = None, error_callback = None):
        prompt = (
            f"Создай персонажа для Dungeons & Dragons 5e, основываясь на следующем сюжете:\n\n{plot}\n\n"
            "Опиши персонажа в формате JSON со следующими ключами:\n"
            "- name: Имя персонажа\n"
            "- race: Раса персонажа\n"
            "- class: Класс персонажа\n"
            "- attributes: Базовые характеристики (Сила, Ловкость, Телосложение, Интеллект, Мудрость, Харизма)\n"
            "- speed: Скорость персонажа, числом, без единицы измерения\n"
            "- languages: Языки, которыми владеет персонаж\n"
            "- features: Особенности и способности расы\n"
            "- armor_proficiencies: Владение доспехами\n"
            "- weapon_proficiencies: Владение оружием\n"
            "- skills: Навыки класса\n"
            "- hit_points: Очки здоровья (вычисляются как сумма хита класса и модификатора Телосложения)\n"
            "- saving_throws: Спасброски класса\n"
            "- inventory: Инвентарь персонажа, перечисляй вещи вот так: \n"
            "- background: Предыстория персонажа, связанная с сюжетом\n"
            "- personal_goal: Личная цель персонажа, основанная на сюжете\n"
            "При генерации ответа не ограждай ответ ```json..```, выведи только ключи\n"
            "Не оставляй никаких заметок, результат должен быть полностью интерпритируемым\n"
            "Все строчные значения должны быть на русском"
        )
        
        self.AIClient.generate([
                {"role": "system", "content": "You are a creative character generator for Dungeons & Dragons."},
                {"role": "user", "content": prompt}
            ], self.extract_json(callback, plot, error_callback) if not callback is None else None,
            self.extract_json_async(callback) if not async_callback is None else None,
            asyncio_loop, error_callback
        )

    def generate_prompt_for_images(self, scene: str, callback = None, async_callback = None, asyncio_loop = None, error_callback = None):
        self.AIClient.generate([
            {"role": "system", "content": "You are skillful prompt writer for the ai image generation"},
            {"role": "user", "content": f"Здесь ситуация, которую тебе нужно описать в запросе: {scene}"}
        ], callback=callback, async_callback=async_callback, asyncio_loop=asyncio_loop, error_callback=error_callback)

    def generate_prompt_for_music(self, scene: str, callback = None, async_callback = None, asyncio_loop = None, error_callback = None):
        self.AIClient.generate([
        {"role": "system", "content": "You are skillful prompt writer for the ai music generation"},
        {"role": "user", "content": f"Здесь ситуация, которую тебе нужно описать в запросе: {scene} \nУложись в ограничение в 250 символов\nМузыка должна быть спокойной, и в средневековом стиле"},
    ], callback=callback, async_callback=async_callback, asyncio_loop=asyncio_loop, error_callback=error_callback)
        
    def chatWithItInGame(self, plot: str | None = None, character_info: str | None = None, messages: list | None = None, callback = None, async_callback = None, asyncio_loop = None, error_callback = None):
        tor = None
        if messages is None:
            messages = [
                {"role": "system", "content": "You are the Dungeon Master in a D&D 5e game. You control the world, enemies, and story. Players will interact with you by describing their actions. Stop at each scene in more detail. Give control over the actions of the players to the user"},
                {"role": "assistant", "content": f"Приключения начинаются! Здесь конечный сценарий игры: {plot}. Здесь наши герои: {character_info}"},
            ]
            tor = messages
        self.AIClient.generate(messages, callback=callback, async_callback=async_callback, asyncio_loop=asyncio_loop, error_callback=error_callback)
        return tor
    
    def packMessages(self, messages: list, callback = None):
        self.AIClient.generate(
            [
                {"role": "system", "content": "You are intended to receive the brief chat of the texts. Chat have roles: assistent and user. The summary should contain no more than three paragraph"},
                {"role": "user", "content": f"Сожми переписку: ```{messages} ```\n\nНе сжимай json информацию"}
            ], callback=callback
        )