import flet as ft

import game_controller

import threading as thrd

import utils as u

def start_game_page(page: ft.Page):
    
    if u.tryAttr(page, "game"):
        if not u.tryAttr(page.game, "plot"):
            page.go("/write_scene")
            return
    if not u.tryAttr(page, "game"):
        if not u.tryAttr(page, "players"):
            page.go("/select_players")
            return
        page.go("/setup_chars")
        return

    def game_loaded():
        page.go("/game")

    def game_loaded_failed(reason_token_expired: bool = False):
        if reason_token_expired:
            page.go("/tokens_expired_error")
            return
        page.go("/unknown_error")

    status = ft.Text("Идет генерация конечного сценария...", size=23)

    thrd.Thread(target=page.game.start, args=(game_loaded, game_loaded_failed, status)).start()

    page.add(ft.Container(
        ft.Column([
            ft.Text("Идет первоначальная генерация сцены...", size=45),
            ft.ProgressRing(stroke_width=17, width=250, height=250),
            status
        ], ft.MainAxisAlignment.SPACE_EVENLY, ft.CrossAxisAlignment.CENTER), width=page.width, height=page.height
    ))
    