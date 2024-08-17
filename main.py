import flet as ft

import pages

def main(page: ft.Page):
    def on_route_change(e: ft.RouteChangeEvent | None):
        pages.router(page.route, page)(page)
    
    page.on_route_change = on_route_change
    page.theme_mode = ft.ThemeMode.DARK

    on_route_change(None)

ft.app(main, host="192.168.0.137", port=80, view=ft.AppView.WEB_BROWSER, assets_dir="content")