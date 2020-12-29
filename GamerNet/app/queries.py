from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
import json


def get_genres():  # devolve uma lista com todos o géneros de jogos, sem repetidos por ordem alfabética
    query = """select  ?genre
    where
    {
        ?name a game:game .
        ?name game:genre ?genre.

    }group by ?genre
    order by asc(?genre)"""

    result = queryDB(query)
    return [x["genre"]["value"] for x in result]


def insert_price():  # inserir preço nos free to play
    """PREFIX game: <http://GamerNetLibrary.com/>

    INSERT{
        ?name game:price "0,00€"
    }
    where
    {
        ?name a game:game .
        ?name game:genre "Free to Play".
    }"""


def get_games():
    query = """select  ?name ?gameName  ?image ?description ?price ?site
        where 
        {
            ?name a game:game .
            ?name game:description ?description. 
            ?name game:name ?gameName.
            ?name game:image ?image.
            ?name game:price ?price.
            ?name game:website ?site.
        }"""

    result = queryDB(query)
    return [(x["image"]["value"], x["gameName"]["value"], x["description"]["value"], x["name"]["value"],
             x["price"]["value"], x["site"]["value"]) for x in
            result]


def search_game(name, genre=""):
    query = """select  ?name ?gameName  ?image ?description ?price ?site
            where 
            {
                ?name a game:game .
                ?name game:description ?description. 
                ?name game:name ?gameName.
                ?name game:image ?image.
                ?name game:price ?price.
                ?name game:website ?site.
            """
    if genre:
        query += """
                ?name game:genre \'""" + genre + """\'. """

    query += """filter regex(?gameName,\'""" + name + """\',"i")  #filtra tds os jogos que contem name
            }"""
    result = queryDB(query)
    # print(result)
    return [(x["image"]["value"], x["gameName"]["value"], x["description"]["value"], x["name"]["value"],
             x["price"]["value"], x["site"]["value"]) for x in
            result]

0
def get_game_info(appid):
    query = """select  ?gamename ?image ?description ?price ?site
            where 
            {
                game:""" + appid + """ game:name ?gamename.
    			game:""" + appid + """ game:image ?image.
    			game:""" + appid + """ game:price ?price.
    			game:""" + appid + """ game:website ?site.
            }"""

    result = queryDB(query)

    return [(x["image"]["value"], x["gamename"]["value"], x["price"]["value"], x["site"]["value"]) for x in result]


def get_games_by_genre(genre):
    query = """select  ?name ?gameName  ?image ?description ?price ?site
            where 
            {
                ?name a game:game .
                ?name game:description ?description. 
                ?name game:name ?gameName.
                ?name game:image ?image.
                ?name game:price ?price.
                ?name game:website ?site.
                ?name game:genre \'""" + genre + """\'.
            }"""

    result = queryDB(query)
    return [(x["image"]["value"], x["gameName"]["value"], x["description"]["value"], x["name"]["value"],
             x["price"]["value"], x["site"]["value"]) for x in result]


def get_accounts():
    query = """
     select ?s
      where { 
	    ?s foaf:name ?name .
        }  """
    result = queryDB(query)

    res = [(x["s"]["value"].split("http://GamerNetLibrary.com/")[1]) for x in result]
    return res


def get_person_info(pessoa):
    query = """
        select ?name ?nick ?games ?logo
        where { 
            game:""" + pessoa + """ foaf:name ?name.
            game:""" + pessoa + """ foaf:nick ?nick.
            game:""" + pessoa + """ game:owns ?games.
            game:""" + pessoa + """ foaf:logo ?logo.
            

        } 
    """

    result = queryDB(query)
    #print(result)
    res = [result[0]["name"]["value"], result[0]["nick"]["value"], result[0]["logo"]["value"]]  # pos 0,1 n 2 = name, nick,logo
    for x in result:
        res.append(x["games"]["value"])

    return res


def get_no_friends(acc):
    query = """
            select ?name ?nick ?account
            where { 
                ?account foaf:name ?name.
                ?account foaf:nick ?nick.
                FILTER (
                    !EXISTS {
                        ?account foaf:knows game:""" + acc + """.
                    }
                )
            } 
        """
    result = queryDB(query)
    return [(x["name"]["value"], x["nick"]["value"], x["account"]["value"]) for x in result]


def get_friends(acc):
    query = """
                select ?name ?nick ?account
                where { 
                    ?account foaf:name ?name.
                    ?account foaf:nick ?nick.
                    ?account foaf:knows game:""" + acc + """.

                } 
            """
    result = queryDB(query)
    return [(x["name"]["value"], x["nick"]["value"], x["account"]["value"]) for x in result]

def queryDB(query):
    query = """
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
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

# print(get_genres())
# print(get_games_by_genre('Free to Play'))
# print(search_game('Counter'))
# print(search_game('Cou', 'Action'))
#print(get_person_info("Account11"))
# print(get_accounts())
# print(insert_price())
# print(get_games())
# print(get_game_info("10"))
# insert_price()
