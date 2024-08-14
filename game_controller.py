import flet as ft


class Game:
    def __init__(self, page: ft.Page):
        try: page.players
        except AttributeError:
            page.go("/select_players")
            return
        self.page = page
        
    def start(self, callback: callable, error_callback: callable):
        self.img = "https://kappa.lol/cio8N"
        self.info_players = []
        for i in range(self.page.players):
            self.info_players.append({"name": f"Имя {i+1}", "info": f"Еще что нибудь {i+1}"})
        callback()