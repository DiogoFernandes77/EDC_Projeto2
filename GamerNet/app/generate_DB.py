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
