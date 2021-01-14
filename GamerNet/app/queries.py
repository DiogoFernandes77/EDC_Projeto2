import time

from SPARQLWrapper import SPARQLWrapper, JSON
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


def get_games(acc): #jogos que a account logada não tem e pode comprar
    query = """select  ?name ?gameName  ?image ?description ?price ?site
        where 
        {
            ?name a game:game .
            ?name game:description ?description. 
            ?name game:name ?gameName.
            ?name game:image ?image.
            ?name game:price ?price.
            ?name game:website ?site.
             FILTER (
                    !EXISTS {
                       game:""" + acc + """ game:owns ?name.
                    }
            )
        }
       
        """


    result = queryDB(query)
    return [(x["image"]["value"], x["gameName"]["value"], x["description"]["value"], x["name"]["value"],
             x["price"]["value"], x["site"]["value"]) for x in
            result]


def search_game(name, acc, genre=""):
    query = """select  ?name ?gameName  ?image ?description ?price ?site
            where 
            {
                ?name a game:game .
                ?name game:description ?description. 
                ?name game:name ?gameName.
                ?name game:image ?image.
                ?name game:price ?price.
                ?name game:website ?site.
                FILTER (
                    !EXISTS {
                       game:""" + acc + """ game:owns ?name.
                    }
            )
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


def get_games_by_genre(genre, acc):
    query = """select  ?name ?gameName  ?image ?description ?price ?site
            where 
            {
                ?name a game:game .
                ?name game:description ?description. 
                ?name game:name ?gameName.
                ?name game:image ?image.
                ?name game:price ?price.
                ?name game:website ?site.
                ?name game:genre \'""" + genre + """\'
                FILTER (
                    !EXISTS {
                       game:""" + acc + """ game:owns ?name.
                    }
            ).
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
            select ?name ?nick ?account ?logo
            where { 
                ?account foaf:name ?name.
                ?account foaf:nick ?nick.
                ?account foaf:logo ?logo.
                FILTER (
                    !EXISTS {
                        ?account foaf:knows game:""" + acc + """.
                    }
                )
                filter (game:""" + acc + """ != ?account)
              
            } 
        """
    result = queryDB(query)
    return [(x["name"]["value"], x["nick"]["value"], x["account"]["value"], x["logo"]["value"]) for x in result]


def get_friends(acc):
    query = """
                select ?name ?nick ?account ?logo
                where { 
                    ?account foaf:name ?name.
                    ?account foaf:nick ?nick.
                    ?account foaf:knows game:""" + acc + """.
                    ?account foaf:logo ?logo.
                } 
            """
    result = queryDB(query)
    return [(x["name"]["value"], x["nick"]["value"], x["account"]["value"], x["logo"]["value"]) for x in result]

def get_recommended_friends(acc):

    query = """
                select (count(distinct(?game)) as ?count) ?account
                where 
                { 
                    {   
                
                        game:""" + acc + """ a foaf:Person .
                        game:""" + acc + """ game:owns ?game .
                    }
                    {
                        ?account game:owns ?game.
                    }
                    
                    minus {game:""" + acc + """ foaf:knows ?account}
                    filter (game:""" + acc + """ != ?account)
                    
                          
                }
                group by ?account
                order by desc(?count)
    """
    result = queryDB(query)

    if not 'account' in result[0]:
        print("sem amigos recomencados")
        result1 = []
    else:
        result = [(x["account"]["value"]) for x in result]


        rec_friend = [ p.split("http://GamerNetLibrary.com/")[1] for p in result]

        result1 = []

        for r in rec_friend:

            result1.append(get_attributes(acc, r))


    return result1

def get_attributes(acc1, acc2):


    query = """
                select ?name ?nick ?logo ?account
                where { 
                      game:""" + acc2 + """ foaf:name ?name.
                      game:""" + acc2 + """ foaf:nick ?nick.
                      game:""" + acc2 + """ foaf:logo ?logo.
                      FILTER (
                        !EXISTS {
                            game:""" + acc1 + """ foaf:knows game:""" + acc2 + """.
                    }
                )
                      
                }"""

    lst = queryDB(query)
    return [(x["name"]["value"], x["nick"]["value"], "http://GamerNetLibrary.com/"+str(acc2), x["logo"]["value"]) for x in lst][0]

def get_common_games(acc1,acc2):
    query = """
                select ?game
                where { 
                        {
                            game:""" + acc1 + """ game:owns ?game .
                        }
                        {
                            game:""" + acc2 + """ game:owns ?game .
                        }
                   
                } 
                """
    result = queryDB(query)
    #print(result)
    return [ x["game"]["value"] for x in result]

def get_common_friends(acc1,acc2):
    query = """
            select ?person ?name ?nick ?logo
            where { 
                    {
                      
                        game:""" + acc1 + """ foaf:knows ?person .
                    }
                    {
                        game:""" + acc2 + """ foaf:knows ?person .
                        ?person foaf:name ?name.
                        ?person foaf:nick ?nick.
                        ?person foaf:logo ?logo.
                    }

            } 
            """
    result = queryDB(query)
    # print(result)
    return [(x["name"]["value"], x["nick"]["value"], x["person"]["value"], x["logo"]["value"]) for x in result]

def make_friend(friend1, friend2):
    query = """
            insert data{
                game:""" + friend1 + """ foaf:knows game:""" + friend2 + """.
            }
        """

    print(queryDB(query))

def delete_friend(friend1, friend2):
    query = """
            delete data{
                game:""" + friend1 + """ foaf:knows game:""" + friend2 + """.
            }
        """

    print(queryDB(query))

def buy_game(acc, game_id):
    query = """
    
            insert data{
                game:"""+acc+""" game:owns game:"""+game_id+""".
            }
    """
    print(queryDB(query))

def queryDB(query):
    query = """
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX game: <http://GamerNetLibrary.com/>
    """ + query
    endpoint = "http://localhost:7200"
    repo = "games"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    if query.find('update') != -1 or query.find('insert') != -1 or query.find('delete') != -1:
        print("update")
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
#print(get_no_friends("Account1"))
#print(get_attributes("Account1"))
#print(get_recommended_friends("Account1"))
#print(get_common_games("Account10","Account16"))
print(get_common_friends("Account10","Account16"))
#print(get_games("Account1"))
#print(search_game("Counter", "Account1"))
#print(make_friend("Account1", "Account7"))
