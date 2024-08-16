from flet import Page

from .index import *
from .game import *
from .select_players import *
from .p404 import *
from .start_game import *
from .tokens_expired_error import *
from .unkown_error import *
from.setup_chars import *

ROUTES = {
    "/": index_page,
    "/game": game_page,
    "/select_players": select_players_page,
    "/404": p404_page,
    "/start_game": start_game_page,
    "/tokens_expired_error": tokens_expired_error_page,
    "/unknown_error": unknown_error_page,
    "/setup_chars": setup_chars_page
}

def router(route: str, page: Page):
    page.clean()
    if not route in ROUTES.keys():
        page.go("/404", True)
        return ROUTES["/404"]
    return ROUTES[route]