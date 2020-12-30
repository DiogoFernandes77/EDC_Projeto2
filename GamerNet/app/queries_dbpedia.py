from SPARQLWrapper import SPARQLWrapper, JSON
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
import json
import time

def query_dbpedia(query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql") #http://dbpedia.org / https://query.wikidata.org/bigdata/namespace/wdq/sparql
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()
    return results

def dbpedia_get_decription(game):
    query = """SELECT *
        WHERE
        {
          ?game rdfs:label \"""" + game + """\"@en;
           dbo:abstract ?info.
           FILTER(lang(?info) = 'en')
        }"""

    results = query_dbpedia(query)

    # for result in results["results"]["bindings"]:
    #     print(result["game"]["value"],result["info"]["value"])
    return [(result["info"]["value"]) for result in results["results"]["bindings"]]

def dbpedia_get_dev(game):
    query = """SELECT *
        WHERE
        {
          ?game rdfs:label \"""" + game + """\"@en;
           dbo:developer ?info.
        }"""

    results = query_dbpedia(query)

    # for result in results["results"]["bindings"]:
    #     print(result["game"]["value"],result["info"]["value"])
    return [(result["info"]["value"]) for result in results["results"]["bindings"]]




#print(dbpedia_get_dev("Fortnite"))


#print(dbpedia_get_decription("Fortnite"))



def dbpedia_example():
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?label
    WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        print(result["label"]["value"])
    print('---------------------------')
    for result in results["results"]["bindings"]:
        print('%s: %s' % (result["label"]["xml:lang"], result["label"]["value"]))





