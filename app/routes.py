from flask import render_template, request, jsonify, redirect
from flask_simplelogin import login_required
from app import app
from app.forms import RomanConsularDating, CyrenaicaYears, AttestationUpdate, AttestationDelete, CyrenaicaRomanImperialTitulature, SearchRomanConsulate, EgyptianCalendarLatePeriod, EgyptianCalendarPtolemies, EgyptianCalendarRomanEmperors, RomanImperialDating, EponymOffice, EponymOfficial
from app.convert import Convert_roman_calendar
from app.EgyptianCalendarDate import EgyptianCalendarDate
from app.neo4j_utils import *
from app.cyrenaica import write_cyrenaica_single_year, write_cyrenaica_emperor_titulature_path, get_snap_uri_for_lgpn
import simplejson as json
from app.openrefine_utils import search, get_openrefine_metadata
import requests
import json


@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/browse/synchronisms')
def browse_synchronsims():
    synchronisms_list = get_synchronisms()
    return render_template('browse_synchronisms.html', title='Browse Synchronisms', synchronisms_list=synchronisms_list)


@app.route('/browse', defaults={'yrs': 'All', 'yrs2': 1, 'yrs3':'', 'yrs4':''})
@app.route('/browse/<yrs>', defaults={'yrs2': 1, 'yrs3':'', 'yrs4':''})
@app.route('/browse/<yrs>/<yrs2>', defaults={'yrs3':'', 'yrs4':''})
@app.route('/browse/<yrs>/<yrs2>/<yrs3>', defaults={'yrs4':''})
@app.route('/browse/<yrs>/<yrs2>/<yrs3>/<yrs4>')
def browse(yrs, yrs2, yrs3, yrs4):
    list_of_yrs = get_list_of_yrs()
    if yrs == "Regnal Years - Roman Emperors":
        if yrs2 == 1:
            # show list of emperors names
            emperors_list = get_all_roman_emperors()
            return render_template('browse_emperors.html', title='Browse Data', browse_data=emperors_list, list_of_yrs=list_of_yrs, yrs=yrs, period="Roman Emperors")
        else:
            # show all regnal years of specified ruler
            emperors_list = get_all_roman_emperors()
            regnal_years_list = get_regnal_years_for_emperor(yrs2)
            return render_template('browse_emperors_detail.html', title='Browse Data', browse_data=emperors_list,
                                   list_of_yrs=list_of_yrs, yrs=yrs, yrs2=yrs2, regnal_years_list=regnal_years_list, period="Roman Emperors")

    elif yrs == "Regnal Years - Ptolemies":
        if yrs2 == 1:
            # show list of Ptolemies names
            names_list = get_all_ptolemies()
            return render_template('browse_emperors.html', title='Browse Data', browse_data=names_list, list_of_yrs=list_of_yrs, yrs=yrs, period="Ptolemies")
        else:
            # show all regnal years of specified ruler
            emperors_list = get_all_ptolemies()
            regnal_years_list = get_regnal_years_for_ptolemy(yrs2)
            return render_template('browse_emperors_detail.html', title='Browse Data', browse_data=emperors_list,
                                   list_of_yrs=list_of_yrs, yrs=yrs, yrs2=yrs2, regnal_years_list=regnal_years_list, period="Ptolemies")
    elif yrs == "Era - Actian":
        if yrs2 == 1:
            browse_data = get_actian_era_year_entries()
            total_hits = get_browse_data_number_of_results(yrs)
            return render_template('browse_actian_era.html', title='Browse Data', browse_data=browse_data, list_of_yrs=list_of_yrs,
                               yrs=yrs, page=yrs2, total_hits=total_hits)
        else:
            # show entries for given year only
            browse_data = get_actian_era_single_year_entries(yrs2)
            total_hits = get_browse_data_number_of_results(yrs)
            return render_template('browse_actian_era_year.html', title='Browse Data', browse_data=browse_data,
                                   list_of_yrs=list_of_yrs,
                                   yrs=yrs, year=yrs2, total_hits=total_hits)


    elif yrs == "Roman Consulships":
        browse_data = get_consulate_entries(yrs, yrs2)
        total_hits = get_browse_data_number_of_results(yrs)
        return render_template('browse_consulates.html', title='Browse Data', browse_data=browse_data,
                               list_of_yrs=list_of_yrs,
                               yrs=yrs, page=yrs2, total_hits=total_hits)
    elif yrs == "Eponymous officials":
        if yrs2 == 1:
            # show list of all eponym. officials
            eponyms_list = get_eponyms()
            return render_template('browse_eponymous_offices.html', title='Browse Data', browse_data=eponyms_list,
                                   list_of_yrs=list_of_yrs, yrs=yrs, period="Eponymous Officials")
        else:
            # show individuals of given eponym. official
            eponyms_list = get_eponyms()
            return render_template('browse_eponymous_offices.html', title='Browse Data', browse_data=eponyms_list,
                                   list_of_yrs=list_of_yrs, yrs=yrs, period="Eponymous Officials")


    elif yrs == "Titulature of Roman Emperors":
        if yrs2 == 1:
            # show list of emperors names
            emperors_list = get_all_roman_emperors()
            return render_template('browse_emperors_titulature.html', title='Browse Data', browse_data=emperors_list, list_of_yrs=list_of_yrs, yrs=yrs)
        elif yrs3 == '':
            # show list of available titulature parts for specified emperor
            emperors_list = get_all_roman_emperors()
            emperor_titulature_list = get_titulature_list_for_emperor(yrs2)
            return render_template('browse_emperors_titulature_list.html', title='Browse Data', browse_data=emperors_list,
                                   list_of_yrs=list_of_yrs, yrs=yrs, yrs2=yrs2, emperor_titulature_list=emperor_titulature_list)
        elif yrs3 == 'Imperial Consulates' or yrs3 == 'Imperial Victory Titles':
            # add another level of information to drilldown
            emperors_list = get_all_roman_emperors()
            emperor_titulature_list = get_titulature_list_for_emperor(yrs2)
            emperor_titulature_list_entries = get_titulature_list_entries_for_emperor(yrs2, yrs3)
            emperor_titulature_list_entries_last_level = get_titulature_list_entries_for_emperor_last_level(yrs2, yrs3)
            return render_template('browse_emperors_titulature_list_entries_last_level.html', title='Browse Data',
                                   browse_data=emperors_list,
                                   list_of_yrs=list_of_yrs, yrs=yrs, yrs2=yrs2, yrs3=yrs3,
                                   emperor_titulature_list=emperor_titulature_list,
                                   emperor_titulature_list_entries=emperor_titulature_list_entries,
                                   emperor_titulature_list_entries_last_level=emperor_titulature_list_entries_last_level)
        else:
            # show list entries of given titulature parts for specified emperor
            emperors_list = get_all_roman_emperors()
            emperor_titulature_list = get_titulature_list_for_emperor(yrs2)
            emperor_titulature_list_entries = get_titulature_list_entries_for_emperor(yrs2, yrs3)
            return render_template('browse_emperors_titulature_list_entries.html', title='Browse Data',
                                   browse_data=emperors_list,
                                   list_of_yrs=list_of_yrs, yrs=yrs, yrs2=yrs2, yrs3=yrs3,
                                   emperor_titulature_list=emperor_titulature_list, emperor_titulature_list_entries=emperor_titulature_list_entries)
    elif yrs == "Cycles - Indiction Cycle":
        # show list of year numbers
        cycles_list = get_indiction_cycles()
        return render_template('browse_indiction_cycles_years.html', title='Browse Data', browse_data=cycles_list, list_of_yrs=list_of_yrs, yrs=yrs, period="Indiction Years (311 AD - 704 AD)")
    else:
        browse_data = get_browse_data(yrs, yrs2)
        total_hits = get_browse_data_number_of_results(yrs)
        return render_template('browse.html', title='Browse Data', browse_data=browse_data, list_of_yrs=list_of_yrs,
                               yrs=yrs, page=yrs2, total_hits=total_hits)


@app.route('/contact')
def contact():
    number_of_nodes = get_number_of_nodes()
    number_of_relations = get_number_of_relations()
    number_of_godot_uris = get_number_of_godot_uris()
    number_of_attestations = get_number_of_attestations()
    return render_template('contact.html', title='Contact', number_of_nodes=number_of_nodes,
                           number_of_relations=number_of_relations, number_of_godot_uris=number_of_godot_uris, number_of_attestations=number_of_attestations)


@app.route('/about')
def about():
    return render_template('about.html', title='About GODOT', about_text='About GODOT')


@app.route('/data/edh')
def data_edh():
    return render_template('data_edh.html', title='GODOT Data: Epigraphic Database Heidelberg', data_text='GODOT Data: Epigraphic Database Heidelberg')


@app.route('/data/tm')
def data_tm():
    return render_template('data_tm.html', title='GODOT Data: Trismegistos', data_text='GODOT Data: Trismegistos')


@app.route('/data/ircyr')
def data_ircyr():
    return render_template('data_ircyr.html', title='GODOT Data: IRCyr', data_text='GODOT Data: IRCyr')


@app.route('/data')
def data():
    return render_template('data.html', title='GODOT Data', data_text='GODOT Data')


@app.route('/id/<godot_uri>')
def display_godot_uri(godot_uri):
    # get data/path and attestation links for this GODOT URI as list of dicts
    paths = get_godot_path("https://godot.date/id/" + godot_uri)
    # some info needn't be displayed on detail view page
    date_dict = {}
    path_list = []
    for p_dict in paths:
        if p_dict['label'] == 'GODOT' and p_dict['type'] == 'synchron':
            continue
        else:
            path_list.append(p_dict)
    paths = path_list
    attestations = get_attestations("https://godot.date/id/" + godot_uri)
    sub_godot_nodes = get_sub_godot_nodes("https://godot.date/id/" + godot_uri)
    if paths:
        return render_template('detail.html', title='Detail view', id=godot_uri, paths=paths, attestations=attestations, sub_godot_nodes=sub_godot_nodes)
    else:
        return render_template('404.html'), 404


@app.route('/id/<godot_uri>/<node_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_attestation_data(godot_uri, node_id):
    form = AttestationUpdate()
    date_category = form.date_category.data
    date_categories = ['', 'Uncategorised', 'Date of Death', 'Date of Birth', 'Date of Document', 'Date of Recording', 'Date of Action', 'Date of Office', 'Recurring Date of Action', 'Roman Emperor Titulature']
    if form.validate_on_submit():
        attestation_uri = form.attestation_uri.data
        title = form.title.data
        date_string = form.date_string.data
        date_category = form.date_category.data
        if update_attestation(node_id, attestation_uri, title, date_string, date_category):
            return redirect("/id/" + godot_uri)
    paths = get_godot_path("https://godot.date/id/" + godot_uri)
    # some info needn't be displayed on detail view page
    path_list = []
    for p_dict in paths:
        if p_dict['label'] == 'GODOT' and p_dict['type'] == 'synchron':
            continue
        else:
            path_list.append(p_dict)
    paths = path_list
    attestation = get_attestation(node_id)
    if paths:
        return render_template('update_attestation_data.html', title='Edit Attestation Data', id=godot_uri, paths=paths, attestations=attestation, date_categories=date_categories, form=form)
    else:
        return render_template('404.html'), 404


@app.route('/id/<godot_uri>/<node_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_attestation_node(godot_uri, node_id):
    form = AttestationDelete()
    if form.validate_on_submit():
        if delete_attestation(node_id):
            return redirect("/id/" + godot_uri)
    paths = get_godot_path("https://godot.date/id/" + godot_uri)
    # some info needn't be displayed on detail view page
    path_list = []
    for p_dict in paths:
        if p_dict['label'] == 'GODOT' and p_dict['type'] == 'synchron':
            continue
        else:
            path_list.append(p_dict)

    paths = path_list
    attestation = get_attestation(node_id)
    if paths:
        return render_template('delete_attestation_data.html', title='Delete Attestation Data', id=godot_uri, paths=paths, attestations=attestation, form=form)
    else:
        return render_template('404.html'), 404


@app.route('/convert/roman_consuls', methods=['GET', 'POST'])
def roman_consuls():
    form = RomanConsularDating()
    if form.consulship.data is not None:
        # date validation: some date combinations are not valid

        #
        # convert date from roman calendar with consulship
        # get year from form.consulship.data (number at beginning of string until colon)
        year = form.consulship.data.split(':')[0]
        converted_date = Convert_roman_calendar.consulship(
            form.day_number.data, form.day_ref.data, form.months.data, year)
        result_string = converted_date
        consulate = form.consulship.data
        if '|' in form.consulship.data:
            consul_label, godot_uri = form.consulship.data.split('|')
            day_number_label = Convert_roman_calendar.get_day_number_label(form.day_number.data)
            # return conversion result to template
            return render_template('roman_consuls_result.html', title='Roman Consuls', consulship=consul_label,
                                   day_ref=form.day_ref.data, day_number=day_number_label, month=form.months.data,
                                   result=result_string)
    return render_template('roman_consuls.html', title='Roman Consular Dating', form=form)


@app.route('/tools/identify/roman_emperors', methods=['GET', 'POST'])
def roman_emperors():
    form = RomanImperialDating()
    if form.validate_on_submit():
        consul_number = form.consul_number.data
        consul_designatus = form.consul_designatus.data
        trib_pot_number = form.trib_pot_number.data
        imperator_number = form.imperator_number.data
        victory_titles_list = form.victory_titles.data
        if consul_number or trib_pot_number or imperator_number or victory_titles_list:
            result_list = get_emperors_by_titulature( consul_number, consul_designatus, trib_pot_number, imperator_number, victory_titles_list)
            result_list_overlap = get_overlapping_periods_from_emperor_titulature_result_set(result_list)
            return render_template('roman_emperors_result.html', title='Identify Roman Emperor by Titulature - Results', header="Identify Roman Emperor by Titulature - Results", form=form, result_list=result_list, result_list_overlap=result_list_overlap)
    return render_template('roman_emperors.html', title='Identify Roman Emperor by Titulature', form=form, header="Identify Roman Emperor by Titulature")


@app.route('/convert/egyptian/late_period', methods=['GET', 'POST'])
def convert_egyptian_late_period():
    form = EgyptianCalendarLatePeriod()
    if form.validate_on_submit():
        reign = form.late_period_pharaos.data
        year = form.year.data
        month = form.egyptian_calendar_months.data
        day = form.day.data
        lp_date = EgyptianCalendarDate('latePeriod', reign, year, month, day)
        converted_date_json = lp_date.convert_to_julian()
        return render_template('convert_egyptian_late_period_result.html',
            reign=reign, year=year, month=month, day=day, response=converted_date_json)
    return render_template('convert_egyptian_late_period.html', form=form)


@app.route('/convert/egyptian/ptolemies', methods=['GET', 'POST'])
def convert_egyptian_ptolemies():
    form = EgyptianCalendarPtolemies()
    if form.validate_on_submit():
        reign = form.ptolemaic_pharaos.data
        year = form.year.data
        month = form.egyptian_calendar_months.data
        day = form.day.data
        ptolemaic_date = EgyptianCalendarDate('ptolemies', reign, year, month, day)
        converted_date_json = ptolemaic_date.convert_to_julian()
        return render_template('convert_egyptian_ptolemies_result.html',
            reign=reign, year=year, month=month, day=day, response=converted_date_json)
    return render_template('convert_egyptian_ptolemies.html', form=form)


@app.route('/convert/egyptian/roman_emperors', methods=['GET', 'POST'])
def convert_egyptian_roman_emperors():
    form = EgyptianCalendarRomanEmperors()
    if form.validate_on_submit():
        reign = form.roman_emperors.data
        year = form.year.data
        month = form.egyptian_calendar_months.data
        day = form.day.data
        roman_emperor_date = EgyptianCalendarDate('romanEmperors', reign, year, month, day)
        converted_date_json = roman_emperor_date.convert_to_julian()
        return render_template('convert_egyptian_roman_emperors_result.html',
            reign=reign, year=year, month=month, day=day, response=converted_date_json)
    return render_template('convert_egyptian_roman_emperors.html', form=form)


@app.route('/cyrenaica/roman_imperial_titulature', methods=['GET', 'POST'])
@login_required
def cyrenaica_roman_emperor_titulature():
    form = CyrenaicaRomanImperialTitulature()
    if form.validate_on_submit():
        roman_emperor = form.roman_emperors.data
        consul_number = form.consul_number.data
        consul_designatus = form.consul_designatus.data
        trib_pot_number = form.trib_pot_number.data
        imperator_number = form.imperator_number.data
        victory_titles = form.victory_titles.data
        date_category = form.date_category.data
        attestation_uri = form.attestation_uri.data
        date_string = form.date_string.data
        date_title = form.title.data
        godot_uri = write_cyrenaica_emperor_titulature_path(roman_emperor, consul_number, consul_designatus, trib_pot_number, imperator_number, victory_titles, attestation_uri,
                                         date_string, date_title, date_category)
        return render_template('cyrenaica_emperors_result.html',
                               title='Cyrenaica Roman Imperial Titulature',
                               attestation_uri=attestation_uri,
                               date_string=date_string,
                               date_title=date_title,
                               roman_emperor=roman_emperor,
                               consul_number=consul_number,
                               consul_designatus=consul_designatus,
                               trib_pot_number=trib_pot_number,
                               imperator_number=imperator_number,
                               victory_titles=victory_titles,
                               godot_uri=godot_uri.split("/")[-1],
                               date_category=date_category,
                               form=form)
    return render_template('cyrenaica_emperors.html', title='Cyrenaica Roman Imperial Titulature', form=form)


@app.route('/cyrenaica/single_year', methods=['GET', 'POST'])
@login_required
def cyrenaica_years():
    form = CyrenaicaYears()
    if form.validate_on_submit():
        yrs = form.year_reference_system.data
        apollo_priest = form.apollo_priests_cyrenaica.data
        roman_emperor = form.roman_emperors.data
        year = form.year.data
        month = form.egyptian_calendar_months.data
        day = form.day.data
        date_category = form.date_category.data
        attestation_uri = form.attestation_uri.data
        date_string = form.date_string.data
        date_title = form.title.data
        godot_uri = write_cyrenaica_single_year(yrs, apollo_priest, roman_emperor, year, month, day, attestation_uri,
                                                date_string, date_title, date_category)
        if yrs == "Eponymous Officials: Apollo Priest (Cyrenaica)":
            roman_emperor = ""
        elif yrs == "Regnal: Roman Emperors":
            apollo_priest = ""
        else:
            apollo_priest = ""
            roman_emperor = ""
        if godot_uri:
            return render_template('cyrenaica_years_result.html', title='Cyrenaica Year Dating', yrs=yrs,
                               apollo_priest=apollo_priest, roman_emperor=roman_emperor, year=year, month=month,
                               day=day, attestation_uri=attestation_uri, date_string=date_string, date_category=date_category, date_title=date_title, godot_uri=godot_uri.split("/")[-1])
    return render_template('cyrenaica_years.html', title='Cyrenaica Year Dating', form=form)


@app.route('/tools/openrefine')
def tools_openrefine():
    return render_template('tools_openrefine.html', title="Tools: OpenRefine")


@app.route('/tools/api')
def tools_api():
    return render_template('tools_api.html', title="Tools: API")


@app.route('/api/v1/query', methods=['GET', 'POST'])
def api_v1():
    godot_uri = request.args.get('id')
    resp_dict = {}
    date_string = get_date_string_for_godot_uri(godot_uri)
    attestations = get_attestations(godot_uri)
    attestations_list = []
    for att in attestations:
        attestations_list.append({'title':att['title'], 'uri':att['uri'], 'last_update':str(att['last_update']), 'date_string':att['date_string'], 'username':att['username'],})
    resp_dict['attestations'] = attestations_list
    resp_dict['date_translation'] = date_string
    resp_dict_json = jsonify(resp_dict)
    resp_dict_json.headers.add('Access-Control-Allow-Origin', '*')
    return resp_dict_json


@app.route('/tools/identify/consulate', methods=['GET', 'POST'])
def tools_search_consulate():
    form = SearchRomanConsulate()
    if form.validate_on_submit():
        if "|" in form.consulship.data:
            godot_uri = form.consulship.data.split('|')[1].strip()
            consulate = form.consulship.data.split('|')[0].strip()
            attestations = get_attestations(godot_uri)
            property_dict = get_godot_node_properties(godot_uri)
            return render_template('search_consulate_result.html', attestations=attestations, consulate=consulate, godot_uri=godot_uri, property_dict=property_dict, form=form)
    return render_template('search_consulate.html', title="Tools: Search Roman Consulate", form=form)


def _jsonpify(obj):
    try:
        callback = request.args['callback']
        response = app.make_response("%s(%s)" % (callback, json.dumps(obj)))
        response.mimetype = "text/javascript"
        return response
    except KeyError:
        return jsonify(obj)


@app.route("/api/openrefine/reconcile", methods=['POST', 'GET'])
def reconcile():
    query = request.args.get('query')
    queries = request.form.get('queries')
    if query:
        if query.startswith("{"):
            query = json.loads(query)['query']
        results = search(query)
        return _jsonpify({"result": results})
    if queries:
        queries = json.loads(queries)
        results = {}
        for (key, query) in queries.items():
            results[key] = {"result": app.search(query['query'])}
        return _jsonpify(results)
    return _jsonpify(get_openrefine_metadata())


@app.route('/eponymous_office/add', methods=['GET', 'POST'])
def eponymous_office_add():
    form = EponymOffice()
    if form.validate_on_submit():
        description = form.description.data
        wikidata_uri = form.wikidata_uri.data
        pleiades_uri = form.pleiades_uri.data
        place_label = form.place_label.data
        type = form.type.data
        godot_uri = get_godot_uri_for_eponymous_office(type, place_label, pleiades_uri, wikidata_uri, description)
        return render_template('eponymous_office_add_result.html', title="Add Eponymous Office Result",
                               data_text="Add Eponymous Office Result", description=description, wikidata_uri=wikidata_uri, pleiades_uri=pleiades_uri, place_label=place_label, type=type, godot_uri=str(godot_uri.split("/")[-1]))
    return render_template('eponymous_office_add.html', title="Add Eponymous Office", data_text="Add Eponymous Office", form=form)


@app.route('/eponymous_office/<godot_id>/edit', methods=['GET', 'POST'])
@login_required
def eponyms_detailview_edit(godot_id):
    form = EponymOffice()
    eponym_data = get_eponym_data(godot_id)
    if form.validate_on_submit():
        description = form.description.data
        wikidata_uri = form.wikidata_uri.data
        pleiades_uri = form.pleiades_uri.data
        godot_uri = form.godot_uri.data
        place_label = form.place_label.data
        type = form.type.data
        godot_uri = update_godot_uri_for_eponymous_office(type, place_label, pleiades_uri, wikidata_uri, description)
        return render_template('eponymous_office_add_result.html', title="Edit Eponymous Office Result",
                               data_text="Edit Eponymous Office Result", description=description,
                               wikidata_uri=wikidata_uri, pleiades_uri=pleiades_uri, place_label=place_label, type=type,
                               godot_uri=str(godot_uri.split("/")[-1]))
    else:
        return render_template('detail_eponym_edit.html', title="Edit Eponymous Office",
                           data_text="Edit Eponymous Office", eponym_data=eponym_data, godot_id=godot_id, form=form)


@app.route('/eponymous_office/<godot_id>')
def eponyms_detailview(godot_id):
    # show all information for this eponym
    eponym_data = get_eponym_data(godot_id)
    individuals_list = get_individuals_for_eponym(godot_id)
    pleiades_info = _get_pleiades_info(eponym_data['pleiades_uri'])
    return render_template('detail_eponym.html', title="Eponymous Office Detail View", data_text="Eponymous Office Detail View", eponym_data=eponym_data, individuals_list=individuals_list, pleiades_info=pleiades_info, godot_id=godot_id)


@app.route('/eponymous_office')
def eponyms_list():
    # get all eponymous offices node information
    eponyms_list = get_eponyms()
    return render_template('eponyms_list.html', title="Eponyms", data_text="Eponyms", eponyms_list=eponyms_list)


@app.route('/eponymous_office/<godot_id>/add', methods=['GET', 'POST'])
def eponymous_official_add(godot_id):
    form = EponymOfficial()
    office_data = get_eponym_data(godot_id)
    if form.validate_on_submit():
        name = form.name.data
        office_godot_uri = "https://godot.date/id/"+godot_id
        identifying_uri = form.identifying_uri.data
        identifying_uri_list = []
        has_snap_uri = False
        for uri in identifying_uri.split():
            if "snapdrgn" in uri:
                has_snap_uri = True
        for uri in identifying_uri.split():
            if uri.startswith("http://www.lgpn.ox.ac.uk") and not has_snap_uri:
                # adding SNAP URI if LPGN URI is entered via SNAP SPARQL endpoint
                snap_uri = get_snap_uri_for_lgpn(uri)
                if snap_uri:
                    identifying_uri_list.append(snap_uri)
            identifying_uri_list.append(uri)
        print("identifying_uri_list", identifying_uri_list)
        not_before = form.not_before.data
        not_after = form.not_after.data
        official_godot_uri = get_godot_uri_for_eponymous_official(office_godot_uri, name, identifying_uri_list, not_before, not_after)
        return render_template('eponymous_official_add_result.html', title="Add Eponymous Official Result",
                               data_text="Add Eponymous Official Result", name=name, identifying_uri=identifying_uri_list, not_before=not_before, not_after=not_after, official_godot_uri=str(official_godot_uri.split("/")[-1]), office_godot_uri=str(office_godot_uri.split("/")[-1]), office_data=office_data)
    return render_template('eponymous_official_add.html', title="Add Eponymous Official", data_text="Add Eponymous Official", form=form, godot_uri='https://godot.date/id/'+godot_id, office_data=office_data)


@app.route('/eponymous_office/<office_godot_id>/<official_godot_id>/edit', methods=['GET', 'POST'])
def eponymous_official_edit(office_godot_id, official_godot_id):
    form = EponymOfficial()
    official_data_dict = get_official_data(official_godot_id)

    identifying_uri_str = ""
    # convert list of identifying_uris into string
    for uri in official_data_dict['identifying_uri']:
        identifying_uri_str += uri + " "
    official_data_dict['identifying_uri'] = identifying_uri_str
    office_data = get_office_data_by_official_id(official_godot_id)
    if form.validate_on_submit():
        name = form.name.data
        not_before = ""
        not_after = ""
        office_godot_uri = "https://godot.date/id/"+office_godot_id
        identifying_uri_list = []
        identifying_uri_str = form.identifying_uri.data
        for uri in identifying_uri_str.split():
            identifying_uri_list.append(uri.strip())

        print(identifying_uri_list)

        has_snap_uri = False
        for uri in identifying_uri_list:
            if "snapdrgn" in uri:
                has_snap_uri = True
        identifying_uri_snap_list= []
        for uri in identifying_uri_list:
            if uri.startswith("http://www.lgpn.ox.ac.uk") and not has_snap_uri:
                # adding SNAP URI if LPGN URI is entered via SNAP SPARQL endpoint
                snap_uri = get_snap_uri_for_lgpn(uri)
                if snap_uri:
                    identifying_uri_snap_list.append(snap_uri)
            identifying_uri_snap_list.append(uri)

        print("identifying_uri_snap_list", identifying_uri_snap_list)
        not_before = form.not_before.data
        not_after = form.not_after.data
        official_data = update_eponymous_official_data(official_godot_id, name, identifying_uri_snap_list, not_before, not_after)
        return render_template('eponymous_official_add_result.html', title="Edit Eponymous Official Result",
                               data_text="Edit Eponymous Office Result", name=official_data['value'], identifying_uri=identifying_uri_list, not_before=official_data['not_before'], not_after=official_data['not_after'], official_godot_uri=official_godot_id, office_godot_uri=office_godot_id, office_data=office_data, official_data=official_data_dict)
    return render_template('eponymous_official_edit.html', title="Edit Eponymous Official", data_text="Edit Eponymous Official", form=form, official_godot_uri='https://godot.date/id/'+official_godot_id, official_data=official_data_dict, office_data=office_data)


@app.route('/eponymous_office/<office_godot_id>/<official_godot_id>')
def eponymous_official(office_godot_id, official_godot_id):
    form = EponymOfficial()
    official_data_dict = get_official_data(official_godot_id)
    print(official_data_dict)
    office_data = get_office_data_by_official_id(official_godot_id)
    return render_template('eponymous_official_add_result.html', title="Eponymous Official Detail View",
                           data_text="Eponymous Official Detail View", name=official_data_dict['value'],
                           identifying_uri=official_data_dict['identifying_uri'],
                           not_before=official_data_dict['not_before'], not_after=official_data_dict['not_after'],
                           official_godot_uri=official_godot_id, office_godot_uri=office_godot_id, office_data=office_data)


@app.route('/workshop')
def workshop():
    return render_template('workshop.html', title="Workshop")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


def _get_pleiades_info(pleiades_uri):
    """
    queries pleiades json for names & coordinates of place
    :param pleiades_uri:
    :return: dictionary
    """
    place_information_dict = {}
    print("huhu")
    try:
        r = requests.get(pleiades_uri+'/json', timeout=4)
        names = r.json()['names']
        names_list = []
        for name in names:
            if name['attested']:
                names_list.append(name['attested'])
            else:
                names_list.append(name['romanized'])
        # reverse order lat/lng vs. lng/lat
        coordinates = r.json()['reprPoint'][::-1]
        place_information_dict['names'] = names_list
        place_information_dict['coordinates'] = coordinates
        return place_information_dict
    except:
        return {'error':'Service not available'}
