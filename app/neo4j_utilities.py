from app import app
from neo4j.v1 import GraphDatabase, basic_auth
import shortuuid


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
    query = "match (yrs:YearReferenceSystem) return yrs.type as yrs order by yrs"
    results = query_neo4j_db(query)
    yrs = ['All']
    for record in results:
        yrs.append(record["yrs"])
    return yrs


def write_cyrenaica_path(yrs, apollo_priest, roman_emperor, year, month, day, attestation_uri, date_string, title):
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
    :param title:
    :return: GODOT URI (string) or None
    """

    if (yrs == "" and month == "" and day == "") or (attestation_uri == "" or date_string == ""):
        return None

    if yrs == "None" and (month is not None or day is not None):
        cypher_query = _create_cypher_yrs_none(month, day, attestation_uri, title, date_string)
    elif yrs == "Unknown" and year is not None:
        cypher_query = _create_cypher_yrs_unknown(year, month, day, attestation_uri, title, date_string)

    elif yrs == "Eponymous Officials: Apollo Priest (Cyrenaica)":
        cypher_query = """
        MATCH (root:Timeline)
        MERGE (root)-[:hasYearReckoningSystem]->(yrs:YearReferenceSystem {type:'Eponymous officials: Apollo Priest (Cyrenaica)'})
        MERGE (yrs)-[:hasCalendarPartial]->(cp1:CalendarPartial {value:'%s'})
        """ % apollo_priest
        prev_node = "cp1"
    elif yrs == "Regnal: Roman Emperors":
        cypher_query = """
        MATCH (root:Timeline)
        MERGE (root)-[:hasYearReckoningSystem]->(yrs:YearReferenceSystem {type:'Regnal: Roman Emperors'})
        MERGE (yrs)-[:hasCalendarPartial]->(cp1:CalendarPartial {type:'reign', value:'%s'})
        """ % roman_emperor
        prev_node = "cp1"
        if year != "":
            cypher_query += """
            MERGE (cp1)-[:hasCalendarPartial]->(cp2:CalendarPartial {type:'year', value:'%s'})
            """ % year
            prev_node = "cp2"
    elif yrs == "Era: Actian":
        cypher_query = """
        MATCH (root:Timeline)
        MERGE (root)-[:hasYearReckoningSystem]->(yrs:YearReferenceSystem {type:'Era: Actian'})
        MERGE (yrs)-[:hasCalendarPartial]->(cp1:CalendarPartial {type:'year', value:'%s'})
        """ % year
        prev_node = "cp1"
    else:
        print("Fehler")
        return None
    results = query_neo4j_db(cypher_query)
    g = None
    for record in results:
        g = record["g"]
    return g


def _create_cypher_yrs_none(month, day, attestation_uri, title, date_string):
    """
    creates cypher query for none type of yrs
    :param month:
    :param day:
    :param attestation_uri:
    :param title:
    :param date_string:
    :return: cypher query string
    """
    godot_uri = "https://godot.date/id/" + shortuuid.uuid()
    if day is None:
        # only month specified
        cypher_query = """
        MATCH (root:Timeline)--(yrs:YearReferenceSystem {type: 'None'})-[:hasCalendarType]->(ct:CalendarType 
          {type:'Egyptian Calendar'})-[:hasCalendarPartial]->(cp_month:CalendarPartial {type:'month', value:'%s'}),
          (cp_month)-->(g_month:GODOT)
        MERGE (g_month)-[:hasAttestation]->(att:Attestation {uri: '%s', title: '%s', date_string: '%s'})
        RETURN g_month.uri as g
        """ % (month, attestation_uri, title, date_string)
    else:
        # both month and day specified
        cypher_query = """
        MATCH (root:Timeline)--(yrs:YearReferenceSystem {type: 'None'})-[:hasCalendarType]->(ct:CalendarType 
          {type:'Egyptian Calendar'})-[:hasCalendarPartial]->(cp_month:CalendarPartial {type:'month', value:'%s'})
        MERGE (cp_month)-[:hasCalendarPartial]->(cp_day:CalendarPartial {type:'day', value:'%s'})
        MERGE (cp_day)-[:hasGodotUri]->(g_day:GODOT)
          ON CREATE SET g_day.uri='%s'
        MERGE (g_day)-[:hasAttestation]->(att:Attestation {uri: '%s', title: '%s', date_string: '%s'})
        RETURN g_day.uri as g
        """ % (month, day, godot_uri, attestation_uri, title, date_string)
    return cypher_query


def _create_cypher_yrs_unknown(year, month, day, attestation_uri, title, date_string):
    """
    creates cypher query for unknown yrs
    :param year:
    :param month:
    :param day:
    :param attestation_uri:
    :param title:
    :param date_string:
    :return: cypher query string
    """
    godot_uri = "https://godot.date/id/" + shortuuid.uuid()
    if month == "None" and day is None:
        # only year given
        cypher_query = """
        MATCH (root:Timeline)--(yrs:YearReferenceSystem {type: 'Unknown'})
        MERGE (yrs)-[:hasCalendarPartial]->(cp:CalendarPartial {type: 'year', value: '%s'})
        MERGE (cp)-[:hasGodotoUri]->(g:GODOT)
          ON CREATE SET g.uri='%s'
        MERGE (g)-[:hasAttestation]->(att:Attestation {uri: '%s', title: '%s', date_string: '%s'})
        RETURN g.uri as g 
        """ % (year, godot_uri, attestation_uri, title, date_string)
    else:
        if day is None:
            # only month specified
            cypher_query = """
            MATCH (root:Timeline)--(yrs:YearReferenceSystem {type: 'Unknown'})
            MERGE (yrs)-[:hasCalendarPartial]->(cp:CalendarPartial {type: 'year', value: '%s'})
            MERGE (cp)-[:hasCalendarType]->(ct:CalendarType {type: 'Egyptian Calendar'})
            MERGE (ct)-[:hasCalendarPartial]->(cp_month:CalendarPartial {type: 'month', value: '%s'})
            MERGE (cp_month)-[:hasGodotoUri]->(g:GODOT)
              ON CREATE SET g.uri='%s'
            MERGE (g)-[:hasAttestation]->(att:Attestation {uri: '%s', title: '%s', date_string: '%s'})
            RETURN g.uri as g 
            """ % (year, month, godot_uri, attestation_uri, title, date_string)
        else:
            # month & day specified
            cypher_query = """
            MATCH (root:Timeline)--(yrs:YearReferenceSystem {type: 'Unknown'})
            MERGE (yrs)-[:hasCalendarPartial]->(cp:CalendarPartial {type: 'year', value: '%s'})
            MERGE (cp)-[:hasCalendarType]->(ct:CalendarType {type: 'Egyptian Calendar'})
            MERGE (ct)-[:hasCalendarPartial]->(cp_month:CalendarPartial {type: 'month', value: '%s'})
            MERGE (cp_month)-[:hasCalendarPartial]->(cp_day:CalendarPartial {type: 'day', value: '%s'})
            MERGE (cp_day)-[:hasGodotoUri]->(g:GODOT)
              ON CREATE SET g.uri='%s'
            MERGE (g)-[:hasAttestation]->(att:Attestation {uri: '%s', title: '%s', date_string: '%s'})
            RETURN g.uri as g 
            """ % (year, month, day, godot_uri, attestation_uri, title, date_string)
    return cypher_query

