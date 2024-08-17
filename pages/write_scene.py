import flet as ft


def write_scene_page(page: ft.Page):
    page.ttitle = ft.Text(f"Сценарий игры", text_align=ft.TextAlign.CENTER, width=page.width, size=56)
    page.add(page.ttitle, ft.Row([
        ft.ElevatedButton(content=ft.Column([ft.Icon(ft.icons.SMART_TOY, size=page.width/3), ft.Text("Создать сценарий нейросетью", size=23, text_align=ft.TextAlign.CENTER, width=page.width/3)], ft.MainAxisAlignment.CENTER), width=page.width/2.5, height=page.width/2.5, on_click=lambda _: ai_char()),
        ft.ElevatedButton(content=ft.Column([ft.Icon(ft.icons.EDIT, size=page.width/3), ft.Text("Написание собственного сценария", size=23, text_align=ft.TextAlign.CENTER, width=page.width/3)], ft.MainAxisAlignment.CENTER), width=page.width/2.5, height=page.width/2.5, on_click=lambda _: page.open(
            ft.AlertDialog(modal=True, content=ft.Container(
                ft.TextField(label="Сценарий игры", multiline=True, width=page.width),
                width=page.width, height=page.height
            ))
        ))
    ], ft.MainAxisAlignment.SPACE_AROUND))