import flet as ft


def unknown_error_page(page: ft.Page):
    page.add(ft.TextButton("Произошла ошибка при генерации. Нажмите сюда чтобы вернуться на главную >", on_click=lambda _: page.go("/")))