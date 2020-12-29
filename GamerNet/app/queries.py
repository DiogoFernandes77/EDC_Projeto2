from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
import json

def get_genres(): #devolve uma lista com todos o géneros de jogos, sem repetidos por ordem alfabética
    query = """select  ?genre
    where
    {
        ?name a game:game .
        ?name game:genre ?genre.

    }group by ?genre
    order by asc(?genre)"""

    result = queryDB(query)
    return [x["genre"]["value"] for x in result]

def get_games():
    query = """select  ?name ?gameName  ?image ?description
        where 
        {
            ?name a game:game .
            ?name game:description ?description. 
            ?name game:name ?gameName.
            ?name game:image ?image.
        }"""

    result = queryDB(query)
    return [(x["image"]["value"], x["gameName"]["value"], x["description"]["value"], x["name"]["value"]) for x in result]

def search_game(name, genre =""):
    query = """select  ?name ?gameName  ?image ?description
            where 
            {
                ?name a game:game .
                ?name game:description ?description. 
                ?name game:name ?gameName.
                ?name game:image ?image.
            """
    if genre:
        query+="""
                ?name game:genre \'""" + genre + """\'. """

    query += """filter regex(?gameName,\'""" + name + """\',"i")  #filtra tds os jogos que contem name
            }"""
    result = queryDB(query)
    print(result)
    return [(x["image"]["value"], x["gameName"]["value"], x["description"]["value"], x["name"]["value"]) for x in
            result]

def get_games_by_genre(genre):
    query = """select  ?name ?gameName  ?image ?description
            where 
            {
                ?name a game:game .
                ?name game:description ?description. 
                ?name game:name ?gameName.
                ?name game:image ?image.
                ?name game:genre \'""" + genre + """\'.
            }"""

    result = queryDB(query)
    return [(x["image"]["value"], x["gameName"]["value"], x["description"]["value"], x["name"]["value"]) for x in
            result]

def queryDB(query):
    query = """
        PREFIX game: <http://GamerNetLibrary.com/>
    """ + query
    endpoint = "http://localhost:7200"
    repo = "games"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    if query.find('update') != -1 or query.find('insert') != -1:
        payload = {"update": query}
        accessor.sparql_update(body=payload, repo_name=repo)
    else:
        payload = {"query": query}
        result = accessor.sparql_select(body=payload, repo_name=repo)
        result_json = json.loads(result)
        return result_json["results"]["bindings"]


def test():
    result_json = queryDB("""select  ?name ?gameName  ?image ?description
    where 
    {
        ?name a game:game .
        ?name game:description ?description. 
        ?name game:name ?gameName.
        ?name game:image ?image.
    }""")

    print(result_json["results"]["bindings"][1]["description"]["value"])
    print([x["image"]["value"] for x in result_json["results"]["bindings"]])

#print(get_genres())
#print(get_games_by_genre('Free to Play'))
#print(search_game('Cou'))
print(search_game('Cou', 'Action'))