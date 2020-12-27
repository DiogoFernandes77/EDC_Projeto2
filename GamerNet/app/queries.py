from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
import json

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
        return json.loads(result)


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