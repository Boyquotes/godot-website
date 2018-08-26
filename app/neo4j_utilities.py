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
    if yrs != 'all':
        query = "match (yrs:YearReferenceSystem {type:'%s'}), (g:GODOT), p = shortestPath((yrs)-[*..15]->(g)) return p order by g skip %s limit %s" % (
            yrs, page, limit)
    else:
        query = "match (t:Timeline), (g:GODOT), p = shortestPath((t)-[*..15]->(g)) return p order by g skip %s limit %s" % (
            page, limit)
    print(query)
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


def get_browse_data_number_of_results(yrs):
    if yrs != 'all':
        query = "match (yrs:YearReferenceSystem {type:'%s'}), (g:GODOT), p = shortestPath((yrs)-[*..15]->(g)) return count(p) as p" % (yrs)
    else:
        query = "match (t:Timeline), (g:GODOT), p = shortestPath((t)-[*..15]->(g)) return count(p) as p"
    results = query_neo4j_db(query)
    for record in results:
        total_hits = record["p"]
    print(total_hits)
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


def get_number_of_nodes():
    """
    returns number of nodes in GODOT graph
    :return: number of nodes (int)
    """
    query = "MATCH (n) RETURN count(*) as n"
    results = query_neo4j_db(query)
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
    for record in results:
        n = record["n"]
    return n


def get_list_of_yrs():
    """
    returns list of yrs in the GODOT graph
    :return: list of yrs
    """
    query = "match (yrs:YearReferenceSystem) return yrs.type as yrs"
    results = query_neo4j_db(query)
    yrs = ['all']
    for record in results:
        yrs.append(record["yrs"])
    return yrs


def write_cyrenaica_path(yrs, apollo_priest, roman_emperor, year, month, day, attestation_uri, date_string):
    """
    adds path for cyrenaica dates according to cyrenaica web form
    :param yrs:
    :param apollo_priest:
    :param roman_emperor:
    :param year:
    :param month:
    :param day:
    :param attestation_uri:
    :param date_string:
    :return:
    """

    if (yrs == "" and month == "" and day == "") or (attestation_uri == "" or date_string == ""):
        return None

    if yrs != "":
        # write path from Timeline node to yrs (including year)
        cypher_cyr = ""

        if yrs != "Eponymous Officials: Apollo Priest (Cyrenaica)":
            cypher_cyr = """
           MATCH (root:Timeline)
           MERGE (root)-[:hasYearReckoningSystem]->(yrs:YearReferenceSystem {type:'%s'})
           """ % yrs
        if yrs == "Regnal: Roman Emperors":
            cypher_cyr += """
           MERGE (yrs)-[:hasCalendarPartial]->(:CalendarPartial {type:'reign', value:'%s'})
           """ % roman_emperor

        # add year number
        # MERGE(yrs) - [: hasCalendarPartial]->(cp1:CalendarPartial {type:'year', value:13})

        # add month/day if specified


    else:
        # only month/day given, no yrs
        pass

    print(cypher_cyr)
