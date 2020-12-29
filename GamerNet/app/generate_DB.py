from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF
import random
import json
import os

# from GamerNet.settings import BASE_DIR

g = Graph()
NS = Namespace('http://GamerNetLibrary.com/')
names = ["Pedro", "Diogo", "Daniel", "Francisco", "Mario", "Maria", "Joana", "Gustavo", "Rodrigo", "Santiago",
         "Henrique", "Antonio", "Jorge", "Eduardo", "Eduarda", "Milene", "Sara", "Marta", "Antonieta", "Mariana",
         "Ricardo", "Silvia"]
surnames = ["Fernandes", "Alves", "Pereira", "Pomar", "Martins", "Pinheiro", "Pinho", "Nunes", "Machado", "Esteves",
            "Freitas"]


person_number = 20
tmp = ""

def generation():
    with open('data/games_full_info.json') as file_parser:
        json_games = json.load(file_parser)
        tmp_array = json_games.keys()
        count = 0
        appid_array = [key for key in tmp_array]

        for idx in json_games:

            game = json_games[idx]["data"]

            subject = NS[appid_array[count]]

            g.add((subject, RDF.type, NS[game["type"]]))

            g.add((subject, NS.name, Literal(game["name"])))
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
            if "price_overview" in game.keys():
                g.add((subject, NS.price, Literal(game["price_overview"]["final_formatted"])))
            else:
                g.add((subject, NS.price, Literal("0,00\u20ac")))

            count += 1



def people_generation():

    for id in range(0, person_number):
        name = random.choice(names)
        surname = random.choice(surnames)
        username = name + "_" + surname + str(id)
        subject = NS["Account" + str(id)]

        g.add((subject, RDF.type, FOAF.Person))
        g.add((subject,FOAF.nick,Literal(username)))
        g.add((subject,FOAF.name,Literal(name + " " + surname)))
        g.add((subject,FOAF.logo, Literal('/static/img/Pic' + str(id) + '.jpeg')))
        #games owned
        n_games_owned = random.randint(1, 10)
        games_list = list(g.subjects(RDF.type, NS.game))
        random.shuffle(games_list)
        for i in range(0, n_games_owned):
            g.add((subject,NS.owns, games_list[i]))



def people_friends_generation():
    people = list(g.subjects(RDF.type, FOAF.Person))
    random.shuffle(people)
    pl_iter = people.copy()

    for i in range(0,len(people)):
        friends_list = []
        relation_number = random.randint(0, 10)
        subject = people.pop()
        for x in range(0, relation_number):
            friend = None
            while(friend == subject) or (friend in friends_list) or (friend == None):
                friend = random.choice(pl_iter)
            friends_list.append(friend)
            g.add((subject, FOAF.knows, friend))







def graph_export():
    g.bind("dc", DC)
    g.bind("foaf", FOAF)
    g.bind("game", NS)

    of = open("graph.n3", "wb")
    of.write(g.serialize(format="n3"))
    of.close()


generation()
people_generation()
people_friends_generation()
graph_export()
