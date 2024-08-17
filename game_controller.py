import flet as ft

import basic_stuff

import ai_apis.LLM as llm
import ai_apis.images as images
import ai_apis.music as music

import time

import utils as u

def nums(item: str | tuple) -> str | list:
    if isinstance(item, tuple):
        return f"{item[1]} x {item[0]}"
    elif 'Набор' in item:
        try:
            kit = list(map(nums, basic_stuff.kits[item]['contents']))
            return kit
        except KeyError: return item
    return item

def unpack_all(inv_list: list) -> list:
    unpacked = []
    for item_or_list in inv_list:
        if isinstance(item_or_list, list):
            unpacked += unpack_all(item_or_list)
            continue
        unpacked.append(item_or_list)
    return unpacked

class Game:
    def __init__(self, page: ft.Page):
        try: page.players
        except AttributeError:
            page.go("/select_players")
            return
        self.page = page
        self.chars = []
        self.llm = llm.LLMAI()
        self.musicAi = music.MusicAI()
        self.images = images.ImagesAI()
        self.messages_count = 0
        self.messages_count_2 = 0

    def createCharFields(self, name: str, race_name: str, class_name: str, base_stats: dict, kit_choices: list, background: str, pers_goal: str):
        try: race = basic_stuff.races_data[race_name]
        except KeyError:
            race = basic_stuff.generic_race
            race_name = basic_stuff.generic_race_name
        try: chr_class = basic_stuff.classes_data[class_name]
        except KeyError:
            chr_class = basic_stuff.generic_class
            class_name = basic_stuff.generic_class_name
        self.chars.append({
            "name": name,
            "race": race_name,
            "class": class_name,
            "attributes": base_stats,
            "speed": race['speed'],
            "languages": race['languages'],
            "features": race['features'],
            "armor_proficiencies": race['armor_proficiencies'] + chr_class['armor_proficiencies'],
            "weapon_proficiencies": race['weapon_proficiencies'] + chr_class['weapon_proficiencies'],
            "skills": chr_class['skills'],
            "hit_points": chr_class['hit_dice'] + ((base_stats['Телосложение'] - 10) // 2),
            "saving_throws": chr_class['saving_throws'],
            "inventory": unpack_all(list(map(nums, kit_choices))) + unpack_all(list(map(nums, chr_class['starting_equipment']['fixed']))),
            "background": background if background else "Нет предыстроии",
            "personal_goal": pers_goal if pers_goal else "Нет личной цели"
        })

    def createCharAi(self):
        self.chars.append("ai")

    def plot_with_ai(self):
        self.plot = "ai"

    def set_plot(self, plot: str):
        self.plot = plot
        
    def _start(self, callback, _, __):
        self.plot = ("""Отлично, приключение готово к началу! Группа героев собралась в деревне Эвердейл, чтобы решить проблему землетрясений, разрушающих мирный уклад жизни жителей. Староста деревни, Маррион Уорлик, проводит с вами встречу на центральной площади деревни, под открытым небом, окруженная стойкими жителями, которые наблюдают за вами с надеждой и тревогой в глазах.

Маррион объясняет: «Темные силы кажется беспокоят дух земли под нашей деревней. Мы верим, что это исходит из заброшенной колокольни на окраине деревни. Многие поколения назад она была местом поклонения, но сейчас это разрушенное место, окутанное тайной и страхом. Пожалуйста, исследуйте колокольню, найдите причину бедствия и, если 
возможно, положите конец этим землетрясениям.»

Маррион предоставляет вам местную карту и прощается, пожелав удачи. Теперь ваша группа должна решить, отправляться ли сразу к колокольне или же провести небольшое исследование, возможно, узнав что-то у местных жителей или осмотреть снаряжение.

**Что герои решат делать дальше?**
- Провести дополнительные разговоры с жителями и поискать информацию о колокольне?
- Посетить местный магазин, чтобы дополнить снаряжение?
- Прямо отправиться к колокольне?

Решение за вами, герои""")

        self.scene = self.plot

        self.img = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-0R8vUcuFmFGVZajgsups3mY8/user-3rNX173bhBPKv3s47XZgTmPL/img-X5rZUkgXi2YAv7PHzUZHDwDf.png?st=2024-08-17T14%3A41%3A39Z&se=2024-08-17T16%3A41%3A39Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-08-17T01%3A45%3A17Z&ske=2024-08-18T01%3A45%3A17Z&sks=b&skv=2024-08-04&sig=9W5NyB9SYMllXgwQ/IyT1ERju7pyQlH83dUKkxjRSeo%3D"
        self.music = "https://audiopipe.suno.ai/?item_id=691ddcac-972b-4825-a12b-99fd4cf1c360"
        self.chars = [{'name': 'Аларика Лунный Ветер', 'race': 'Полуэльф', 'class': 'Жрец', 'attributes': {'Сила': 10, 'Ловкость': 12, 'Телосложение': 12, 'Интеллект': 13, 'Мудрость': 16, 'Харизма': 14}, 'speed': 30, 'languages': ['Общий', 'Эльфийский'], 'features': ['Тёмное зрение', 'Преимущество на спасброски от очарования', 'Не нуждается в сне'], 'armor_proficiencies': ['Лёгкие доспехи', 'Средние доспехи', 'Щиты'], 'weapon_proficiencies': ['Простое оружие'], 'skills': ['Лечение', 'Религия'], 'hit_points': 10, 'saving_throws': ['Мудрость', 'Харизма'], 'inventory': ['Жезл', 'Религиозный символ', 'Путевые одежды'], 'background': 'Аларика выросла в большом городе, но всегда была связана с природой и слушала голоса лесов. Землетрясения в Эвердейл вызвали у неё тревогу и желание понять, как помочь природе и жителям деревни.', 'personal_goal': 'Очистить колокольню от проклятий и восстановить естественный баланс, чтобы землетрясения прекратились.'}, {'name': 'Лирель Сумеречная Песнь', 'race': 'Эльф', 'class': 'Бард', 'attributes': {'Сила': 8, 'Ловкость': 14, 'Телосложение': 12, 'Интеллект': 13, 'Мудрость': 10, 'Харизма': 16}, 'speed': 30, 'languages': ['Общий', 'Эльфийский'], 'features': ['Острое зрение', 'Трехчасовой сон', 'Восприятие магии', 'Скрытность в лесах'], 'armor_proficiencies': ['Легкие доспехи'], 'weapon_proficiencies': ['Длинные мечи', 'Короткие мечи', 'Длинные луки', 'Короткие луки', 'Простое оружие'], 'skills': ['Акробатика', 'Выступление', 'Убеждение', 'Использование магических устройств'], 'hit_points': 10, 'saving_throws': ['Ловкость', 'Харизма'], 'inventory': ['Музыкальный инструмент', 'Дорожный посуд', 'Фляга', 'Кинжал'], 'background': 'Лирель прибыла в Эвердейл случайно, когда искала вдохновения в своих странствиях. Заинтересована в тайнах и легендах местного населения.', 'personal_goal': 'Собрать материал для своей новой эпической баллады о забытом божестве и тайне колокольни, раскрыть причину землетрясений и вмешаться в события, чтобы оставить свой след в истории.'}, {'name': 'Эларион Сумрачный Лист', 'race': 'Эльф', 'class': 'Лучник', 'attributes': {'Сила': 12, 'Ловкость': 18, 'Телосложение': 14, 'Интеллект': 13, 'Мудрость': 16, 'Харизма': 10}, 'speed': 30, 'languages': ['Общий', 'Эльфийский'], 'features': ['Острый слух', 'Тёмное зрение', 'Тренировка с доспехами: легкие', 'Тренировка с оружием: длинные мечи, короткие мечи, длинные луки, короткие луки'], 'armor_proficiencies': ['Лёгкие доспехи'], 'weapon_proficiencies': ['Длинные мечи', 'Короткие мечи', 'Длинные луки', 'Короткие луки'], 'skills': ['Стелс', 'Выживание', 'Внимательность'], 'hit_points': 11, 'saving_throws': ['Ловкость', 'Интеллект'], 'inventory': ['Длинный лук', 'Колчан с стрелами (20)', 'Комплект путешественника', 'Комплект обмундирования лучника'], 'background': 'Эларион родился и вырос в дремучем лесу, но увлекся изучением заброшенных и замкнутых мест. Услышав о колокольне и загадочных землетрясениях в Эвердейл, он не смог удержаться от мысли присоединиться к экспедиции.', 'personal_goal': 'Найти подсказку о забытом боге земли, которому могли поклоняться в колокольне, с целью расширения своих знаний об этой давно потеряной культуре.'}]
        self.chars_info_str = "\n".join([f"Персонаж {i+1}: {character}" for i, character in enumerate(self.chars)])

        self.messages = [
                {"role": "system", "content": "You are the Dungeon Master in a D&D 5e game. You control the world, enemies, and story. Players will interact with you by describing their actions."},
                {"role": "assistant", "content": f"Приключения начинаются! Здесь конечный сценарий игры: {self.plot}. Здесь наши герои: {self.chars_info_str}"},
            ] + [{"role": "assistant", "content": f"Отлично, приключение готово к началу! Группа героев собралась в деревне Эвердейл, чтобы решить проблему землетрясений, разрушающих мирный уклад жизни жителей. Староста деревни, Маррион Уорлик, проводит с вами встречу на центральной площади деревни, под открытым небом, окруженная стойкими жителями, которые наблюдают за вами с надеждой и тревогой в глазах.\n\nМаррион объясняет: «Темные силы кажется беспокоят дух земли под нашей деревней. Мы верим, что это исходит из заброшенной колокольни на окраине деревни. Многие поколения назад она была местом поклонения, но сейчас это разрушенное место, окутанное тайной и страхом. Пожалуйста, исследуйте колокольню, найдите причину бедствия и, если возможно, положите конец этим землетрясениям.»\n\nМаррион предоставляет вам местную карту и прощается, пожелав удачи. Теперь ваша группа должна решить, отправляться ли сразу к колокольне или же провести небольшое исследование, возможно, узнав что-то у местных жителей или осмотреть снаряжение.\n\n**Что герои решат делать дальше?**\n- Провести дополнительные разговоры с жителями и поискать информацию о колокольне?\n- Посетить местный магазин, чтобы дополнить снаряжение?\n- Прямо отправиться к колокольне?\n\nРешение за вами, герои"}]

        callback()

    def start(self, callback: callable, error_callback: callable, status: ft.Text):
        time.sleep(1)

        exit = False

        def error_generated(error_info: str):
            print(f"ERROR! {error_info}")
            error_callback()
            exit = True
        
        def plot_generated(plot: str):
            print(f"Plot generated, tasks: {tasks}")
            status.value = "Сценарий сгенерирован. Идет генерация персонажей..."
            self.plot = plot

            if not "char" in tasks:
                self.chars_info_str = "\n".join([f"Персонаж {i+1}: {character}" for i, character in enumerate(self.chars)])
                self.messages = self.llm.chatWithItInGame(plot=plot, character_info=self.chars_info_str, callback=scene_generated, error_callback=error_generated)
                status.value = "Сценарий сгенерирован. Идет генерация начальной сцены..."
            else:
                for i in range(tasks.count("char")):
                    self.llm.generate_character_with_ai(plot, callback=char_generated, error_callback=error_generated)
            status.update()

        def scene_generated(new_scene: str):
            print(f"Scene generated, tasks: {tasks}")
            status.value = "Сцена сгенерирована. Идет генерация музыки и иллюстрации..."
            status.update()
            print('484848' in new_scene, '525252' in new_scene, '485248' in new_scene)
            self.scene = new_scene.replace('4848484', '').replace('525252', '').replace('485248', '')
            self.messages.append({"role": "assistant", "content": self.scene})
            self.messages_view = [{"role": "assistant", "content": self.scene}]
            
            self.llm.generate_prompt_for_images(new_scene, callback=image_prompt_generated, error_callback=error_generated)
            self.llm.generate_prompt_for_music(new_scene, callback=music_prompt_generated, error_callback=error_generated)

        def char_generated(chr: dict):
            print(f"New char generated, tasks: {tasks}")
            status.value = "Новый персонаж сгенерирован. Идет генерация следующего..."
            self.chars[self.chars.index("ai")] = chr
            tasks.remove("char")
            if not "char" in tasks:
                status.value = "Все персонажи сгенерированны. Идет генерация начальной сцены..."
                self.chars_info_str = "\n".join([f"Персонаж {i+1}: {character}" for i, character in enumerate(self.chars)])
                self.messages = self.llm.chatWithItInGame(plot=self.plot, character_info=self.chars_info_str, callback=scene_generated, error_callback=error_generated)
            status.update()

        def image_prompt_generated(prompt: str):
            print(f"Image prompt generated, tasks: {tasks}")
            print(f"\n\nImage prompt: {prompt}\n\n")
            self.images.generateImage(prompt_en=prompt, callback=image_generated, error_callback=error_generated)

        def music_prompt_generated(prompt: str):
            print(f"Music prompt generated, tasks {tasks}")
            print(f"\n\nMusic prompt: {prompt}\n\n")
            self.musicAi.generate(prompt, make_instrumental=True, callback=music_generated, error_callback=error_generated, return_param=[["audio_url"]])

        def image_generated(url: str):
            print(f"Image generated, tasks: {tasks}")
            status.value = "Иллюстрация сгенерированна. Идет генерация фоновой музыки..."
            if "music" in tasks: status.update()
            self.img = url
            u.image_show(self.img)
            tasks.remove("image")

        def music_generated(url: str):
            print(f"Music generated, tasks: {tasks}")
            status.value = "Музыка сгенерированна. Идет генерация иллюстрации..."
            if "image" in tasks: status.update()
            self.music = url[0]
            print(url)
            u.music_show(self.music)
            tasks.remove("music")

        tasks = ["image", "music"]
        for char in self.chars:
            if char == "ai":
                tasks.append("char")
        
        if self.plot == "ai":
            self.llm.generate_plot_with_ai(callback=plot_generated, error_callback=error_generated)
        else:
            plot_generated(self.plot)

        while tasks and not exit: pass
        if exit: return
        callback()

    def updateMusic(self, update_music: callable):
        def music_prompt_generated(prompt: str):
            print(f"Music prompt generated, ")
            print(f"\n\nMusic prompt: {prompt}\n\n")
            self.musicAi.generate(prompt, make_instrumental=True, callback=music_generated, return_param=[["audio_url"]])

        def music_generated(url: str):
            print(f"Music generated, ")
            self.music = url[0]
            print(url)
            u.music_show(self.music)
            update_music()

        self.llm.generate_prompt_for_music(self.scene, callback=music_prompt_generated)

    def updateImage(self, update_image: callable):
        def image_prompt_generated(prompt: str):
            print(f"Image prompt generated, ")
            print(f"\n\nImage prompt: {prompt}\n\n")
            self.images.generateImage(prompt_en=prompt, callback=image_generated)

        def image_generated(url: str):
            print(f"Image generated, ")
            self.img = url
            u.image_show(self.img)
            update_image()

        self.llm.generate_prompt_for_images(self.scene, callback=image_prompt_generated)

    def packMessages(self):
        def packed(packed_in_one_message: str):
            try:
                self.messages = [self.messages[0]] + [{"user": "assistent", "content": packed_in_one_message}]
                print(f"Packed: {packed_in_one_message}")
            except Exception: pass
        self.llm.packMessages(self.messages[1:], callback=packed)

    def user_input(self, input_val: str, update_chat: callable, update_image: callable, update_music: callable):
        def gptError():
            self.messages_view.append({"role": "err", "content": "Произошла ошибка при обращении к исскуственному интелекту, попробуйте еще раз!"})
            self.messages = self.messages[:-1]
            update_chat()

        def gptAnswered(resp: str):
            if '484848' in resp:
                print("UPDATE MUSIC!")
                #self.updateMusic(update_music)
            if '525252' in resp:
                print("UPDATE IMAGE!")
                #self.updateImage(update_image)
            if '485248' in resp:
                print("UPDATE MUSIC AND IMAGE")
                #self.updateImage(update_image)
                #self.updateMusic(update_music)
            self.messages.append({"role": "assistant", "content": resp.replace('4848484', '').replace('525252', '').replace('485248', '')})
            self.messages_view.append({"role": "assistant", "content": resp.replace('4848484', '').replace('525252', '').replace('485248', '')})
            self.scene = resp.replace('4848484', '').replace('525252', '').replace('485248', '')
            update_chat()

        self.messages.append({"role": "user", "content": input_val})
        self.messages_view.append({"role": "user", "content": input_val})
        update_chat(True)
        self.llm.chatWithItInGame(messages=self.messages, callback=gptAnswered, error_callback=gptError)
        self.messages_count += 1
        self.messages_count_2 += 1
        if self.messages_count == 10:
            self.messages_count = 0
            self.updateImage(update_image)
            self.updateMusic(update_music)
        if self.messages_count_2 == 15:
            self.messages_count_2 = 0
            self.packMessages()