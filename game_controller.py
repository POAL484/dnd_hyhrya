import flet as ft

import basic_stuff

import ai_apis.LLM as llm

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
            "languages": race['langueges'],
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

    def createCharAI(self):
        self.chars.append("ai")
        
    def start(self, callback: callable, error_callback: callable):
        self.img = "https://kappa.lol/cio8N"
        self.info_players = []
        for i in range(self.page.players):
            self.info_players.append({"name": f"Имя {i+1}", "info": f"Еще что нибудь {i+1}"})
        callback()