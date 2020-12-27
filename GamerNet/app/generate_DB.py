from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF
import random
import json
import os
#from GamerNet.settings import BASE_DIR

g = Graph()
NS = Namespace('http://GamerNetLibrary.com/')


def generation():
    with open('data/games_full_info.json') as file_parser:
        json_games = json.load(file_parser)
        tmp_array = json_games.keys()
        count = 0
        appid_array = [ key for key in tmp_array]


        for idx in json_games:

            game = json_games[idx]["data"]

            subject = NS[appid_array[count]]

            g.add((subject, RDF.type, NS[game["type"]]))
            g.add((subject,NS.name, Literal(game["name"])))
            g.add((subject, NS.release_date, Literal(game["release_date"]["date"])))
            g.add((subject, NS.description, Literal(game["short_description"])))
            g.add((subject, NS.image, Literal(game["header_image"])))
            g.add((subject, NS.website, Literal(game["website"])))

            if "screenshots" in game.keys():
                g.add((subject, NS.screenshot, Literal(game["screenshots"][0]["path_full"])))
            for platform in game["platforms"]:
                if game["platforms"][platform]:
                    g.add((subject, NS.platform, Literal(platform)))
            for category in game["categories"]:
                g.add((subject, NS.category, Literal(category["description"])))
            if "genres" in game.keys():
                for genre in game["genres"]:
                    g.add((subject, NS.genre, Literal(genre["description"])))
            if "dlc" in game.keys():
                for dlc in game["dlc"]:
                    g.add((subject, NS.dlc, NS["dlc" + str(dlc)]))
            if "price_overview" in game.keys():
                g.add((subject, NS.price, Literal(game["price_overview"]["final_formatted"])))

            count += 1




def graph_export():
    g.bind("dc", DC)
    g.bind("foaf", FOAF)
    g.bind("game", NS)

    of = open("graph.n3", "wb")
    of.write(g.serialize(format="n3"))
    of.close()




generation()
graph_export()
