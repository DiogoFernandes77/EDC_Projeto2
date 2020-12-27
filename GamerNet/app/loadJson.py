import json
import requests

complement_url = 'https://store.steampowered.com/api/appdetails/'


def extract_games():
    with open('data/games_info.json') as g:
        games = json.load(g)

        #for game in games:
