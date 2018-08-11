from app import app
from neo4j.v1 import GraphDatabase, basic_auth


def get_session():
    """ returns neo4j session, based on user/password stored in
        environment variables
    """
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=basic_auth(
        app.config['NEO4J_USER'], app.config['NEO4J_PASSWORD']))
    return driver.session()


def get_godot_path(godot_uri):
    """ returns all paths between Timeline node and the GODOT node
        specified by GODOT URI as list of dictionaries
    """
    query = "match (t:Timeline),(g:GODOT {uri:'%s'}),p = ((t)-[*..15]->(g)) return p" % godot_uri
    session = get_session()
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
    session = get_session()
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
