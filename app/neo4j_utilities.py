from app import app
from neo4j.v1 import GraphDatabase, basic_auth


def get_browse_data():
    """ returns GODOT URIs and string of paths as a list of dictionaries
        for browse data page on website as a list of dictionaries
    """
    query = "match (t:Timeline),(g:GODOT),p = shortestPath((t)-[*..15]->(g)) return p"
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=basic_auth(
        app.config['NEO4J_USER'], app.config['NEO4J_PASSWORD']))
    session = driver.session()
    results = session.run(query)
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
                        godot = v.split("/")
                        entry_dict['godot_uri'] = godot[-1]
                    if k == 'type' and label != 'GODOT':
                        if v != 'number' and v != 'reign' and v != 'mont' and v != 'day' and v != 'consulship':
                            path_str += "%s " % v
                    if k == 'value':
                        path_str += " %s " % v
        entry_dict['path_str'] = path_str
        browse_array.append(entry_dict)
    session.close()
    return browse_array


def get_godot_path(godot_uri):
    """ returns all paths between Timeline node and the GODOT node
        specified by GODOT URI as list of dictionaries
    """
    query = "match (t:Timeline),(g:GODOT {uri:'%s'}),p = ((t)-[*..15]->(g)) return p" % godot_uri
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=basic_auth(
        app.config['NEO4J_USER'], app.config['NEO4J_PASSWORD']))
    session = driver.session()
    print("get_godot_path: " + query)
    results = session.run(query)
    paths = []
    for record in results:
        nodes = record["p"].nodes
        for n in nodes:
            if list(n.labels)[0] != 'Timeline' and list(n.labels)[0] != 'GODOT':
                n_dict = {}
                n_dict['label'] = list(n.labels)[0]
                for k, v in n.items():
                    n_dict[k] = str(v)
                paths.append(n_dict)
    session.close()
    return paths


def get_attestations(godot_uri):
    """ returns all attestations for specified GODOT node
        as a list of dictionaries
    """
    query = "match (g:GODOT {uri:'%s'})--(a:Attestation) return a" % godot_uri
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=basic_auth(
        app.config['NEO4J_USER'], app.config['NEO4J_PASSWORD']))
    session = driver.session()
    print("get_attestations: " + query)
    results = session.run(query)
    att = []
    for record in results:
        r_dict = {}
        for k, v in record["a"].items():
            r_dict[k] = v
        att.append(r_dict)
    session.close()
    return att
