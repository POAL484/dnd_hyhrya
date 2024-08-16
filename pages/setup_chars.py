import flet as ft

import game_controller

import basic_stuff

import utils as u
import fast_grid

def setup_chars_page(page: ft.Page):

    def get_info_about_race(race_key: str) -> list:
        INFO_KEYS = {
            'ability_bonuses': "Бонусы к характеристикам",
            'speed': "Скорость",
            'langueges': "Языки",
            'features': "Особенности",
            'tool_proficiencies': "Ремесленные навыки",
            'armor_proficiencies': "Предпочтения в броне",
            'weapon_proficiencies': "Навыки во владении с оружием"
        }
        if race_key == "ns": return [ft.Text("Выберите расу для просмтора информации")]
        try: race = basic_stuff.races_data[race_key]
        except KeyError: return [ft.Text("Нет информации об этой расе")]
        texts = [ft.Text(f"Раса {race_key}:")]
        for info in race.keys():
            if isinstance(race[info], dict):
                texts.append(ft.Text(f"{INFO_KEYS[info] if info in INFO_KEYS.keys() else info}: {u.dump_dict(race[info], ' - ')}"))
                continue
            if isinstance(race[info], list):
                texts.append(ft.Text(f"{INFO_KEYS[info] if info in INFO_KEYS.keys() else info}: {', '.join(race[info]) if race[info] else 'Нет'}"))
                continue
            texts.append(ft.Text(f"{INFO_KEYS[info] if info in INFO_KEYS.keys() else info}: {race[info]}"))
        return texts
    
    def get_info_about_class(class_key: str) -> list:
        def parse_item(item: str | tuple):
            if isinstance(item, tuple):
                return f"{item[0]} x {item[1]}"
            return item
        INFO_KEYS = {
            'tool_proficiencies': "Ремесленные навыки",
            'armor_proficiencies': "Предпочтения в броне",
            'weapon_proficiencies': "Навыки во владении с оружием",
            'hit_dice': "Очки здоровья",
            'hit_increase': "Влияние уровня на очки здоровья",
            'saving_throws': "Спасброски",
            'skills': "Навыки"
        }
        if class_key == "ns": return [ft.Text("Выберите класс для просмтора информации")]
        try: class_ = basic_stuff.classes_data[class_key]
        except KeyError: return [ft.Text("Нет информации об этом классе")]
        texts = [ft.Text(f"Класс {class_key}:")]
        for info in class_.keys():
            if info == "starting_equipment":
                texts.append(ft.Text("Начальная экипировка:"))
                if not class_[info]["choices"]:
                    texts.append(ft.Text(f"\tЭкипировка на выбор: Нет"))
                else:
                    texts.append(ft.Text("\tЭкипировка на выбор:"))
                    for ch in class_[info]["choices"]:
                        ch1 = []
                        for ch11 in ch:
                            ch1.append(', '.join(map(parse_item, ch11)))
                        texts.append(ft.Text(f"\t\t{'  ИЛИ  '.join(ch1)}"))
                if not class_[info]["fixed"]:
                    texts.append(ft.Text(f"\tФиксированная экипировка: Нет"))
                else:
                    texts.append(ft.Text(f"\tФиксированная экипировка: {', '.join(map(parse_item, class_[info]['fixed']))}"))
                continue
            if isinstance(class_[info], dict):
                texts.append(ft.Text(f"{INFO_KEYS[info] if info in INFO_KEYS.keys() else info}: {u.dump_dict(class_[info], ' - ')}"))
                continue
            if isinstance(class_[info], list):
                texts.append(ft.Text(f"{INFO_KEYS[info] if info in INFO_KEYS.keys() else info}: {', '.join(class_[info]) if class_[info] else 'Нет'}"))
                continue
            texts.append(ft.Text(f"{INFO_KEYS[info] if info in INFO_KEYS.keys() else info}: {class_[info]}"))
        return texts

    def update_info_race(e: ft.ControlEvent):
        page.dialog_1_fields["race_info"].controls = get_info_about_race(
            page.dialog_1_fields["race"].value
        )
        page.update()

    def update_info_class(e: ft.ControlEvent):
        page.dialog_1_fields["class_info"].controls = get_info_about_class(
            page.dialog_1_fields["class"].value
        )
        page.update()

    def gen_dialog(name: str = "",
                   race_key: str = "ns",
                   class_key: str = "ns",
                   base_stats: dict = u.rightDictGen(basic_stuff.base_stats, [0] * len(basic_stuff.base_stats)),
                   background: str = "",
                   pers_goal: str = "") -> ft.AlertDialog:
        stats = {}
        app_row = ft.Row()
        for stat in base_stats.keys():
            stats[stat] = ft.TextField(base_stats[stat], label=stat, width=(fast_grid.Grid(len(base_stats.keys()))(page.width/1.1, 1))-(10*len(base_stats.keys())))
            app_row.controls.append(stats[stat])
        page.dialog_1_fields = {
            "name": ft.TextField(name, label="Имя персонажа"),
            "race": ft.Dropdown(race_key, u.generateDropdownOptionsKeysEqualValues(basic_stuff.races_data.keys()), label="Раса", on_change=update_info_race),
            "race_info": ft.Column(get_info_about_race(race_key), spacing=2),
            "class": ft.Dropdown(class_key, u.generateDropdownOptionsKeysEqualValues(basic_stuff.classes_data.keys()), label="Класс", on_change=update_info_class),
            "class_info": ft.Column(get_info_about_class(class_key), spacing=2),
            "stats": stats,
            "background": ft.TextField(background, label="Предыстория (необязательно)", multiline=True),
            "pers_goal": ft.TextField(pers_goal, label="Личная цель (необязательно)", multiline=True)
        }
        return ft.AlertDialog(
            modal=True, title=ft.Text("Создание персонажа: лист 1"),
            content=ft.Container(
                ft.Column([
                    page.dialog_1_fields['name'],
                    page.dialog_1_fields['race'],
                    page.dialog_1_fields['race_info'],
                    page.dialog_1_fields['class'],
                    page.dialog_1_fields['class_info'],
                    app_row,
                    page.dialog_1_fields['background'],
                    page.dialog_1_fields['pers_goal']
                ], scroll='adaptive'),
                width=page.width,
                height=page.height,
            ),
            actions=[
                ft.TextButton("123")
            ]
        )

    if not u.tryAttr(page, "players"):
        page.go("/select_players")
        return
    page.game = game_controller.Game(page)
    page.n_char = 1
    page.add(ft.TextButton("123", on_click=lambda e: page.open(gen_dialog())))