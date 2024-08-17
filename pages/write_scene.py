import flet as ft


import utils as u

def write_scene_page(page: ft.Page):
    if not u.tryAttr(page, "game"):
        if not u.tryAttr(page, "players"):
            page.go("/select_players")
            return
        page.go("/setup_chars")
        return
    
    def create_ai():
        page.game.plot_with_ai()
        page.go("/start_game")

    def set_plot():
        page.game.set_plot(page.tft.value)
        page.go("/start_game")
    
    page.ttitle = ft.Text(f"Сценарий игры", text_align=ft.TextAlign.CENTER, width=page.width, size=56)
    page.tft = ft.TextField(label="Сценарий игры", multiline=True, width=page.width)
    page.add(page.ttitle, ft.Row([
        ft.Column([ft.ElevatedButton(content=ft.Column([ft.Icon(ft.icons.SMART_TOY, size=page.width/3.5), ], ft.MainAxisAlignment.CENTER), width=page.width/3.5, height=page.width/3.5, on_click=lambda _: create_ai()), ft.Text("Предоставить написание сценария игры нейросети", size=23, text_align=ft.TextAlign.CENTER, width=page.width/3.5)], ft.MainAxisAlignment.CENTER),
        ft.Column([ft.ElevatedButton(content=ft.Column([ft.Icon(ft.icons.EDIT, size=page.width/3.5), ], ft.MainAxisAlignment.CENTER), width=page.width/3.5, height=page.width/3.5, on_click=lambda _: page.open(
            ft.AlertDialog(modal=True, content=ft.Container(
                page.tft,
                width=page.width, height=page.height
            ), actions=[
                ft.TextButton("Создать нейросетью", on_click=lambda _: create_ai()),
                ft.TextButton("Отправить сценарий", on_click=lambda _: set_plot())
            ]
            )
        )), ft.Text("Написать свой сценарий", size=23, text_align=ft.TextAlign.CENTER, width=page.width/3.5)], ft.MainAxisAlignment.CENTER)
    ], ft.MainAxisAlignment.SPACE_AROUND))