import flet as ft

import utils as u
import fast_grid

def select_players_page(page: ft.Page):
    def change_players(players: int, e: ft.ControlEvent):
        page.players = players
        pl2.bgcolor = "#111418"
        pl3.bgcolor = "#111418"
        pl4.bgcolor = "#111418"
        pl5.bgcolor = "#111418"
        pl6.bgcolor = "#111418"
        e.control.bgcolor = "#2C3239"
        page.update()

    def start_game(e: ft.ControlEvent):
        try:
            page.players
        except AttributeError:
            page.open(ft.AlertDialog(content=ft.Container(ft.Text("He выбранно количество игроков!", size=u.calcFontByWidth(page.width/1.5, "Не выбрано количество игроков!"), text_align=ft.TextAlign.CENTER), width=page.width/1.4, height=70, alignment=ft.Alignment(0, 0)), modal=False))
            return
        page.go("/start_game")

    pl2 = ft.Container(ft.Text("2 Игрока", size=34), on_click=lambda e: change_players(2, e), width=fast_grid.Grid(1, 2, 1)(page.width, 2), padding=15, border_radius=5)
    pl3 = ft.Container(ft.Text("3 Игрока", size=34), on_click=lambda e: change_players(3, e), width=fast_grid.Grid(1, 2, 1)(page.width, 2), padding=15, border_radius=5)
    pl4 = ft.Container(ft.Text("4 Игрока", size=34), on_click=lambda e: change_players(4, e), width=fast_grid.Grid(1, 2, 1)(page.width, 2), padding=15, border_radius=5)
    pl5 = ft.Container(ft.Text("5 Игрока", size=34), on_click=lambda e: change_players(5, e), width=fast_grid.Grid(1, 2, 1)(page.width, 2), padding=15, border_radius=5)
    pl6 = ft.Container(ft.Text("6 Игрока", size=34), on_click=lambda e: change_players(6, e), width=fast_grid.Grid(1, 2, 1)(page.width, 2), padding=15, border_radius=5)

    page.add(ft.Container(ft.Column([
        pl2, pl3, pl4, pl5, pl6,
        ft.Row([ft.ElevatedButton(content=ft.Text("Начать игру!", size=34), on_click=start_game)], ft.MainAxisAlignment.END, width=fast_grid.Grid(1, 2, 1)(page.width, 2))
    ], ft.MainAxisAlignment.CENTER, ft.CrossAxisAlignment.CENTER), width=page.width, height=page.height))