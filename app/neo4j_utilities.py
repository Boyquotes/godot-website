from app import app
from neo4j.v1 import GraphDatabase, basic_auth


def get_browse_data():
    """
    returns GODOT URIs and string of paths as a list of dictionaries
        for browse data page on website
    :return: list of dictionaries
    """
    query = "match (t:Timeline),(g:GODOT),p = shortestPath((t)-[*..15]->(g)) return p"
    results = query_neo4j_db(query)
    browse_array = []
    for path in results:
        entry_dict = {}
        path_str = ""
        nodes = path["p"].nodes
        for n in nodes:
            if list(n.labels)[0] != 'Timeline':
                label = list(n.labels)[0]
                for k, v in n.items():
                    if label == "GODOT" and k == 'uri':
                        # get GODOT ID only
                        entry_dict['godot_uri'] = v.split("/")[-1]
                    if k == 'type' and label != 'GODOT':
                        if v != 'number' and v != 'reign' and v != 'mont' and v != 'day' and v != 'consulship':
                            path_str += "%s " % v
                    if k == 'value':
                        path_str += " %s " % v
        entry_dict['path_str'] = path_str
        browse_array.append(entry_dict)
    return browse_array


def get_godot_path(godot_uri):
    """
    returns all paths between Timeline node and the GODOT node
    :param godot_uri: string/uri of GODOT ID
    :return: list of dictionaries
    """
    query = "match (t:Timeline),(g:GODOT {uri:'%s'}),p = ((t)-[*..15]->(g)) return p" % godot_uri
    results = query_neo4j_db(query)
    paths = []
    for record in results:
        nodes = record["p"].nodes
        for n in nodes:
            if list(n.labels)[0] != 'Timeline' and list(n.labels)[0] != 'GODOT':
                n_dict = {'label': list(n.labels)[0]}
                for k, v in n.items():
                    n_dict[k] = str(v)
                paths.append(n_dict)
    return paths


def get_attestations(godot_uri):
    """
    returns all attestations for specified GODOT node
    :param godot_uri: string/uri of GODOT ID
    :return: list of dictionaries
    """
    query = "match (g:GODOT {uri:'%s'})--(a:Attestation) return a" % godot_uri
    results = query_neo4j_db(query)
    att = []
    for record in results:
        att.append({k: v for (k, v) in record["a"].items()})
    return att


def query_neo4j_db(query):
    """
    performs query into graph database and returns results
    :param query: string of cypher query
    :return: result dictionary
    """
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=basic_auth(
        app.config['NEO4J_USER'], app.config['NEO4J_PASSWORD']))
    session = driver.session()
    res = session.run(query)
    session.close()
    return res
