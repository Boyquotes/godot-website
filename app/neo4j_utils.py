from app import app
from neo4j.v1 import GraphDatabase, basic_auth


def get_browse_data(yrs, page):
    """
    returns GODOT URIs and string of paths as a list of dictionaries
        for browse data page on website
    :return: list of dictionaries
    """
    limit = 20
    page = int(page) * 20 - 20
    if page < 1:
        page = 0
    if yrs != 'All':
        if "-" in yrs:
            query = "match (yrs:YearReferenceSystem {type:'%s'})--(yrs2:YearReferenceSystem {type:'%s'}), (g:GODOT), p = shortestPath((yrs2)-[*..15]->(g)) return p order by g skip %s limit %s" % (
                yrs.split(" - ")[0], yrs.split(" - ")[1], page, limit)
        else:
            query = "match (yrs:YearReferenceSystem {type:'%s'}), (g:GODOT), p = shortestPath((yrs)-[*..15]->(g)) return p order by g skip %s limit %s" % (
            yrs, page, limit)
    else:
        query = "match (t:Timeline), (g:GODOT), p = shortestPath((t)-[*..15]->(g)) return p order by g skip %s limit %s" % (
            page, limit)
    results = query_neo4j_db(query)
    browse_array = []
    if results is not None:
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
                            if v != 'number' and v != 'reign' and v != 'month' and v != 'day' and v != 'consulship' and v != 'type' and v != 'name':
                                path_str += "%s " % v
                        if k == 'value':
                            path_str += " %s " % v
            entry_dict['path_str'] = path_str
            browse_array.append(entry_dict)
    return browse_array


def get_browse_data_number_of_results(yrs):
    if yrs != 'All':
        if "-" in yrs:
            query = "match (yrs:YearReferenceSystem {type:'%s'})--(yrs2:YearReferenceSystem {type:'%s'}), (g:GODOT), p = shortestPath((yrs2)-[*..15]->(g)) return count(p) as p" % (yrs.split(" - ")[0], yrs.split(" - ")[1])
        else:
            query = "match (yrs:YearReferenceSystem {type:'%s'}), (g:GODOT), p = shortestPath((yrs)-[*..15]->(g)) return count(p) as p" % (
                yrs)
    else:
        query = "match (t:Timeline), (g:GODOT), p = shortestPath((t)-[*..15]->(g)) return count(p) as p"
    results = query_neo4j_db(query)
    total_hits = 0
    if results:
        for record in results:
            total_hits = record["p"]
    return total_hits


def get_godot_path(godot_uri):
    """
    returns all paths between Timeline node and the GODOT node
    :param godot_uri: string/uri of GODOT ID
    :return: list of dictionaries
    """
    query = "match (t:Timeline),(g:GODOT {uri:'%s'}),p = ((t)-[*..15]->(g)) return p" % godot_uri
    results = query_neo4j_db(query)
    paths = []
    if results:
        for record in results:
            nodes = record["p"].nodes
            for n in nodes:
                #if list(n.labels)[0] != 'Timeline' and list(n.labels)[0] != 'GODOT':
                if list(n.labels)[0] != 'Timeline':
                    n_dict = {'label': list(n.labels)[0]}
                    for k, v in n.items():
                        n_dict[k] = str(v)
                    paths.append(n_dict)
    return paths


def get_godot_node_properties(godot_uri):
    """
    returns dict of all node properties
    :param godot_uri: string (URI of GODOT node)
    :return: dict
    """
    query = "match (g:GODOT {uri:'%s'}) return g as g" % godot_uri
    results = query_neo4j_db(query)
    node_props_dict = {}
    if results:
        for record in results:
            from pprint import pprint
            pprint(record)
            for k, v in record['g'].items():
                node_props_dict[k] = v
    return node_props_dict


def get_attestations(godot_uri):
    """
    returns all attestations for specified GODOT node
    :param godot_uri: string/uri of GODOT ID
    :return: list of dictionaries
    """
    query = "match (g:GODOT {uri:'%s'})--(a:Attestation) return a, id(a) as b" % godot_uri
    results = query_neo4j_db(query)
    att = []
    if results:
        for record in results:
            tmp_dict = {}
            tmp_dict.update({'node_id': record['b']})
            for (k, v) in record["a"].items():
                tmp_dict[k] = v
            att.append(tmp_dict)
    return att


def query_neo4j_db(query):
    """
    performs query into graph database and returns results
    :param query: string of cypher query
    :return: result dictionary
    """
    driver = get_neo4j_driver()
    if driver:
        with driver.session() as session:
            res = session.run(query)
            session.close()
            return res
    else:
        return None


def get_neo4j_driver():
    """
    gets Neo4j Driver instance
    :return: neo4j driver
    """
    uri = "bolt://localhost:7687"
    try:
        return GraphDatabase.driver(uri, auth=basic_auth(
            app.config['NEO4J_USER'], app.config['NEO4J_PASSWORD']))
    except:
        return None


def get_number_of_nodes():
    """
    returns number of nodes in GODOT graph
    :return: number of nodes (int)
    """
    query = "MATCH (n) RETURN count(*) as n"
    results = query_neo4j_db(query)
    n = 0
    if results:
        for record in results:
            n = record["n"]
    return n


def get_number_of_relations():
    """
    returns number of relations in GODOT graph
    :return: number of relations (int)
    """
    query = "MATCH (n)-[r]->() RETURN COUNT(r) as n"
    results = query_neo4j_db(query)
    n = 0
    if results:
        for record in results:
            n = record["n"]
    return n


def get_number_of_godot_uris():
    """
    returns number of GODOT nodes in GODOT graph
    :return: number of nodes (int)
    """
    query = "MATCH (n:GODOT) RETURN count(*) as n"
    results = query_neo4j_db(query)
    n = 0
    if results:
        for record in results:
            n = record["n"]
    return n


def get_list_of_yrs():
    """
    returns list of yrs in the GODOT graph
    :return: list of yrs
    """
    query = "match (t:Timeline)--(yrs1:YearReferenceSystem) optional match (yrs1)--(yrs2:YearReferenceSystem) return yrs1, yrs2"
    results = query_neo4j_db(query)
    yrs = ['All']
    if results:
        for record in results:
            label = record["yrs1"]["type"]
            if record["yrs2"]:
                label += " - " + record["yrs2"]["type"]
            yrs.append(label)
    return yrs


def get_attestation(node_id):
    query = "match (a:Attestation) where id(a) = %s return a" % node_id
    results = query_neo4j_db(query)
    tmp_dict = {}
    for record in results:
        for (k, v) in record["a"].items():
            tmp_dict[k] = v
    return tmp_dict


def update_attestation(node_id, attestation_uri, title, date_string):
    title = _clean_string(title)
    date_string = _clean_string(date_string)
    query = "match (a:Attestation) where id(a) = %s set a.date_string='%s', a.title = '%s', a.uri = '%s'" % (node_id, date_string, title, attestation_uri)
    results = query_neo4j_db(query)
    if results:
        return results


def delete_attestation(node_id):
    query = "match (a:Attestation)-[r:hasAttestation]-(:GODOT) where id(a) = %s delete a, r" % node_id
    results = query_neo4j_db(query)
    if results:
        return results


def _clean_string(str):
    """
    cleans data entered by user, including escaping
    :param str: string
    :return: string
    """
    str = str.replace("'", "\\'")
    return str
