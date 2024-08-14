import flet as ft

import utils as u

def p404_page(page: ft.Page):

    page.add(
        ft.Container(ft.Text("Ошибка 404", size=u.calcFontByWidth(page.width/1.152, "Ошибка 404"))),
        ft.ElevatedButton("На главную", on_click=lambda e: page.go("/"))
    )