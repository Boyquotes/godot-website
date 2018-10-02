from app.neo4j_utils import query_neo4j_db
import shortuuid


def write_cyrenaica_single_year(yrs, apollo_priest, roman_emperor, year, month, day, attestation_uri, date_string, title):
    """
    adds path for cyrenaica dates according to cyrenaica web form
    :param yrs:
    :param apollo_priest:
    :param roman_emperor:
    :param year: None (value) or year integer number
    :param month: "None" or month name (str)
    :param day: None (value) or integer number
    :param attestation_uri:
    :param date_string:
    :param title:
    :return: GODOT URI (string) or None
    """
    date_string = _clean_string(date_string)
    title = _clean_string(title)
    if (yrs == "" and year == "" and month == "" and day is None) or (attestation_uri == "" or date_string == ""):
        return None
    if yrs == "None":
        cypher_query = _create_cypher_yrs_none(month, day, attestation_uri, title, date_string)
    elif yrs == "Unknown" and year != "":
        cypher_query = _create_cypher_yrs_unknown(year, month, day, attestation_uri, title, date_string)
    elif yrs == "Era: Actian" and year != "":
        cypher_query = _create_cypher_yrs_actian(year, month, day, attestation_uri, title, date_string)
    elif yrs == "Eponymous Officials: Apollo Priest (Cyrenaica)":
        cypher_query = _create_cypher_yrs_apollo_priest(apollo_priest, month, day, attestation_uri, title, date_string)
    elif yrs == "Regnal: Roman Emperors":
        cypher_query = _create_cypher_yrs_regnal_year_roman_emperor(roman_emperor, year, month, day, attestation_uri, title, date_string)
    else:
        return None
    results = query_neo4j_db(cypher_query)
    g = None
    if results:
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
    if day == "":
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
        MERGE (cp_day)-[:hasGodotUri]->(g_day:GODOT {type:'standard'})
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
    if month == "None" and day == "":
        # only year given
        cypher_query = """
        MATCH (root:Timeline)--(yrs:YearReferenceSystem {type: 'Unknown'})
        MERGE (yrs)-[:hasCalendarPartial]->(cp:CalendarPartial {type: 'year', value: '%s'})
        MERGE (cp)-[:hasGodotUri]->(g:GODOT {type:'standard'})
          ON CREATE SET g.uri='%s'
        MERGE (g)-[:hasAttestation]->(att:Attestation {uri: '%s', title: '%s', date_string: '%s'})
        RETURN g.uri as g 
        """ % (year, godot_uri, attestation_uri, title, date_string)
    else:
        if day == "":
            # only month specified
            cypher_query = """
            MATCH (root:Timeline)--(yrs:YearReferenceSystem {type: 'Unknown'})
            MERGE (yrs)-[:hasCalendarPartial]->(cp:CalendarPartial {type: 'year', value: '%s'})
            MERGE (cp)-[:hasCalendarType]->(ct:CalendarType {type: 'Egyptian Calendar'})
            MERGE (ct)-[:hasCalendarPartial]->(cp_month:CalendarPartial {type: 'month', value: '%s'})
            MERGE (cp_month)-[:hasGodotUri]->(g:GODOT {type:'standard'})
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
            MERGE (cp_day)-[:hasGodotUri]->(g:GODOT {type:'standard'})
              ON CREATE SET g.uri='%s'
            MERGE (g)-[:hasAttestation]->(att:Attestation {uri: '%s', title: '%s', date_string: '%s'})
            RETURN g.uri as g 
            """ % (year, month, day, godot_uri, attestation_uri, title, date_string)
    return cypher_query


def _create_cypher_yrs_actian(year, month, day, attestation_uri, title, date_string):
    """
    creates cypher query for actian year yrs
    :param year:
    :param month:
    :param day:
    :param attestation_uri:
    :param title:
    :param date_string:
    :return: cypher query string
    """
    godot_uri = "https://godot.date/id/" + shortuuid.uuid()
    if month == "None" and day == "":
        # only actian year given, no month/day
        cypher_query = """
            MATCH (root:Timeline)--(:YearReferenceSystem {type: 'Era'})--(yrs:YearReferenceSystem {type:'Actian'})
            MERGE (yrs)-[:hasCalendarPartial]->(cp:CalendarPartial {type: 'year', value: '%s'})
            MERGE (cp)-[:hasGodotUri]->(g:GODOT {type:'standard'})
              ON CREATE SET g.uri='%s'
            MERGE (g)-[:hasAttestation]->(att:Attestation {uri: '%s', title: '%s', date_string: '%s'})
            RETURN g.uri as g 
            """ % (year, godot_uri, attestation_uri, title, date_string)
    else:
        if day == "":
            # only year & month specified
            cypher_query = """
                MATCH (root:Timeline)--(:YearReferenceSystem {type: 'Era'})--(yrs:YearReferenceSystem {type:'Actian'})
                MERGE (yrs)-[:hasCalendarPartial]->(cp:CalendarPartial {type: 'year', value: '%s'})
                MERGE (cp)-[:hasCalendarType]->(ct:CalendarType {type: 'Egyptian Calendar'})
                MERGE (ct)-[:hasCalendarPartial]->(cp_month:CalendarPartial {type: 'month', value: '%s'})
                MERGE (cp_month)-[:hasGodotUri]->(g:GODOT {type:'standard'})
                  ON CREATE SET g.uri='%s'
                MERGE (g)-[:hasAttestation]->(att:Attestation {uri: '%s', title: '%s', date_string: '%s'})
                RETURN g.uri as g 
                """ % (year, month, godot_uri, attestation_uri, title, date_string)
        else:
            # year, month & day specified
            cypher_query = """
                MATCH (root:Timeline)--(:YearReferenceSystem {type: 'Era'})--(yrs:YearReferenceSystem {type:'Actian'})
                MERGE (yrs)-[:hasCalendarPartial]->(cp:CalendarPartial {type: 'year', value: '%s'})
                MERGE (cp)-[:hasCalendarType]->(ct:CalendarType {type: 'Egyptian Calendar'})
                MERGE (ct)-[:hasCalendarPartial]->(cp_month:CalendarPartial {type: 'month', value: '%s'})
                MERGE (cp_month)-[:hasCalendarPartial]->(cp_day:CalendarPartial {type: 'day', value: '%s'})
                MERGE (cp_day)-[:hasGodotUri]->(g:GODOT {type:'standard'})
                  ON CREATE SET g.uri='%s'
                MERGE (g)-[:hasAttestation]->(att:Attestation {uri: '%s', title: '%s', date_string: '%s'})
                RETURN g.uri as g 
                """ % (year, month, day, godot_uri, attestation_uri, title, date_string)
    return cypher_query


def _create_cypher_yrs_apollo_priest(apollo_priest, month, day, attestation_uri, title, date_string):
    """
    creates cypher query for apollo priest yrs
    :param apollo_priest:
    :param month:
    :param day:
    :param attestation_uri:
    :param title:
    :param date_string:
    :return:
    """
    godot_uri = "https://godot.date/id/" + shortuuid.uuid()
    if month == "None" and day == "":
        # only apollo priest given, no month/day
        cypher_query = """
        MATCH (root:Timeline)--(YearReferenceSystem {type: 'Eponymous officials'})--(yrs:YearReferenceSystem {type: 'Apollo Priest (Cyrenaica)'})
        MERGE (yrs)-[:hasCalendarPartial]->(cp1:CalendarPartial {type: 'name', value: '%s'})
        MERGE (cp1)-[:hasGodotUri]->(g:GODOT {type:'standard'})
          ON CREATE SET g.uri='%s'
        MERGE (g)-[:hasAttestation]->(att:Attestation {uri: '%s', title: '%s', date_string: '%s'})
        RETURN g.uri as g 
        """ % (apollo_priest, godot_uri, attestation_uri, title, date_string)
    else:
        if day == "":
            # only apollo priest & month specified
            cypher_query = """
                MATCH (root:Timeline)--(YearReferenceSystem {type: 'Eponymous officials'})--(yrs:YearReferenceSystem {type: 'Apollo Priest (Cyrenaica)'})
                MERGE (yrs)-[:hasCalendarPartial]->(cp1:CalendarPartial {type: 'name', value: '%s'})
                MERGE (cp1)-[:hasCalendarType]->(ct:CalendarType {type: 'Egyptian Calendar'})
                MERGE (ct)-[:hasCalendarPartial]->(cp_month:CalendarPartial {type: 'month', value: '%s'})
                MERGE (cp_month)-[:hasGodotUri]->(g:GODOT {type:'standard'})
                  ON CREATE SET g.uri='%s'
                MERGE (g)-[:hasAttestation]->(att:Attestation {uri: '%s', title: '%s', date_string: '%s'})
                RETURN g.uri as g 
                """ % (apollo_priest, month, godot_uri, attestation_uri, title, date_string)
        else:
            # year, month & day specified
            cypher_query = """
                MATCH (root:Timeline)--(YearReferenceSystem {type: 'Eponymous officials'})--(yrs:YearReferenceSystem {type: 'Apollo Priest (Cyrenaica)'})
                MERGE (yrs)-[:hasCalendarPartial]->(cp1:CalendarPartial {type: 'name', value: '%s'})
                MERGE (cp1)-[:hasCalendarType]->(ct:CalendarType {type: 'Egyptian Calendar'})
                MERGE (ct)-[:hasCalendarPartial]->(cp_month:CalendarPartial {type: 'month', value: '%s'})
                MERGE (cp_month)-[:hasCalendarPartial]->(cp_day:CalendarPartial {type: 'day', value: '%s'})
                MERGE (cp_day)-[:hasGodotUri]->(g:GODOT)
                  ON CREATE SET g.uri='%s'
                MERGE (g)-[:hasAttestation]->(att:Attestation {uri: '%s', title: '%s', date_string: '%s'})
                RETURN g.uri as g 
                """ % (apollo_priest, month, day, godot_uri, attestation_uri, title, date_string)
    return cypher_query


def _create_cypher_yrs_regnal_year_roman_emperor(roman_emperor, year, month, day, attestation_uri, title, date_string):
    """
    creates cypher query for regnal year of Roman emperor
    :param roman_emperor:
    :param year:
    :param month:
    :param day:
    :param attestation_uri:
    :param title:
    :param date_string:
    :return:
    """
    godot_uri = "https://godot.date/id/" + shortuuid.uuid()
    if month == "None" and day == "":
        # only Roman Emperor given, no month/day
        if year != "":
            # only year specified, no month/day
            cypher_query = """
            MATCH (root:Timeline)--(YearReferenceSystem {type: 'Regnal Years'})--(yrs:YearReferenceSystem {type:'Roman Emperors'})
            MERGE (yrs)-[:hasCalendarPartial]->(cp1:CalendarPartial {type: 'name', value: '%s'})
            MERGE (cp1)-[:hasCalendarPartial]->(cp2:CalendarPartial {type: 'year', value: '%s'})
            MERGE (cp2)-[:hasGodotUri]->(g:GODOT {type:'standard'})
              ON CREATE SET g.uri='%s'
            MERGE (g)-[:hasAttestation]->(att:Attestation {uri: '%s', title: '%s', date_string: '%s'})
            RETURN g.uri as g 
            """ % (roman_emperor, year, godot_uri, attestation_uri, title, date_string)
        else:
            # only name of Roman Emperor specified, no year/month/day
            cypher_query = """
            MATCH (root:Timeline)--(YearReferenceSystem {type: 'Regnal Years'})--(yrs:YearReferenceSystem {type:'Roman Emperors'})
            MERGE (yrs)-[:hasCalendarPartial]->(cp1:CalendarPartial {type: 'name', value: '%s'})
            MERGE (cp1)-[:hasGodotUri]->(g:GODOT)
              ON CREATE SET g.uri='%s'
            MERGE (g)-[:hasAttestation]->(att:Attestation {uri: '%s', title: '%s', date_string: '%s'})
            RETURN g.uri as g 
            """ % (roman_emperor, godot_uri, attestation_uri, title, date_string)
    else:
        #
        if day == "":
            # only month specified, no day
            if year != "":
                # year, month specified, no day given
                cypher_query = """
                MATCH (root:Timeline)--(YearReferenceSystem {type: 'Regnal Years'})--(yrs:YearReferenceSystem {type:'Roman Emperors'})
                MERGE (yrs)-[:hasCalendarPartial]->(cp1:CalendarPartial {type: 'name', value: '%s'})
                MERGE (cp1)-[:hasCalendarType]->(ct:CalendarType {type: 'Egyptian Calendar'})
                MERGE (ct)-[:hasCalendarPartial]->(cp2:CalendarPartial {type: 'year', value: '%s'})
                MERGE (cp2)-[:hasCalendarPartial]->(cp3:CalendarPartial {type: 'month', value: '%s'})
                MERGE (cp3)-[:hasGodotUri]->(g:GODOT {type:'standard'})
                  ON CREATE SET g.uri='%s'
                MERGE (g)-[:hasAttestation]->(att:Attestation {uri: '%s', title: '%s', date_string: '%s'})
                RETURN g.uri as g 
                """ % (roman_emperor, year, month, godot_uri, attestation_uri, title, date_string)
            else:
                # month is specified, no year or day
                cypher_query = """
                MATCH (root:Timeline)--(YearReferenceSystem {type: 'Regnal Years'})--(yrs:YearReferenceSystem {type:'Roman Emperors'})
                MERGE (yrs)-[:hasCalendarPartial]->(cp1:CalendarPartial {type: 'name', value: '%s'})
                MERGE (cp1)-[:hasCalendarType]->(ct:CalendarType {type: 'Egyptian Calendar'})
                MERGE (ct)-[:hasCalendarPartial]->(cp2:CalendarPartial {type: 'month', value: '%s'})
                MERGE (cp2)-[:hasGodotUri]->(g:GODOT)
                  ON CREATE SET g.uri='%s'
                MERGE (g)-[:hasAttestation]->(att:Attestation {uri: '%s', title: '%s', date_string: '%s'})
                RETURN g.uri as g 
                """ % (roman_emperor, month, godot_uri, attestation_uri, title, date_string)
        else:
            # month and day specified
            if year != "":
                # year, month, day specified
                cypher_query = """
                MATCH (root:Timeline)--(YearReferenceSystem {type: 'Regnal Years'})--(yrs:YearReferenceSystem {type:'Roman Emperors'})
                MERGE (yrs)-[:hasCalendarPartial]->(cp1:CalendarPartial {type: 'name', value: '%s'})
                MERGE (cp1)-[:hasCalendarPartial]->(cp2:CalendarPartial {type: 'year', value: '%s'})
                MERGE (cp2)-[:hasCalendarType]->(ct:CalendarType {type: 'Egyptian Calendar'})
                MERGE (ct)-[:hasCalendarPartial]->(cp3:CalendarPartial {type: 'month', value: '%s'})
                MERGE (cp3)-[:hasCalendarPartial]->(cp4:CalendarPartial {type: 'day', value: '%s'})
                MERGE (cp4)-[:hasGodotUri]->(g:GODOT {type:'standard'})
                  ON CREATE SET g.uri='%s'
                MERGE (g)-[:hasAttestation]->(att:Attestation {uri: '%s', title: '%s', date_string: '%s'})
                RETURN g.uri as g 
                """ % (roman_emperor, year, month, day, godot_uri, attestation_uri, title, date_string)
            else:
                # month, day specified, no year given
                cypher_query = """
                MATCH (root:Timeline)--(YearReferenceSystem {type: 'Regnal Years'})--(yrs:YearReferenceSystem {type:'Roman Emperors'})
                MERGE (yrs)-[:hasCalendarPartial]->(cp1:CalendarPartial {type: 'name', value: '%s'})
                MERGE (cp1)-[:hasCalendarType]->(ct:CalendarType {type: 'Egyptian Calendar'})
                MERGE (ct)-[:hasCalendarPartial]->(cp2:CalendarPartial {type: 'month', value: '%s'})
                MERGE (cp2)-[:hasCalendarPartial]->(cp3:CalendarPartial {type: 'day', value: '%s'})
                MERGE (cp3)-[:hasGodotUri]->(g:GODOT {type:'standard'})
                  ON CREATE SET g.uri='%s'
                MERGE (g)-[:hasAttestation]->(att:Attestation {uri: '%s', title: '%s', date_string: '%s'})
                RETURN g.uri as g 
                """ % (roman_emperor, month, day, godot_uri, attestation_uri, title, date_string)
    return cypher_query




def write_cyrenaica_emperor_titulature_path(roman_emperor, consul_number, consul_designatus, trib_pot_number, imperator_number, victory_titles, attestation_uri,
                                         date_string, date_title):
    godot_uri_consul_number = ""
    godot_uri_trib_pot_number = ""
    godot_uri_imperator_number = ""
    godot_uri_vitory_titles = ""
    date_string = _clean_string(date_string)
    date_title = _clean_string(date_title)
    target_godot_uris = []
    if consul_number != "":
        target_godot_uris.append(_get_godot_uri_consul_number(roman_emperor, consul_number, consul_designatus))
    if trib_pot_number != "":
        target_godot_uris.append(_get_godot_uri_trib_pot_number(roman_emperor, trib_pot_number))
    if imperator_number != "":
        target_godot_uris.append(_get_godot_uri_imperator_number(roman_emperor, imperator_number))
    if victory_titles:
        target_godot_uris.append(_get_godot_uri_victory_titles(roman_emperor, victory_titles))

    # now we have all godot uris that needs to be connected by a synchron godot uri
    godot_uri = "https://godot.date/id/" + shortuuid.uuid()
    cnt = 1
    query = "match (g:GODOT {type:'synchron'}) ,"
    for g_uri in target_godot_uris:
        query += "(g)<-[:hasGodotUri]-(g%s:GODOT {uri:'%s'})," % (cnt, g_uri)
        cnt += 1
    # remove trailing comma
    query = query[:-1]
    query += "where size( (g)-[:hasGodotUri]-() ) = %s return g.uri as g" % len(target_godot_uris)
    results = query_neo4j_db(query)
    g_synchron_uri = None
    for record in results:
        g_synchron_uri = record["g"]
    if not g_synchron_uri:
        godot_uri = "https://godot.date/id/" + shortuuid.uuid()
        q_match = ""
        q_merge = ""
        query = """
        create(g: GODOT {uri: '%s', type: 'synchron'})
        with g
        """ % godot_uri
        cnt = 1
        for g_uri in target_godot_uris:
            q_match += "match (g%s: GODOT {uri: '%s'})\n" % (cnt, g_uri)
            q_merge += "merge (g)<-[:hasGodotUri]-(g%s)\n" % (cnt)
            cnt += 1
        query += q_match + q_merge + " return g.uri as g"
        results = query_neo4j_db(query)
        if results:
            for record in results:
                g_synchron_uri = record["g"]
    # add attestation info to g_synchron_uri node
    query = """
    match (g_synchron:GODOT {uri:'%s'})
    with g_synchron
    merge (g_synchron)-[:hasAttestation]->(att:Attestation {uri: '%s', title: '%s', date_string: '%s'})
    """ % (g_synchron_uri, attestation_uri, date_title, date_string)
    results = query_neo4j_db(query)
    return g_synchron_uri


def _get_godot_uri_consul_number(roman_emperor, consul_number, consul_designatus):
    consulship_type = "cos."
    if consul_designatus:
        consulship_type = "cos. design."
    godot_uri = "https://godot.date/id/" + shortuuid.uuid()
    query = """
    MATCH (yrs:YearReferenceSystem {type: 'Titulature of Roman Emperors'})-[:hasCalendarPartial]->(cp1:CalendarPartial {value: '%s'})
    MERGE (cp1)-[:hasCalendarPartial]->(cp2:CalendarPartial {type:'Titulature Part', value:'Imperial Consulates'})
    MERGE (cp2)-[:hasCalendarPartial]->(cp3:CalendarPartial {type:'consulship_type', value:'%s'})
    MERGE (cp3)-[:hasCalendarPartial]->(cp4:CalendarPartial {type:'number', value:'%s'}) 
    MERGE (cp4)-[:hasGodotUri]->(g:GODOT {type:'standard'})
                  ON CREATE SET g.uri='%s' 
    RETURN g.uri as g
    """ % (roman_emperor, consulship_type, consul_number, godot_uri)
    results = query_neo4j_db(query)
    if results:
        for record in results:
            g = record["g"]
    return g


def _get_godot_uri_trib_pot_number(roman_emperor, trib_pot_number):
    godot_uri = "https://godot.date/id/" + shortuuid.uuid()
    query = """
    MATCH (yrs:YearReferenceSystem {type: 'Titulature of Roman Emperors'})-[:hasCalendarPartial]->(cp1:CalendarPartial {value: '%s'})
    MERGE (cp1)-[:hasCalendarPartial]->(cp2:CalendarPartial {type:'Titulature Part', value:'Tribunicia Potestas'})
    MERGE (cp2)-[:hasCalendarPartial]->(cp3:CalendarPartial {value:'%s'})
    MERGE (cp3)-[:hasGodotUri]->(g:GODOT {type:'standard'})
                  ON CREATE SET g.uri='%s' 
    RETURN g.uri as g
    """ % (roman_emperor, trib_pot_number, godot_uri)
    results = query_neo4j_db(query)
    if results:
        for record in results:
            g = record["g"]
    return g


def _get_godot_uri_imperator_number(roman_emperor, acc_number):
    godot_uri = "https://godot.date/id/" + shortuuid.uuid()
    query = """
    MATCH (yrs:YearReferenceSystem {type: 'Titulature of Roman Emperors'})-[:hasCalendarPartial]->(cp1:CalendarPartial {value: '%s'})
    MERGE (cp1)-[:hasCalendarPartial]->(cp2:CalendarPartial {type:'Titulature Part', value:'Imperial Acclamations'})
    MERGE (cp2)-[:hasCalendarPartial]->(cp3:CalendarPartial {value:'%s'})
    MERGE (cp3)-[:hasGodotUri]->(g:GODOT {type:'standard'})
                  ON CREATE SET g.uri='%s' 
    RETURN g.uri as g
    """ % (roman_emperor, acc_number, godot_uri)
    results = query_neo4j_db(query)
    if results:
        for record in results:
            g = record["g"]
    return g


def _get_godot_uri_victory_titles(roman_emperor, victory_titles):
    # if only one victory titles is chosen, return standard GODOT URI
    # otherwise create new synchron GODOT node
    if len(victory_titles) == 1:
        return _get_standard_godot_uri_victory_title(roman_emperor, victory_titles)
    else:
        return _get_synchron_godot_uri_victory_titles(roman_emperor, victory_titles)


def _get_standard_godot_uri_victory_title(roman_emperor, victory_titles):
    godot_uri = "https://godot.date/id/" + shortuuid.uuid()
    title = victory_titles[0]
    title_label = ""
    title_nr = ""
    for token in title.split():
        if token.isdigit():
            title_nr = token
        else:
            title_label += token + " "
    title_label = title_label.strip()
    query = """
    MATCH (yrs:YearReferenceSystem {type: 'Titulature of Roman Emperors'})-[:hasCalendarPartial]->(cp1:CalendarPartial {value: '%s'})
    MERGE (cp1)-[:hasCalendarPartial]->(cp2:CalendarPartial {type:'Titulature Part', value:'Imperial Victory Titles'})
    MERGE (cp2)-[:hasCalendarPartial]->(cp3:CalendarPartial {type:'title', value:'%s'})
    MERGE (cp3)-[:hasCalendarPartial]->(cp4:CalendarPartial {type:'number', value:'%s'})
    MERGE (cp4)-[:hasGodotUri]->(g:GODOT {type:'standard'})
               ON CREATE SET g.uri='%s' 
    RETURN g.uri as g
    """ % (roman_emperor, title_label, title_nr, godot_uri)
    results = query_neo4j_db(query)
    if results:
        for record in results:
            return record["g"]


def _get_synchron_godot_uri_victory_titles(roman_emperor, victory_titles):
    godot_uris_victory_titles = _get_godot_uris_victory_titles(roman_emperor, victory_titles)
    # find synchron type GODOT node for all GODOT URIs in list godot_uris_victory_titles
    # create if it not exists
    cnt = 1
    query = "match (g:GODOT {type:'synchron'}) ,"
    for g_uri in godot_uris_victory_titles:
        query += "(g)<-[:hasGodotUri]-(g%s:GODOT {uri:'%s'})," % (cnt, g_uri)
        cnt += 1
    # remove trailing comma
    query = query[:-1]
    query += " where size( (g)<--() ) = %s return g.uri as g" % len(godot_uris_victory_titles)
    results = query_neo4j_db(query)
    g_synchron_uri = None
    for record in results:
        g_synchron_uri = record["g"]
    if not g_synchron_uri:
        godot_uri = "https://godot.date/id/" + shortuuid.uuid()
        q_match = ""
        q_merge = ""
        query = """
        create(g: GODOT {uri: '%s', type: 'synchron'})
        with g
        """ % godot_uri
        cnt = 1
        for g_uri in godot_uris_victory_titles:
            q_match += "match (g%s: GODOT {uri: '%s'})\n" % (cnt, g_uri)
            q_merge += "merge (g)<-[:hasGodotUri]-(g%s)\n" % (cnt)
            cnt += 1
        query += q_match + q_merge + " return g.uri as g"
        results = query_neo4j_db(query)
        if results:
            for record in results:
                return record["g"]
    else:
        return g_synchron_uri


def _get_godot_uris_victory_titles(roman_emperor, victory_titles):
    godot_uris_victory_titles = []
    for title in victory_titles:
        godot_uri = "https://godot.date/id/" + shortuuid.uuid()
        title_label = ""
        title_nr = ""
        for token in title.split():
            if token.isdigit():
                title_nr = token
            else:
                title_label += token + " "
        title_label = title_label.strip()
        query = """
        MATCH (yrs:YearReferenceSystem {type: 'Titulature of Roman Emperors'})-[:hasCalendarPartial]->(cp1:CalendarPartial {value: '%s'})
        MERGE (cp1)-[:hasCalendarPartial]->(cp2:CalendarPartial {type:'Titulature Part', value:'Imperial Victory Titles'})
        MERGE (cp2)-[:hasCalendarPartial]->(cp3:CalendarPartial {type:'title', value:'%s'})
        MERGE (cp3)-[:hasCalendarPartial]->(cp4:CalendarPartial {type:'number', value:'%s'})
        MERGE (cp4)-[:hasGodotUri]->(g:GODOT {type:'standard'})
                      ON CREATE SET g.uri='%s' 
        RETURN g.uri as g
        """ % (roman_emperor, title_label, title_nr, godot_uri)
        results = query_neo4j_db(query)
        if results:
            for record in results:
                godot_uris_victory_titles.append(record["g"])

    return godot_uris_victory_titles

def _clean_string(str):
    """
    cleans data entered by user, including escaping
    :param str: string
    :return: string
    """
    str = str.replace("'", "\\'")
    return str
