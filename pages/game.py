import flet as ft

import fast_grid
import utils as u

def game_page(page: ft.Page):
    
    def text_submit(e: ft.ControlEvent):
        pass

    def mic_clicked(e: ft.ControlEvent):
        pass

    #aud_rec = ft.AudioRecorder(ft.AudioEncoder.WAV)
    #page.overlay.append(aud_rec)
    #page.update()
    #aud_rec.has_permission()

    card_width = round( ( page.width - page.height ) / 2)

    players = []

    for player in page.game.info_players:
        players.append(ft.Container(
            content=ft.Column([
                ft.Text(player['name'], size=u.calcFontByWidth(card_width/1.25, player['name'])),
                ft.Text(player['info'], size=u.calcFontByWidth(card_width/1.55, player['info']))
            ]),
            bgcolor="#191C20", border_radius=15
        ))
        if len(page.game.info_players) % 2 == 0:
            players[-1].height = page.height / (len(page.game.info_players) / 2)
        else:
            if len(players) < (len(page.game.info_players) / 2)+1:
                players[-1].height = page.height / (((len(page.game.info_players)) // 2)+1)
            else:
                players[-1].height = page.height / ((len(page.game.info_players)-1) // 2)

    players_left = ft.Column(players[:len(players)//2] if len(players) % 2 == 0 else players[:(len(players)+1)//2], width=card_width, spacing=0, alignment=ft.MainAxisAlignment.CENTER)
    players_right = ft.Column(players[len(players)//2:] if len(players) % 2 == 0 else players[((len(players)+1)//2):], width=card_width, spacing=0, alignment=ft.MainAxisAlignment.CENTER)
    textField = ft.TextField(width=fast_grid.Grid(10, 1, 1)(page.height, 10), on_submit=text_submit, keyboard_type=ft.KeyboardType.MULTILINE, multiline=True)
    micButton = ft.IconButton(ft.icons.MIC_ROUNDED, icon_color=ft.colors.RED, on_click=mic_clicked, width=fast_grid.Grid(10, 1, 1)(page.height, 1), height=fast_grid.Grid(10, 1, 1)(page.height, 1))
    sendButton = ft.IconButton(ft.icons.SEND_ROUNDED, on_click=text_submit, width=fast_grid.Grid(10, 1, 1)(page.height, 1), height=fast_grid.Grid(10, 1, 1)(page.height, 1))
    main = ft.Stack([
        ft.Image(page.game.img, opacity=.5, width=page.height, height=page.height),
        ft.Row([textField, sendButton, micButton], ft.MainAxisAlignment.CENTER, ft.CrossAxisAlignment.END)
    ], width=page.height, height=page.height-10, alignment=ft.Alignment(0, 1))
    page.add(ft.Row([players_left, main, players_right], spacing=0, alignment=ft.MainAxisAlignment.END))