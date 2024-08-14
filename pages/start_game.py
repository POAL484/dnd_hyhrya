import flet as ft

import game_controller

import threading as thrd

def start_game_page(page: ft.Page):
    
    def game_loaded():
        page.go("/game")

    def game_loaded_failed(reason_token_expired: bool = False):
        if reason_token_expired:
            page.go("/tokens_expired_error")
            return
        page.go("/unknown_error")

    page.game = game_controller.Game(page)

    thrd.Thread(target=page.game.start, args=(game_loaded, game_loaded_failed)).start()

    page.add(ft.Container(
        ft.Column([
            ft.Text("Идет первоначальная генерация сцены...", size=45),
            ft.ProgressRing(stroke_width=17, width=250, height=250),
            ft.Text("Немного терпения...", size=23)
        ], ft.MainAxisAlignment.SPACE_EVENLY, ft.CrossAxisAlignment.CENTER), width=page.width, height=page.height
    ))
    