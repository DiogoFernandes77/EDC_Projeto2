from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF
import random
import json
import os
from GamerNet.settings import BASE_DIR

g = Graph()
NS = Namespace('http://GamerNetLibrary.com/')


def generation():
    with open(os.path.join(BASE_DIR, 'app/data/games_info.json')) as file_parser:
        json_games = json.load(file_parser)

        for idx in json_games:
            game = json_games[idx]
            subject = json_games["appid"]
            g.add(subject, RDF.type, NS["game"])
            g.add(subject,NS.name, Literal(game["name"]))

