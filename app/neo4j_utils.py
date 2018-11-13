from app import app
from neo4j.v1 import GraphDatabase, basic_auth
import shortuuid
from flask_simplelogin import get_username


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


def get_actian_era_entries():
    """
    return list of dicts (keys: year, godot uri) of all Actian Era nodes
    :return: list of dicts (keys: year, godot uri)
    """
    query = """
    match (yrs1:YearReferenceSystem {type:'Era'})--(yrs2:YearReferenceSystem {type:'Actian'})--(cp_year:CalendarPartial)--(g:GODOT)
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
    print(godot_uri)
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
    if results:
        for record in results:
            label = record["yrs1"]["type"]
            if record["yrs2"]:
                # add placename for eponymous officials
                if record["yrs2"]["place_label"]:
                    label += " - " + record["yrs2"]["type"] + " of " + record["yrs2"]["place_label"]
                else:
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


def get_godot_uri_for_eponymous_official(office_godot_uri, name, wikidata_uri, snap_uri, not_before, not_after):
    """
    creates/returns GODOT URi for eponymou official
    :param name:
    :param wikidata_uri:
    :param snap_uri:
    :param not_before:
    :param not_after:
    :return: godot URI of official
    """
    godot_uri  = "https://godot.date/id/" + shortuuid.uuid()
    query = """
    match (g:GODOT {uri:'%s'})--(yrs:YearReferenceSystem)
    merge (yrs)-[:hasCalendarPartial]->(cp:CalendarPartial {type:'name', value:'%s', wikidata_uri:'%s', snap_uri:'%s', not_before:'%s', not_after:'%s'})
    merge (cp)-[:hasGodotUri]->(g2:GODOT {type:'standard'})
        on create set g2.uri = '%s'
    return g2.uri as g
    """ % (office_godot_uri, _clean_string(name), wikidata_uri, snap_uri, _clean_string(not_before), _clean_string(not_after), godot_uri)
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
    results = query_neo4j_db(query)
    result_dict = {}
    for record in results:
        for (k, v) in record["yrs"].items():
            result_dict[k] = v
    return result_dict


def update_godot_uri_for_eponymous_office(type, place_label, pleiades_uri, wikidata_uri, description):
    """
    updates data for eponymous office specified by combination of type/place_label/pleiades_uri
    :param type:
    :param place_label:
    :param pleiades_uri:
    :param wikidata_uri:
    :param description:
    :return: godot URI of office
    """
    query = """
     match (yrs:YearReferenceSystem {type:'%s', place_label:'%s', pleiades_uri:'%s'})-[:hasGodotUri]->(g:GODOT)
     set yrs.wikidata_uri = '%s', yrs.description = '%s'
     return g.uri as g
     """ % (type, place_label, pleiades_uri, wikidata_uri, _clean_string(description))
    results = query_neo4j_db(query)
    if results:
        for record in results:
            g = record["g"]
    return g


def update_eponymous_official_data(official_godot_id, name, wikidata_uri, snap_uri, not_before, not_after):
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
	set cp.value = '%s', cp.wikidata_uri = '%s', cp.snap_uri = '%s', cp.not_before = '%s', cp.not_after = '%s'
    return cp
    """ % (official_godot_id, name, wikidata_uri, snap_uri, not_before, not_after)
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
    # emperor name

    # consul number
    cos_design = "cos."
    if (consul_designatus):
        cos_design = "cos. design."
    if (consul_number):
        query += """
        match (emperor)--(cp_cos:CalendarPartial {value:'Imperial Consulates'})--(cp_cos_2:CalendarPartial {value:'%s'})--(cp_cos_nr:CalendarPartial {value:'%s'})--(g_cos:GODOT)
        """ % (cos_design, consul_number)
        return_statement += ", g_cos"
    # trib pot number
    if (trib_pot_number):
        query += """
        match (emperor)--(cp_vt_tr_pot:CalendarPartial {value:'Tribunicia Potestas'})--(cp_tp_nr:CalendarPartial {value:'%s'})--(g_tr_pot:GODOT)
        """ % trib_pot_number
        return_statement += ", g_tr_pot as g_tr_pot"
    # imperator acclamation number
    if (imperator_number):
        query += """
        match (emperor)--(cp_imp_acc:CalendarPartial {value:'Imperial Acclamations'})--(cp_imp_acc_2:CalendarPartial {value:'%s'})--(g_imp_acc:GODOT)
        """ % imperator_number
        return_statement += ", g_imp_acc"
    # victory titles

    query += return_statement + " order by emperor.value"
    print(query)
    results = query_neo4j_db(query)
    result_list = []
    for record in results:
        result_dict = {}
        result_dict_emperor = {}
        result_dict_cos = {}
        result_dict_tr_pot = {}
        result_dict_imp_acc = {}

        print(record)

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


def _clean_string(str):
    """
    cleans data entered by user, including escaping
    :param str: string
    :return: string
    """
    str = str.replace("'", "\\'")
    return str
