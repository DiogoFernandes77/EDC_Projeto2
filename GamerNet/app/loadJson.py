import json
import requests

complement_url = 'https://store.steampowered.com/api/appdetails/'


def extract_games():
    with open('data/games_info.json') as g:
        games = json.load(g)

        i = 0
        games_info= {}
        for game in games:
            game_info = requests.get(complement_url + '?appids=' + game)

            json_info = json.loads(game_info.text)

            games_info.update(json_info)
            #print("game --- " + str(game_info.text))
            #print(type(game_info.text))
            i+=1

            if i > 100:
                print("Got 100 games")
                with open('data/games_full_info.json', 'w') as w:
                    w.write(json.dumps(games_info, indent=4))
                break

            print(i)



extract_games()