from app import app
from neo4j.v1 import GraphDatabase, basic_auth
import shortuuid
from flask_simplelogin import get_username
import operator
from functools import reduce
import math
from itertools import combinations
import re
from flask import jsonify


def get_all_roman_emperors():
    """
    returns list of name of Roman emperors for browse data page
    :return: list of names of Roman emperors
    """
    query = """
    match (yrs:YearReferenceSystem {type:'Roman Emperors'})-->(cp:CalendarPartial)
    return cp.value as name
    order by cp.value
    """
    results = query_neo4j_db(query)
    name_list = []
    for res in results:
        name_list.append(res['name'])
    return name_list


def get_all_ptolemies():
    """
        returns list of name of Ptolemies for browse data page
        :return: list of names of Ptolemies
        """
    query = """
        match (yrs:YearReferenceSystem {type:'Ptolemies'})-->(cp:CalendarPartial)
        return cp.value as name
        order by cp.value
        """
    results = query_neo4j_db(query)
    name_list = []
    for res in results:
        name_list.append(res['name'])
    return name_list


def get_regnal_years_for_emperor(yrs2):
    """
    returns list of dictionaries of regnal years of specified Roman emperor
    :param yrs2:
    :return: list of dictionaries (keys: year, godot_uri)
    """
    query = """
    match (yrs:YearReferenceSystem {type:'Roman Emperors'})-->(cp:CalendarPartial {value:'%s'})-->(cp_year:CalendarPartial)-->(g:GODOT)
    return cp_year.value as year, g.uri as godot_uri
    order by toInteger(cp_year.value)
    """ % yrs2
    results = query_neo4j_db(query)
    year_list = []
    for res in results:
        year_list.append({'year':res['year'], 'godot_uri': res['godot_uri'].split("/")[-1]})
    return year_list


def get_regnal_years_for_ptolemy(yrs2):
    """
    returns list of dictionaries of regnal years of specified ptolemaic emperor
    :param yrs2:
    :return: list of dictionaries (keys: year, godot_uri)
    """
    query = """
    match (yrs:YearReferenceSystem {type:'Ptolemies'})-->(cp:CalendarPartial {value:'%s'})-->(cp_year:CalendarPartial)-->(g:GODOT)
    return cp_year.value as year, g.uri as godot_uri
    order by toInteger(cp_year.value)
    """ % yrs2
    results = query_neo4j_db(query)
    year_list = []
    for res in results:
        year_list.append({'year':res['year'], 'godot_uri': res['godot_uri'].split("/")[-1]})
    return year_list


def get_titulature_list_for_emperor(yrs2):
    """
    returns list of titulature parts for specified emperor
    :param yrs2:
    :return:  list of dicts
    """
    query = """
    match (yrs:YearReferenceSystem {type:'Titulature of Roman Emperors'})-->(cp:CalendarPartial {value:'%s'})-->(cp_tit_type:CalendarPartial)
    return cp_tit_type.value as tit_type
    """ % yrs2
    results = query_neo4j_db(query)
    titulature_list = []
    for res in results:
        titulature_list.append(res['tit_type'])
    return titulature_list


def get_titulature_list_entries_for_emperor(yrs2, yrs3):
    """
    returns all entries for given titulature parts (trib.pot, etc.) of specified emperor
    :param yrs2:
    :param yrs3:
    :return: list of dicts (keys: entry, godot_uri)
    """
    query = """
    match (yrs:YearReferenceSystem {type:'Titulature of Roman Emperors'})-->(cp:CalendarPartial {value:'%s'})-->(cp_tit_type:CalendarPartial {value:'%s'})--(cp_entries:CalendarPartial)--(g:GODOT)
    return cp_entries as entry, g
    order by toInteger(cp_entries.value) 
    """ % (yrs2, yrs3)
    results = query_neo4j_db(query)
    titulature_entries_list = []
    for res in results:
        titulature_entries_list.append({'entry': res['entry']['value'], 'godot_uri':res['g']['uri']})
    return titulature_entries_list


def get_titulature_list_entries_for_emperor_last_level(yrs2, yrs3):
    """
    returns list of either imperial consulates or imperial victory titles
    :param yrs2:
    :param yrs3:
    :param yrs4:
    :return: list
    """
    query = """
    match (yrs:YearReferenceSystem {type:'Titulature of Roman Emperors'})-->(cp:CalendarPartial {value:'%s'})-->(cp_tit_type:CalendarPartial {value:'%s'})--(cp_entries:CalendarPartial)--(cp_last_level:CalendarPartial)--(g:GODOT)
    return (cp_entries.value + " " + cp_last_level.value) as entry, g
    order by entry
    """ % (yrs2, yrs3)
    results = query_neo4j_db(query)
    titulature_entries_list = []
    for res in results:
        titulature_entries_list.append({'entry': res['entry'], 'godot_uri': res['g']['uri']})
    return titulature_entries_list


def get_actian_era_year_entries():
    """
    returns list of actian era years
    :return: distinct list of years
    """
    query = """
        match (yrs1:YearReferenceSystem {type:'Era'})--(yrs2:YearReferenceSystem {type:'Actian'})--(cp_year:CalendarPartial)-[*1..5]-(g:GODOT)
        return distinct cp_year.value as year
        order by toInteger(cp_year.value)
        """
    results = query_neo4j_db(query)
    actian_era_entries_list = []
    for res in results:
        actian_era_entries_list.append(res['year'])
    return actian_era_entries_list


def get_actian_era_single_year_entries(year):
    """
    returns list of GODOT URIs for given year
    :param year: int of year in Actian era
    :return: list of godot uris
    """
    query = """
    match (yrs1:YearReferenceSystem {type:'Era'})--(yrs2:YearReferenceSystem {type:'Actian'})--(cp_year:CalendarPartial {value:'%s'})-[*1..5]-(g:GODOT)
    return g.uri as godot_uri
    order by toInteger(cp_year.value)   
    """ % year
    results = query_neo4j_db(query)
    actian_era_entries_list = []
    for res in results:
        date_info = _get_date_info_of_actian_era(res['godot_uri'])
        actian_era_entries_list.append({'godot_uri':res['godot_uri'], 'date_info': date_info})
    return actian_era_entries_list


def get_actian_era_entries():
    """
    return list of dicts (keys: year, godot uri) of all Actian Era nodes
    :return: list of dicts (keys: year, godot uri)
    """
    query = """
    match (yrs1:YearReferenceSystem {type:'Era'})--(yrs2:YearReferenceSystem {type:'Actian'})--(cp_year:CalendarPartial)-[*1..5]-(g:GODOT)
    return cp_year.value as year, g.uri as godot_uri
    order by toInteger(cp_year.value)
    """
    results = query_neo4j_db(query)
    actian_era_entries_list = []
    for res in results:
        actian_era_entries_list.append({'year': res['year'], 'godot_uri': res['godot_uri'].split("/")[-1]})
    return actian_era_entries_list


def get_consulate_entries(yrs, page):
    """
    return list of dicts (keys: consulate, godot_uri) of Roman consulates
    :param yrs:
    :param page:
    :return: list of dicts (keys: consulate, godot_uri)
    """
    limit = 20
    page = int(page) * 20 - 20
    query = """
    match (yrs1:YearReferenceSystem {type:'Roman Consulships'})--(cp_consulate:CalendarPartial)--(g:GODOT)
    return cp_consulate.value as consulate, g.uri as godot_uri
    order by toInteger(g.not_before)
    skip %s limit %s
    """ % (page, limit)
    results = query_neo4j_db(query)
    actian_era_entries_list = []
    for res in results:
        actian_era_entries_list.append({'consulate': res['consulate'], 'godot_uri': res['godot_uri'].split("/")[-1]})
    return actian_era_entries_list


def get_indiction_cycles():
    """
    returns list of indiction years
    :return:
    """
    query="""
    match (t:Timeline)--(yrs:YearReferenceSystem {type:'Cycles'})--(yrs2:YearReferenceSystem {type:'Indiction Cycle'})--(cp:CalendarPartial)--(g:GODOT)
    return cp.value as cycle, g.uri as godot_uri
    order by toInteger(cp.value)
    """
    results = query_neo4j_db(query)
    cycle_list = []
    for res in results:
        cycle_list.append({"year": res['cycle'], "godot_uri": res['godot_uri']})
    return cycle_list


def get_years_of_indicion_cycle(cycle):
    """
    return list of years of given cycle number
    :param cycle: cycle number
    :return: dict of years with godot_uris; key: year number
    """
    cycle = cycle.split()[1]
    query = """
    match (t:Timeline)--(yrs:YearReferenceSystem {type:'Cycles'})--(yrs2:YearReferenceSystem {type:'Indiction Cycle'})--(cp:CalendarPartial {value:'%s'})--(cp_years:CalendarPartial)--(g:GODOT)
    return cp_years.value as year, g.uri as godot_uri
    order by toInteger(cp_years.value)
    """ % cycle
    results = query_neo4j_db(query)
    year_list = []
    for res in results:
        year_list.append({"year": res['year'], "godot_uri": res['godot_uri'].split("/")[-1]})
    return year_list


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
            if " of " in yrs:
                # eponymous official of some place
                # first get place
                eponymous_title = yrs.split(" of ")[0].strip()
                place_label = yrs.split(" of ")[1].strip()
                query = "match (yrs:YearReferenceSystem {type:'%s'})--(yrs2:YearReferenceSystem {type:'%s', place_label: '%s'}), (g:GODOT), p = shortestPath((yrs2)-[*..15]->(g)) return p order by g skip %s limit %s" % (
                    eponymous_title.split(" - ")[0], eponymous_title.split(" - ")[1], place_label, page, limit)
            else:
                query = "match (yrs:YearReferenceSystem {type:'%s'})--(yrs2:YearReferenceSystem {type:'%s'}), (g:GODOT), p = shortestPath((yrs2)-[*..15]->(g)) return p order by g skip %s limit %s" % (
                yrs.split(" - ")[0], yrs.split(" - ")[1], page, limit)
        else:
            query = "match (yrs:YearReferenceSystem {type:'%s'}), (g:GODOT), p = shortestPath((yrs)-[*..15]->(g)) return p skip %s limit %s" % (
            yrs, page, limit)
    else:
        query = "match (t:Timeline), (g:GODOT), p = shortestPath((t)-[*..15]->(g)) return p skip %s limit %s" % (
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
                if k == "uri" and v.startswith('ircyr:'):
                    tmp_arr = v.split(':')
                    if len(tmp_arr) == 2:
                        tmp_dict[k] = "https://ircyr2020.inslib.kcl.ac.uk/en/inscriptions/" + tmp_arr[1] + ".html"
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


def get_number_of_attestations():
    """
    returns number of Attestation nodes in GODOT graph
    :return: number of nodes (int)
    """
    query = "MATCH (n:Attestation) RETURN count(*) as n"
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
    query = """match (t:Timeline)--(yrs1:YearReferenceSystem) 
    optional match (yrs1)--(yrs2:YearReferenceSystem) return yrs1, yrs2"""
    results = query_neo4j_db(query)
    yrs = ['All']
    yrs.append('Roman Consulships')
    if results:
        for record in results:
            label = record["yrs1"]["type"]
            if record["yrs1"]["type"] == "Regnal Years":
                label += " - " + record["yrs2"]["type"]
            elif record["yrs1"]["type"] == "Era":
                label += " - " + record["yrs2"]["type"]
            elif record["yrs1"]["type"] == "Cycles":
                label += " - " + record["yrs2"]["type"]
            yrs.append(label)
    return sorted(set(yrs))


def get_attestation(node_id):
    query = "match (a:Attestation) where id(a) = %s return a" % node_id
    results = query_neo4j_db(query)
    tmp_dict = {}
    for record in results:
        for (k, v) in record["a"].items():
            tmp_dict[k] = v
    return tmp_dict


def update_attestation(node_id, attestation_uri, title, date_string, date_category):
    title = _clean_string(title)
    date_string = _clean_string(date_string)
    query = """
    match (a:Attestation) 
    where id(a) = %s 
    set a.date_string='%s', a.title = '%s', a.uri = '%s', a.date_category = '%s', a.username = '%s', a.last_update = date()
    """ % (node_id, date_string, title, attestation_uri, date_category, get_username())
    results = query_neo4j_db(query)
    if results:
        return results


def delete_attestation(node_id):
    query = "match (a:Attestation)-[r:hasAttestation]-(:GODOT) where id(a) = %s delete a, r" % node_id
    results = query_neo4j_db(query)
    if results:
        return results


def get_eponyms():
    query = """
    match (:YearReferenceSystem {type:'Eponymous officials'})-->(yrs:YearReferenceSystem)--(g:GODOT) 
    where not yrs.pleiades_uri = ""
    return yrs, g.uri as g
    order by yrs.type
    """
    results = query_neo4j_db(query)
    list_of_eponyms = []
    for res in results:
        tmp_dict = {}
        tmp_dict.update({'godot_uri': str(res['g'].split("/")[-1])})
        for (k, v) in res["yrs"].items():
            tmp_dict[k] = v
        list_of_eponyms.append(tmp_dict)
    return list_of_eponyms


def get_eponym_data(godot_id):
    """
    returns all data for this eponymous official
    :param godot_id: string of GODOT ID
    :return: dictionary
    """
    query = """
    match (g:GODOT {uri:'https://godot.date/id/%s'})<--(yrs:YearReferenceSystem) return yrs
    """ % godot_id
    results = query_neo4j_db(query)
    tmp_dict = {}
    for res in results:
        for (k, v) in res["yrs"].items():
            tmp_dict[k] = v
    return tmp_dict


def get_individuals_for_eponym(godot_id):
    """
    returns list of all individuals for this eponymous official
    :param godot_id: string of GODOT ID
    :return: list of dictionaries
    """
    query = """
    match (g:GODOT)--(cp:CalendarPartial)--(yrs:YearReferenceSystem)--(g2:GODOT {uri:'https://godot.date/id/%s'}) 
    return g,cp
    """ % godot_id
    results = query_neo4j_db(query)
    individuals_list = []
    for res in results:
        tmp_dict = {}
        tmp_dict.update({'godot_uri': str(res['g']['uri'])})
        for (k, v) in res["cp"].items():
            tmp_dict[k] = v
        individuals_list.append(tmp_dict)
    return individuals_list


def get_godot_uri_for_eponymous_office(type, place_label, pleiades_uri, wikidata_uri, description):
    """
    creates/returns godot URI for eponymous office specified by combination of type/place_label/pleiades_uri
    :param type:
    :param place_label:
    :param pleiades_uri:
    :param wikidata_uri:
    :param description:
    :return: godot URI of office
    """
    godot_uri  = "https://godot.date/id/" + shortuuid.uuid()
    query = """
    match (yrs:YearReferenceSystem {type: 'Eponymous officials'})
    merge (yrs)-[:hasYearReferenceSystem]->(yrs2:YearReferenceSystem {type:'%s', place_label:'%s', pleiades_uri:'%s', wikidata_uri:'%s', description:'%s'})
    merge (yrs2)-[:hasGodotUri]->(g:GODOT {type:'standard'})
        ON CREATE SET g.uri='%s'
    return g.uri as g
    """ % (_clean_string(type), _clean_string(place_label), pleiades_uri, wikidata_uri, _clean_string(description), godot_uri)
    results = query_neo4j_db(query)
    if results:
        for record in results:
            g = record["g"]
    return g


def get_godot_uri_for_eponymous_official(office_godot_uri, name, identifying_uri_list, not_before, not_after):
    """
    creates/returns GODOT URi for eponymou official
    :param name:
    :param identifying_uri:
    :param not_before:
    :param not_after:
    :return: godot URI of official
    """
    godot_uri  = "https://godot.date/id/" + shortuuid.uuid()
    query = """
    match (g:GODOT {uri:'%s'})--(yrs:YearReferenceSystem)
    merge (yrs)-[:hasCalendarPartial]->(cp:CalendarPartial {type:'name', value:'%s', identifying_uri:%s, not_before:'%s', not_after:'%s'})
    merge (cp)-[:hasGodotUri]->(g2:GODOT {type:'standard'})
        on create set g2.uri = '%s'
    return g2.uri as g
    """ % (office_godot_uri, _clean_string(name), identifying_uri_list, _clean_string(not_before), _clean_string(not_after), godot_uri)
    results = query_neo4j_db(query)
    if results:
        for record in results:
            g = record["g"]
    return g


def get_official_data(official_godot_id):
    """
    return dict with all properties of individual office holder
    :param official_godot_uri:
    :return: dictionary with official data
    """
    query = """
    match (g:GODOT {uri:'https://godot.date/id/%s'})--(cp:CalendarPartial)
    return cp
    """ % official_godot_id
    results = query_neo4j_db(query)
    result_dict = {}
    for record in results:
        for (k, v) in record["cp"].items():
            result_dict[k] = v
    return result_dict

def get_office_data_by_official_id(official_godot_id):
    """
    returns all eponymous data by individual official godot id holding this office
    :param official_godot_id:
    :return: dictionary
    """
    query = """
    match (g:GODOT {uri:'https://godot.date/id/%s'})--(cp:CalendarPartial)--(yrs:YearReferenceSystem)
    return yrs
    """ % official_godot_id
    print(query)
    results = query_neo4j_db(query)
    result_dict = {}
    for record in results:
        for (k, v) in record["yrs"].items():
            result_dict[k] = v
    return result_dict


def update_godot_uri_for_eponymous_office(godot_uri, type, place_label, pleiades_uri, wikidata_uri, description):
    """
    updates data for eponymous office specified by combination of type/place_label/pleiades_uri
    :godot_uri:
    :param type:
    :param place_label:
    :param pleiades_uri:
    :param wikidata_uri:
    :param description:
    :return: godot URI of office
    """
    query = """
     match (yrs:YearReferenceSystem)-[:hasGodotUri]->(g:GODOT {uri:'%s'})
     set yrs.type = '%s', yrs.place_label= '%s', yrs.pleiades_uri= '%s', yrs.wikidata_uri = '%s', yrs.description = '%s' 
     return g.uri as g
     """ % (godot_uri, type, place_label, pleiades_uri, wikidata_uri, _clean_string(description))
    results = query_neo4j_db(query)
    if results:
        for record in results:
            g = record["g"]
    return g


def update_eponymous_official_data(official_godot_id, name, identifying_uri_list, not_before, not_after):
    """
    updates data of official specified by godot_id
    :param official_godot_id:
    :param name:
    :param wikidata_uri:
    :param snap_uri:
    :param not_before:
    :param not_after:
    :return: dict of updated offcial data
    """
    query = """
    match (g:GODOT {uri:'https://godot.date/id/%s'})--(cp:CalendarPartial)
    set cp.value = '%s', cp.identifying_uri = %s, cp.not_before = '%s', cp.not_after = '%s'
    return cp
    """ % (official_godot_id, name, identifying_uri_list, not_before, not_after)
    print(query)
    results = query_neo4j_db(query)
    result_dict = {}
    for record in results:
        for (k, v) in record["cp"].items():
            result_dict[k] = v
    return result_dict


def get_emperors_by_titulature(consul_number, consul_designatus, trib_pot_number, imperator_number, victory_titles_list):
    return_statement = "return emperor"
    query = """
    match (yrs:YearReferenceSystem {type:'Titulature of Roman Emperors'})--(emperor:CalendarPartial) with emperor 
    """
    # consul number
    cos_design = "cos."
    if consul_designatus:
        cos_design = "cos. design."
    if consul_number:
        query += """
        match (emperor)--(cp_cos:CalendarPartial {value:'Imperial Consulates'})--(cp_cos_2:CalendarPartial {value:'%s'})--(cp_cos_nr:CalendarPartial {value:'%s'})--(g_cos:GODOT)
        """ % (cos_design, consul_number)
        return_statement += ", g_cos"
    # trib pot number
    if trib_pot_number:
        query += """
        match (emperor)--(cp_vt_tr_pot:CalendarPartial {value:'Tribunicia Potestas'})--(cp_tp_nr:CalendarPartial {value:'%s'})--(g_tr_pot:GODOT)
        """ % trib_pot_number
        return_statement += ", g_tr_pot as g_tr_pot"
    # imperator acclamation number
    if imperator_number:
        query += """
        match (emperor)--(cp_imp_acc:CalendarPartial {value:'Imperial Acclamations'})--(cp_imp_acc_2:CalendarPartial {value:'%s'})--(g_imp_acc:GODOT)
        """ % imperator_number
        return_statement += ", g_imp_acc"
    # victory titles

    query += return_statement + " order by emperor.value"
    results = query_neo4j_db(query)
    result_list = []
    for record in results:
        result_dict = {}
        result_dict_emperor = {}
        result_dict_cos = {}
        result_dict_tr_pot = {}
        result_dict_imp_acc = {}
        for (k, v) in record["emperor"].items():
            result_dict_emperor[k] = v
            result_dict['emperor'] = result_dict_emperor
        if consul_number:
            for (k, v) in record["g_cos"].items():
                result_dict_cos[k] = v
                result_dict['g_cos'] = result_dict_cos
        if trib_pot_number:
            for (k, v) in record["g_tr_pot"].items():
                result_dict_tr_pot[k] = v
                result_dict['g_tr_pot'] = result_dict_tr_pot
        if imperator_number:
            for (k, v) in record["g_imp_acc"].items():
                result_dict_imp_acc[k] = v
                result_dict['g_imp_acc'] = result_dict_imp_acc
        result_list.append(result_dict)
    return result_list


def get_sub_godot_nodes(godot_uri):
    """
    drill down into graph: queries for following godot nodes (type:synchron) which hold
    information about Roman emperor titulatures
    :param godot_uri: string of godot uri which serves as entry point into graph
    :return: result list of dictionary needed for template detail.html
    """
    query = """
    match (g:GODOT {uri:'%s'})--(cp:CalendarPartial),
    (cp)-->(u)-[*..10]->(g2:GODOT)--(a:Attestation),
    p = shortestPath( (u)-[*..10]-(a) )
    return p
    """ % godot_uri

    results = query_neo4j_db(query)
    result_list = []

    for path in results:
        nodes = path["p"].nodes
        date_info = []
        date_dict = {}
        for n in nodes:
            label = list(n.labels)[0]
            if label == "GODOT":
                for k, v in n.items():
                    if k == "uri":
                        date_dict['godot_uri'] = v
            if label == "Attestation":
                for k, v in n.items():
                    if k == "title":
                        date_dict['title'] = v
                    elif k == "date_string":
                        date_dict['date_string'] = v
            else:
                for k, v in n.items():
                    if v != "standard" and v != "year" and v != "month" and v!= "day" and k != "type" and k != "uri":
                        date_info.append(v)
        date_dict['date_partials'] = date_info
        result_list.append(date_dict)
    # if there's a synchron GODOT node adjecent, follow this pattern also
    # these are Roman Emperor titulature data
    query = "match (g:GODOT {uri:'%s'})-->(g2:GODOT {type:'synchron'}) return g2.uri as synchron_godot_node" % godot_uri
    results = query_neo4j_db(query)
    synchron_godot_node_list = []
    for res in results:
        synchron_godot_node_list.append(res['synchron_godot_node'])

    # iterate over all synchron nodes
    for synchron_godot_node in synchron_godot_node_list:
        query = "match (yrs:YearReferenceSystem {type:'Titulature of Roman Emperors'}),(g:GODOT {uri:'%s'})--(a:Attestation),p = ((yrs)-[*..15]->(g)) return p, a.title as title, a.date_string as date_string" % synchron_godot_node
        results = query_neo4j_db(query)
        paths = []
        if results:
            emperor_data = ""
            attestation_dict = {}
            # get attestation data
            att_title = ""
            att_date_string = ""
            # get date path information
            for record in results:
                att_title = record["title"]
                att_date_string = record["date_string"]
                nodes = record["p"].nodes
                for n in nodes:
                    if list(n.labels)[0] != 'YearReferenceSystem' and list(n.labels)[0] != "GODOT":
                        n_dict = {'label': list(n.labels)[0]}
                        for k, v in n.items():
                            if k == "type" or k == "uri":
                                continue
                            if v == "Tribunicia Potestas":
                                v = "trib. pot."
                            if v == "Imperial Acclamations":
                                v = "imp."
                            elif v == "Imperial Consulates":
                                continue
                            elif v == "Imperial Victory Titles":
                                continue
                            emperor_data += v + " "
                            n_dict[k] = str(v)
                        paths.append(n_dict)
            # name only once at beginning
            emperor_name = ""
            if emperor_data:
                emperor_name = emperor_data.split()[0]
            emperor_data = emperor_name + ": " + re.sub(emperor_name, "", emperor_data)
            if emperor_data:
                tmp_dict = {}
                tmp_dict['godot_uri'] = synchron_godot_node
                tmp_dict['date_partials'] = [emperor_data]
                tmp_dict['title'] = att_title
                tmp_dict['date_string'] = att_date_string
                if tmp_dict['godot_uri'] != "":
                    result_list.append(tmp_dict)
    return result_list


def get_overlapping_periods_from_emperor_titulature_result_set(result_list):
    emperor_data_list = _get_chronological_data_from_emperors_list(result_list)
    result_overlap_list = []
    for emperor in emperor_data_list:
        periods_list = emperor['periods']
        ranges_list = []
        for period in periods_list:
            p_start_jdn = _date_to_jd(format_date_string_not_before(period[0]))
            p_end_jdn = _date_to_jd(format_date_string_not_after(period[1]))
            if p_start_jdn or p_end_jdn:
                if not p_start_jdn:
                    p_start_jdn = 0
                if not p_end_jdn:
                    p_end_jdn = 2458437
                ranges_list.append([p_start_jdn, p_end_jdn])
        number_of_overlaps = 0
        tmp_dict = {}
        tmp_dict['emperor'] = emperor['emperor']
        tmp_dict['result_list_length'] = len(ranges_list)
        tmp_dict['overlap_length'] = len(_get_overlap_of_date_ranges(ranges_list))
        tmp_dict['overlap_range'] = _get_overlap_range_of_date_ranges(ranges_list)
        if not tmp_dict['overlap_range']:
            tmp_dict['partial_overlap_range'] = _get_partial_overlap_range_of_date_ranges(ranges_list)
        result_overlap_list.append(tmp_dict)
    newlist = sorted(result_overlap_list, key=operator.itemgetter('overlap_length'), reverse=True)
    return newlist


def _get_overlap_range_of_date_ranges(ranges_list):
    jdn_set_list = []
    for r in ranges_list:
        # adding .5 as ranges take only integers
        # this gets subtracted later again
        jdn_set_list.append(set(range(int(r[0]+.5), int(r[1]+.5)+1 ))) # adding one to end of range
    if jdn_set_list:
        result = reduce(set.intersection, jdn_set_list) # intersection of ALL ranges; fails if one is not intersected with the rest
        range_min = 0
        range_max = 0
        if len(result) > 0:
            range_min = float(min(result))
            range_max = float(max(result))
            return [jd_to_date(range_min - 0.5), jd_to_date(range_max - 0.5)]
        else:
            return ""


def _get_partial_overlap_range_of_date_ranges(ranges_list):
    jdn_set_list = []
    for r in ranges_list:
        # adding .5 as ranges take only integers
        # this gets subtracted later again
        jdn_set_list.append(set(range(int(r[0]+.5), int(r[1]+.5)+1 ))) # adding one to end of range
    result = [ i[0] & i[1] for i in combinations(jdn_set_list,2) ]
    result_set = []
    for r in result:
        if r:
            range_min = 0
            range_max = 0
            if len(result) > 0:
                range_min = float(min(r))
                range_max = float(max(r))
                result_set.append([jd_to_date(range_min - 0.5), jd_to_date(range_max - 0.5)])
    return result_set


def format_date_string_not_before(p_start):
    bc = ""
    date_list = []
    if p_start.startswith("-"):
        # BC date
        p_start = p_start[1:]
        bc = "-"
    p_start_list = p_start.split("-")
    if len(p_start_list) == 1:
        # only year given => mont/day = 01
        if p_start_list[0] != '':
            date_list = [int(bc + p_start_list[0]), 1, 1]
        else:
            date_list = []
    elif len(p_start_list) == 2:
        # only year/month given => day = 01
        date_list = [int(bc + p_start_list[0]), int(p_start_list[1]), 1]
    else:
        date_list = [int(bc + p_start_list[0]), int(p_start_list[1]), int(p_start_list[2])]
    return date_list


def format_date_string_not_after(p_end):
    bc = ""
    date_list = []
    if p_end.startswith("-"):
        # BC date
        p_end = p_end[1:]
        bc = "-"
    p_start_list = p_end.split("-")
    if len(p_start_list) == 1:
        # only year given => mont/day = 01
        if p_start_list[0] != '':
            date_list = [int(bc + p_start_list[0]), 12, 31]
        else:
            p_end = ""
    elif len(p_start_list) == 2:
        # only year/month given => day = last day of month
        if int(p_start_list[1]) in [1, 3, 5, 7, 8, 10, 12]:
            last_day = 31
        elif int(p_start_list[1]) in [2, 4, 6, 9, 11]:
            last_day = 30
        else:
            last_day = 28
        date_list = [int(bc + p_start_list[0]), int(p_start_list[1]), last_day]
    else:
        date_list = [int(bc + p_start_list[0]), int(p_start_list[1]), int(p_start_list[2])]
    return date_list


def _get_chronological_data_from_emperors_list(result_list):
    emperor = ""
    overlapping_data_list = []
    for result_dict in result_list:
        period_list = []
        periods_dict = {}
        for key in result_dict:
            if key == 'emperor':
                emperor = result_dict['emperor']['value']
                continue
            if 'not_before' in result_dict[key]:
                not_before = result_dict[key]['not_before']
            else:
                not_before = ''
            if  'not_after' in result_dict[key]:
                not_after = result_dict[key]['not_after']
            else:
                not_after = ''
            if "time_span_end" in result_dict[key]:
                not_after = result_dict[key]['time_span_end']
            periods_dict['emperor'] = emperor
            period = [not_before, not_after]
            period_list.append(period)
        periods_dict['periods'] = period_list
        overlapping_data_list.append(periods_dict)
    return overlapping_data_list


def _get_overlap_of_date_ranges(intervals):
    intervals = sorted(intervals)
    l = len(intervals)
    overlaps = []
    for i in range(l):
        for j in range(i + 1, l):
            x = intervals[i]
            y = intervals[j]
            if x[0] == y[0]:
                overlaps.append([x, y])
            elif x[1] == y[1]:
                overlaps.append([x, y])
            elif (x[1] > y[0] and x[0] < y[0]):
                overlaps.append([x, y])
    return overlaps


def _date_to_jd(date_list):
    """
    Algorithm taken from 'Practical Astronomy with your Calculator or Spreadsheet',
        4th ed., Duffet-Smith and Zwart, 2011.
    :param year: int; 1 AD = 1, 1 BC = 0, 2 BC = -1, ...
    :param month: int
    :param day: float (for day fragments)
    :return:
    """
    if len(date_list) == 3:
        (year, month, day) = date_list
        if month == 1 or month == 2:
            yearp = year - 1
            monthp = month + 12
        else:
            yearp = year
            monthp = month
            # this checks where we are in relation to October 15, 1582, the beginning
            # of the Gregorian calendar.
        if ((year < 1582) or
                (year == 1582 and month < 10) or
                (year == 1582 and month == 10 and day < 15)):
            # before start of Gregorian calendar
            B = 0
        else:
            # after start of Gregorian calendar
            A = math.trunc(yearp / 100.)
            B = 2 - A + math.trunc(A / 4.)
        if yearp < 0:
            C = math.trunc((365.25 * yearp) - 0.75)
        else:
            C = math.trunc(365.25 * yearp)
        D = math.trunc(30.6001 * (monthp + 1))
        jd = B + C + D + day + 1720994.5
        return jd
    else:
        return []


def jd_to_date(jd):
    """
    Algorithm taken from 'Practical Astronomy with your Calculator or Spreadsheet',
        4th ed., Duffet-Smith and Zwart, 2011.
    :param jd: jdn number (float)
    :return: iso like date string
    """
    jd = jd + 0.5
    F, I = math.modf(jd)
    I = int(I)
    A = math.trunc((I - 1867216.25) / 36524.25)
    if I > 2299160:
        B = I + 1 + A - math.trunc(A / 4.)
    else:
        B = I
    C = B + 1524
    D = math.trunc((C - 122.1) / 365.25)
    E = math.trunc(365.25 * D)
    G = math.trunc((C - E) / 30.6001)
    day = C - E + F - math.trunc(30.6001 * G)
    if G < 13.5:
        month = G - 1
    else:
        month = G - 13
    if month > 2.5:
        year = D - 4716
    else:
        year = D - 4715
    if year < 0:
        return str(year).zfill(5) + "-" + str(month).zfill(2) + "-" + str(int(day)).zfill(2)
    else:
        return str(year).zfill(4) + "-" + str(month).zfill(2) + "-" + str(int(day)).zfill(2)


def get_date_string_for_godot_uri(godot_uri):
    query = """
    match (g:GODOT {uri:'%s'}) return g.type as type
    """ % godot_uri
    results = query_neo4j_db(query)
    godot_type = ""
    for record in results:
        godot_type = record['type']
    if godot_type == "synchron":
        query = """
        match (g:GODOT {uri:'%s'})--(a:Attestation) , (ct:CalendarType)<--(common_node),
        p = allShortestPaths((g)<-[*..15]-(ct)) 
        with p, common_node, a
        match (t:Timeline), p2 = shortestPath((common_node)-[*..15]-(t))
        return distinct(p) as p, p2 as p2, a.title as title
        """ % godot_uri
        results = query_neo4j_db(query)
        date_string = ""

        for record in results:
            p_nodes = record['p'].nodes
            date_partial_month_str = ""
            date_partial_day_str = ""
            for n in p_nodes:
                label = list(n.labels)[0]
                if label == "CalendarPartial":
                    if n['type'] == "day":
                        date_partial_day_str += n['value']
                    elif n['type'] == "month":
                        date_partial_month_str += n['value']
            # get common date string (like year x of king y)
            p2 = record['p2']
            p2_nodes = p2.nodes
            date_common_str = ""
            for n in p2_nodes:
                label = list(n.labels)[0]
                if label == "CalendarPartial":
                    if n['type'] == "name":
                        date_common_str += n['value']
                    elif n['type'] == "year":
                        date_common_str += "year " + n['value'] + " of "
            date_string += date_common_str+" "+date_partial_month_str+" "+date_partial_day_str+" = "
        return date_string[:-3]
    else:
        # simple date (no synchronism)
        query = """
        match (g:GODOT {uri:'%s'}), (t:Timeline)-->(yrs:YearReferenceSystem),
        p = allShortestPaths((g)<-[*..15]-(yrs))
        return p
        """ % godot_uri
        results = query_neo4j_db(query)
        date_string = ""
        for record in results:
            p_nodes = record['p'].nodes
            for n in p_nodes:
                label = list(n.labels)[0]
                if label == "YearReferenceSystem":
                    date_string += n['type'] + " "
                elif label == "CalendarPartial":
                    date_string += n['type'] + " " + n['value'] + " "
        return date_string.strip()


def get_synchronisms():
    """
    returns dictionary of all synchronisms from different calendar systems
    :return: dict
    """
    query = """
    match (g:GODOT {type:'synchron'})--(a:Attestation), (ct:CalendarType),
    p = shortestPath((g)<-[*..15]-(ct)) 
    return g.uri as godot_uri, ct.type as type, a as attestation
    order by g
    """
    results = query_neo4j_db(query)
    result_dict = {}
    calendar_type_dict = {}
    for record in results:
        if record['godot_uri'] in calendar_type_dict:
            calendar_type_dict[record['godot_uri']].update({"type":record['type']})
        else:
            calendar_type_dict[record['godot_uri']] = {"type":record['type']}
        att_title = record['attestation']['title']
        result_dict[record['godot_uri']] = {"attestation_title": att_title}
    print(calendar_type_dict)
    for godot_uri in result_dict:
        date_string = get_date_string_for_godot_uri(godot_uri)
        result_dict[godot_uri].update({"date_string": date_string})
    # return only synchronisms from two different calendar systems
    result_return_dict = {}
    for element in result_dict:
        if "=" in result_dict[element]['date_string']:
            result_return_dict[element] = result_dict[element]
    return result_return_dict


def get_godot_uri_information_as_json(godot_uri):
    """
    returns information for given gosdot uri as json for API
    :param godsot_uri: string of godot uri
    :return: json
    date_string
    attestations list (each item with date_string, uri, contributor, last update)

    """
    date_string = get_date_string_for_godot_uri(godot_uri)
    return jsonify({"date_string": date_string})


def _clean_string(str):
    """
    cleans data entered by user, including escaping
    :param str: string
    :return: string
    """
    str = str.replace("'", "\\'")
    return str


def _get_date_info_of_actian_era(godot_uri):
    """
    return date information string of actian era year if it exists
    :param godot_uri: string of GODOT URI
    :return: string with date information like "Thot 27"
    """
    query = """
    match path=((cp:CalendarType)-[*2..5]->(g:GODOT {uri:'%s'}))
    return extract(n in nodes(path) | n.value) as str
    """ % godot_uri
    results = query_neo4j_db(query)
    str_buffer = ""
    for res in results:
        date_info = res['str']
        for value in date_info:
            if value is None:
                continue
            str_buffer += value + " "
    return str_buffer

