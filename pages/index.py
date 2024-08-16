import flet as ft

import utils as u

def index_page(page: ft.Page):
    def start_game(e: ft.ControlEvent):
        if dd.value == "ns":
            page.open(ft.AlertDialog(content=ft.Container(ft.Text("He выбранно количество игроков!", size=u.calcFontByWidth(page.width/1.5, "Не выбрано количество игроков!"), text_align=ft.TextAlign.CENTER), width=page.width/1.4, height=70, alignment=ft.Alignment(0, 0)), modal=False))
            return
        page.players = int(dd.value)
        page.go("/setup_chars")

    dd = ft.Dropdown("ns", options=[
            ft.dropdown.Option("2", "2 Игрока"),
            ft.dropdown.Option("3", "3 Игрока"),
            ft.dropdown.Option("4", "4 Игрока"),
            ft.dropdown.Option("5", "5 Игроков"),
            ft.dropdown.Option("6", "6 Игроков")
        ], hint_content="Количество игроков")
    
    page.add(ft.Container(
        ft.Column([
            ft.Text("Ого вау днд", size=123),
            ft.Row([
                dd,
                ft.ElevatedButton("Играть! >", on_click=start_game)
            ], ft.MainAxisAlignment.CENTER)
        ], ft.MainAxisAlignment.SPACE_AROUND, ft.CrossAxisAlignment.CENTER), width=page.width, height=page.height
    ))