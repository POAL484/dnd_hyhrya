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
            'weapon_proficiencies': "Навыки во владении с оружием",
            'langueges': "Языки"
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
                    texts.append(ft.Text(f"\t\t\t\tЭкипировка на выбор: Нет"))
                else:
                    texts.append(ft.Text("\t\t\t\tЭкипировка на выбор:"))
                    for ch in class_[info]["choices"]:
                        ch1 = []
                        for ch11 in ch:
                            ch1.append(', '.join(map(parse_item, ch11)))
                        texts.append(ft.Text(f"\t\t\t\t\t\t\t\t{'  ИЛИ  '.join(ch1)}"))
                if not class_[info]["fixed"]:
                    texts.append(ft.Text(f"\t\t\t\tФиксированная экипировка: Нет"))
                else:
                    texts.append(ft.Text(f"\t\t\t\tФиксированная экипировка: {', '.join(map(parse_item, class_[info]['fixed']))}"))
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
        if u.tryAttr(page, "kit_info"): page.__delattr__("kit_info")

    def check_every_value_more(than: int, l: list) -> bool:
        for i in l:
            if int(i) > than: return False
        return True

    def get_value_for_map(tf: ft.TextField):
        if not tf.value: return 0
        return int(tf.value)
    
    def update_stats_errors(e: ft.ControlEvent):
        try:
            int(e.control.value)
        except Exception:
            e.control.value = e.control.value[:-1]
            e.control.update()
            return
        page.dialog_1_fields["stats_errors"].controls[0].color = "#bb2121" if not check_every_value_more(17, map(get_value_for_map, page.dialog_1_fields["stats"].values())) else None
        page.dialog_1_fields["stats_errors"].controls[1].color = "#bb2121" if sum(map(get_value_for_map, page.dialog_1_fields["stats"].values())) > 70 else None
        page.dialog_1_fields["stats_errors"].controls[1].value = f"Сумма статистик не должна быть больше 70. Текущая сумма: {sum(map(get_value_for_map, page.dialog_1_fields["stats"].values()))}"
        page.update()

    def dialog_ai_continue(e: ft.ControlEvent | None):
        page.game.createCharAi()
        page.close(page.ddialog)
        page.n_char += 1
        page.ttitle.value = f"Игрок {page.n_char}, время создавать персонажа!"
        page.ttitle.update()
        if page.n_char > page.players:
            page.go("/write_scene")

    def ai_char():
        page.game.createCharAi()
        page.n_char += 1
        page.ttitle.value = f"Игрок {page.n_char}, время создавать персонажа!"
        page.ttitle.update()
        if page.n_char > page.players:
            page.go("/write_scene")

    def go_to_dialog_2(e: ft.ControlEvent):
        if page.dialog_1_fields["class"].value == "ns":
            page.close(page.ddialog)
            page.open(ft.AlertDialog(content=ft.Container(ft.Text("Для продолжения выбери как минимум класс!", size=u.calcFontByWidth(page.width/1.5, "Для продолжения выбери как минимум класс!"), text_align=ft.TextAlign.CENTER), width=page.width/1.4, height=70, alignment=ft.Alignment(0, 0)), modal=False, on_dismiss=lambda e: page.open(page.ddialog)))
            return
        page.close(page.ddialog)
        if u.tryAttr(page, "kit_info"):
            page.open(gen_dialog_2(page.kit_info))
            return
        page.open(gen_dialog_2())

    def gen_dialog(name: str = "",
                   race_key: str = "ns",
                   class_key: str = "ns",
                   base_stats: dict = u.rightDictGen(basic_stuff.base_stats, [0] * len(basic_stuff.base_stats)),
                   background: str = "",
                   pers_goal: str = "") -> ft.AlertDialog:
        stats = {}
        app_row = ft.Row([], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        for stat in base_stats.keys():
            stats[stat] = ft.TextField(base_stats[stat], label=stat, width=(fast_grid.Grid(len(base_stats.keys()))(page.width/1.025, 1))-(10*(len(base_stats.keys())-1)), on_change=update_stats_errors, keyboard_type=ft.KeyboardType.NUMBER)
            app_row.controls.append(stats[stat])
        page.dialog_1_fields = {
            "name": ft.TextField(name, label="Имя персонажа"),
            "race": ft.Dropdown(race_key, u.generateDropdownOptionsKeysEqualValues(basic_stuff.races_data.keys()), label="Раса", on_change=update_info_race),
            "race_info": ft.Column(get_info_about_race(race_key), spacing=2),
            "class": ft.Dropdown(class_key, u.generateDropdownOptionsKeysEqualValues(basic_stuff.classes_data.keys()), label="Класс", on_change=update_info_class),
            "class_info": ft.Column(get_info_about_class(class_key), spacing=2),
            "stats": stats,
            "stats_errors": ft.Row([ ft.Text("Каждая статистика не должна быть больше 17", color="#bb2121" if not check_every_value_more(17, base_stats.values()) else None), ft.Text(f"Сумма статистик не должна быть больше 70. Текущая сумма: {sum(base_stats.values())}", color="#bb2121" if sum(base_stats.values()) > 70 else None) ]),
            "background": ft.TextField(background, label="Предыстория (необязательно)", multiline=True),
            "pers_goal": ft.TextField(pers_goal, label="Личная цель (необязательно)", multiline=True)
        }
        page.ddialog = ft.AlertDialog(
            modal=True, title=ft.Text("Создание персонажа: лист 1"),
            content=ft.Container(
                ft.Column([
                    page.dialog_1_fields['name'],
                    page.dialog_1_fields['race'],
                    page.dialog_1_fields['race_info'],
                    page.dialog_1_fields['class'],
                    page.dialog_1_fields['class_info'],
                    app_row,
                    page.dialog_1_fields["stats_errors"],
                    page.dialog_1_fields['background'],
                    page.dialog_1_fields['pers_goal']
                ], scroll='adaptive'),
                width=page.width,
                height=page.height,
            ),
            actions=[
                ft.TextButton("Сгенерировать нейросетью", on_click=dialog_ai_continue),
                ft.TextButton("Далее", on_click=go_to_dialog_2)
            ]
        )
        return page.ddialog
    
    def change_kit(e: ft.ControlEvent, i: int, j: int):
        def parse_item(item: str | tuple):
            if isinstance(item, tuple):
                return f"{item[0]} x {item[1]}"
            return item
        page.kit_info[e.control.i] = e.control.j # https://i.supa.codes/i4-YR (баг фреймворка)
        if 'Набор' in e.control.text:
            for findNabor in e.control.text.split(", "):
                if 'Набор' in findNabor and findNabor in basic_stuff.kits.keys():
                    page.kit_info_rows[-1].value = ', '.join(map(parse_item, basic_stuff.kits[findNabor]['contents']))
        for btn in page.kit_info_rows[e.control.i].controls:
            btn.color = "#3fd565" if page.kit_info[e.control.i] == btn.j else "#A0CAFD"
        page.update()

    def return_dialog_1(e: ft.ControlEvent | None):
        page.close(page.ddialog)
        page.open(gen_dialog(page.dialog_1_fields['name'].value,
                             page.dialog_1_fields['race'].value,
                             page.dialog_1_fields['class'].value,
                             u.rightDictGen(basic_stuff.base_stats, list(map(get_value_for_map, page.dialog_1_fields['stats'].values()))),
                             page.dialog_1_fields['background'].value,
                             page.dialog_1_fields['pers_goal'].value))
        
    def submit_char(e: ft.ControlEvent | None):
        def inventoryReadyToSubmit() -> list:
            chc = basic_stuff.classes_data[page.dialog_1_fields['class'].value]['starting_equipment']['choices']
            inv = []
            for i in range(len(page.kit_info)):
                inv += chc[i][page.kit_info[i]]
            return inv
        page.close(page.ddialog)
        fields = []
        if not page.dialog_1_fields['name'].value: fields += ['имени']
        if page.dialog_1_fields['race'].value == "ns": fields += ['расы']
        if page.dialog_1_fields['class'].value == "ns": fields += ['класса']
        if -1 in page.kit_info: fields += ['не выбрано все снаряжение']
        if not check_every_value_more(17, map(get_value_for_map, page.dialog_1_fields["stats"].values())) or sum(map(get_value_for_map, page.dialog_1_fields["stats"].values())) > 70: fields += ["ошибки при заполнении характеристик"]
        if fields:
            page.open(ft.AlertDialog(content=ft.Container(ft.Text(f"Персонаж не имеет: {', '.join(fields)}. Проверьте эти поля", size=u.calcFontByWidth(page.width/1.5, f"Персонаж не имеет: {', '.join(fields)}. Заполните эти поля"), text_align=ft.TextAlign.CENTER), width=page.width/1.4, height=70, alignment=ft.Alignment(0, 0)), modal=False, on_dismiss=lambda e: page.open(page.ddialog)))
            return
        page.game.createCharFields(
            page.dialog_1_fields['name'].value,
            page.dialog_1_fields['race'].value,
            page.dialog_1_fields['class'].value,
            u.rightDictGen(basic_stuff.base_stats, list(map(get_value_for_map, page.dialog_1_fields['stats'].values()))),
            inventoryReadyToSubmit(),
            page.dialog_1_fields['background'].value,
            page.dialog_1_fields['pers_goal'].value
        )
        page.n_char += 1
        page.ttitle.value = f"Игрок {page.n_char}, время создавать персонажа!"
        page.ttitle.update()
        if page.n_char > page.players:
            page.go("/write_scene")
    
    def gen_dialog_2(kit_info: list | None = None):
        def parse_item(item: str | tuple):
            if isinstance(item, tuple):
                return f"{item[0]} x {item[1]}"
            return item
        if kit_info is None: kit_info = [-1] * len(basic_stuff.classes_data[page.dialog_1_fields['class'].value]['starting_equipment']['choices'])
        chc = basic_stuff.classes_data[page.dialog_1_fields['class'].value]['starting_equipment']['choices']
        page.kit_info = kit_info
        page.kit_info_rows = []
        for i in range(len(chc)):
            row = ft.Row([], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            for j in range(len(chc[i])):
                row.controls.append(ft.ElevatedButton(', '.join(list(map(parse_item, chc[i][j]))), color="#3fd565" if kit_info[i] == j else "#A0CAFD",
                                                      width=fast_grid.Grid(len(chc[i]))(page.width/1.5, 1), on_click=lambda e: change_kit(e, i, j)))
                row.controls[-1].i = i # https://i.supa.codes/i4-YR (баг фреймворка)
                row.controls[-1].j = j
            if len(row.controls) == 1: row.alignment = ft.MainAxisAlignment.CENTER
            page.kit_info_rows.append(row)
        page.kit_info_rows.append(ft.Text("Выберите опцию-набор для просмотра содержимого набора"))
        page.ddialog = ft.AlertDialog(
            modal=True, title=ft.Text("Создание персонажа: лист 2"),
            content=ft.Container(
                ft.Column([ft.Text(f"Фиксированное снаряжение: {', '.join(map(parse_item, basic_stuff.classes_data[page.dialog_1_fields['class'].value]['starting_equipment']['fixed'])) if basic_stuff.classes_data[page.dialog_1_fields['class'].value]['starting_equipment']['fixed'] else 'Нет'}")] + page.kit_info_rows, scroll='adaptive'),
                width=page.width,
                height=page.height,
            ),
            actions=[
                ft.TextButton("Назад", on_click=return_dialog_1),
                ft.TextButton("Создать персонажа", on_click=submit_char)
            ]
        )
        return page.ddialog

    if not u.tryAttr(page, "players"):
        page.go("/select_players")
        return
    page.game = game_controller.Game(page)
    page.n_char = 1
    page.ttitle = ft.Text(f"Игрок {page.n_char}, время создавать персонажа!", text_align=ft.TextAlign.CENTER, width=page.width, size=56)
    page.add(page.ttitle, ft.Row([
        ft.ElevatedButton(content=ft.Column([ft.Icon(ft.icons.SMART_TOY, size=page.width/3), ft.Text("Создать персонажа нейросетью", size=23, text_align=ft.TextAlign.CENTER, width=page.width/3)], ft.MainAxisAlignment.CENTER), width=page.width/2.5, height=page.width/2.5, on_click=lambda _: ai_char()),
        ft.ElevatedButton(content=ft.Column([ft.Icon(ft.icons.EDIT, size=page.width/3), ft.Text("Создание собственного персонажа", size=23, text_align=ft.TextAlign.CENTER, width=page.width/3)], ft.MainAxisAlignment.CENTER), width=page.width/2.5, height=page.width/2.5, on_click=lambda _: page.open(gen_dialog()))
    ], ft.MainAxisAlignment.SPACE_AROUND))