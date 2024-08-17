import flet as ft

import fast_grid
import utils as u

def game_page(page: ft.Page):

    if u.tryAttr(page, "game"):
        if not u.tryAttr(page.game, "plot"):
            page.go("/write_scene")
            return
        if not u.tryAttr(page.game, "chars") or not u.tryAttr(page.game, "plot") or not u.tryAttr(page.game, "scene") or not u.tryAttr(page.game, "music") or not u.tryAttr(page.game, "img") or not u.tryAttr(page.game, "chars_info_str"):
            page.go("/unknow_error")
            return
    if not u.tryAttr(page, "game"):
        if not u.tryAttr(page, "players"):
            page.go("/select_players")
            return
        page.go("/setup_chars")
        return
    
    def text_submit(e: ft.ControlEvent):
        page.game.user_input(page.textField.value, update_chat, update_image, update_music)
        page.textField.value = ""
        page.update()

    #def mic_clicked(e: ft.ControlEvent):
    #    pass

    def run_aud(e: ft.ControlEvent):
        page.close(page.ddialog)
        if not page.aud_runned: page.aud.play()
        page.aud_runned = True

    #aud_rec = ft.AudioRecorder(ft.AudioEncoder.WAV)
    #page.overlay.append(aud_rec)
    #page.update()
    #aud_rec.has_permission()

    page.aud = ft.Audio(src="temp.mp3", volume=.25, release_mode=ft.audio.ReleaseMode.LOOP)
    page.overlay.append(page.aud)
    page.update()
    page.aud_runned = False

    #page.on_connect = lambda e: aud.play()

    card_width = round( ( page.width - page.height ) / 2)

    players = []

    def gen_dialog_char(e, player: dict):
        player = e.control.player
        def parse_item(item: str | tuple):
            if isinstance(item, tuple):
                return f"{item[0]} x {item[1]}"
            return item
        INFO_KEYS = {
            "name": "Имя",
            "race": "Раса",
            "class": "Класс",
            "attributes": "Характеристики",
            "speed": "Скорость",
            "languages": "Языки",
            "features": "Особенности и способности расы",
            "armor_proficiencies": "Владение доспехами",
            "weapon_proficiencies": "Владение оружием",
            "skills": "Навыки класса",
            "hit_points": "Очки здоровья",
            "saving_throws": "Спасброски",
            "inventory": "Инвентарь",
            "background": "Предыстроия",
            "personal_goal": "Личная цель"
        }
        texts = []
        for info in player.keys():
            if isinstance(player[info], dict):
                texts.append(ft.Text(f"{INFO_KEYS[info] if info in INFO_KEYS.keys() else info}: {u.dump_dict(player[info], ' - ')}"))
                continue
            if isinstance(player[info], list):
                texts.append(ft.Text(f"{INFO_KEYS[info] if info in INFO_KEYS.keys() else info}: {', '.join(list(map(parse_item, player[info]))) if player[info] else 'Нет'}"))
                continue
            texts.append(ft.Text(f"{INFO_KEYS[info] if info in INFO_KEYS.keys() else info}: {player[info]}"))
        page.ddialog = ft.AlertDialog(modal=False, content=ft.Column(texts, scroll='adaptive'), actions=[ft.TextButton("Закрыть", on_click=lambda e: page.close(page.ddialog))])
        page.open(page.ddialog)

    for player in page.game.chars:
        players.append(ft.Container(
            content=ft.Column([
                ft.Text(f"Имя: {player['name']}", size=u.min_value_max(6, u.calcFontByWidth(card_width/1.15, f"Имя: {player['name']}"), 20)),
                ft.Text(f"Раса: {player['race']}", size=u.min_value_max(6, u.calcFontByWidth(card_width/1.55, f"Раса: {player['race']}"), 23)),
                ft.Text(f"Класс: {player['class']}", size=u.min_value_max(6, u.calcFontByWidth(card_width/1.55, f"Класс: {player['class']}"), 23)),
                ft.Text(f"ОЗ: {player['hit_points']}", size=u.min_value_max(6, u.calcFontByWidth(card_width/1.95, f"ОЗ: {player['hit_points']}"), 18)),
                ft.TextButton(content=ft.Text(f"Подробнее об персонаже >", size=u.min_value_max(6, u.calcFontByWidth(card_width/1.55, "Подробнее об персонаже >"), 18), text_align=ft.TextAlign.END), on_click=lambda e: gen_dialog_char(e, player))
            ]),
            bgcolor="#191C20", border_radius=15, width=card_width
        ))
        players[-1].content.controls[-1].player = player
        if len(page.game.chars) % 2 == 0:
            players[-1].height = page.height / (len(page.game.chars) / 2)
        else:
            if len(players) < (len(page.game.chars) / 2)+1:
                players[-1].height = page.height / (((len(page.game.chars)) // 2)+1)
            else:
                players[-1].height = page.height / ((len(page.game.chars)-1) // 2)

    def generateSpansByMessages(messages: list):
        spans = []
        for msg in messages:
            if msg['role'] == "assistant": spans.append(ft.TextSpan("\n"+msg['content']))
            elif msg['role'] == "user": spans.append(ft.TextSpan("\n"+msg['content'], style=ft.TextStyle(color="#A0CAFD")))
            else: spans.append(ft.TextSpan("\n"+msg['content'], style=ft.TextStyle(color="#4ef36c")))
        return spans
    
    def update_chat(loading: bool = False):
        page.chat.spans = generateSpansByMessages(page.game.messages_view)
        if loading:
            page.main.controls[1].controls[1] = ft.Row([ft.ProgressBar(width=page.width, color="#A0CAFD", bgcolor="#272822", scale=5)], alignment=ft.MainAxisAlignment.CENTER, width=page.width)
        else:
            page.main.controls[1].controls[1] = ft.Row([page.textField, page.sendButton], ft.MainAxisAlignment.CENTER, ft.CrossAxisAlignment.END)
        page.update()

    def update_image():
        page.main.controls[0].src = "temp.png"
        page.update()

    def update_music():
        page.aud.release()
        page.aud.src = "temp.mp3"
        page.update()
        page.aud.play()

    print(page.game.img, page.game.music, page.game.scene, page.game.chars_info_str)

    page.players_left = ft.Column(players[:len(players)//2] if len(players) % 2 == 0 else players[:(len(players)+1)//2], width=card_width, spacing=0, alignment=ft.MainAxisAlignment.CENTER)
    page.players_right = ft.Column(players[len(players)//2:] if len(players) % 2 == 0 else players[((len(players)+1)//2):], width=card_width, spacing=0, alignment=ft.MainAxisAlignment.CENTER)
    page.textField = ft.TextField(width=fast_grid.Grid(10, 1)(page.height, 10), on_submit=text_submit, keyboard_type=ft.KeyboardType.MULTILINE, multiline=True)
    page.sendButton = ft.IconButton(ft.icons.SEND_ROUNDED, on_click=text_submit, width=fast_grid.Grid(10, 1)(page.height, 1), height=fast_grid.Grid(10, 1)(page.height, 1))
    page.chat = ft.Text(spans=generateSpansByMessages(page.game.messages_view))
    page.main = ft.Stack([
        ft.Image(src="temp.png", opacity=.3, width=page.height, height=page.height),
        ft.Column([
            ft.Container(page.chat),
            ft.Row([page.textField, page.sendButton], ft.MainAxisAlignment.CENTER, ft.CrossAxisAlignment.END)
        ], scroll='adaptive')
    ], width=page.height, height=page.height-10, alignment=ft.Alignment(0, 1))
    page.add(ft.Row([page.players_left, page.main, page.players_right], spacing=0, alignment=ft.MainAxisAlignment.END))
    page.ddialog = ft.AlertDialog(modal=False, title=ft.Text("Игра готова!"), actions=[ft.TextButton("Вперед! >", on_click=run_aud)], on_dismiss=run_aud)
    page.open(page.ddialog)