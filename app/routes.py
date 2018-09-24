from flask import render_template, request, jsonify, redirect
from flask_simplelogin import login_required
from app import app
from app.forms import RomanConsularDating, CyrenaicaYears, AttestationUpdate, AttestationDelete, CyrenaicaRomanImperialTitulature
from app.convert import Convert_roman_calendar
from app.neo4j_utilities import get_godot_path, get_attestations, get_browse_data, write_cyrenaica_path, \
    get_number_of_nodes, get_number_of_relations, get_number_of_godot_uris, get_list_of_yrs, get_browse_data_number_of_results, get_attestation, update_attestation, delete_attestation, write_cyrenaica_emperor_titulature_path
import simplejson as json
from app.openrefine_utils import search, get_openrefine_metadata


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/browse', defaults={'yrs': 'All', 'page': 1})
@app.route('/browse/<yrs>', defaults={'page': 1})
@app.route('/browse/<yrs>/<page>')
def browse(yrs, page):
    browse_data = get_browse_data(yrs, page)
    list_of_yrs = get_list_of_yrs()
    total_hits = get_browse_data_number_of_results(yrs)
    return render_template('browse.html', title='Browse Data', browse_data=browse_data, list_of_yrs=list_of_yrs,
                           yrs=yrs, page=page, total_hits=total_hits)


@app.route('/contact')
def contact():
    number_of_nodes = get_number_of_nodes()
    number_of_relations = get_number_of_relations()
    number_of_godot_uris = get_number_of_godot_uris()
    return render_template('contact.html', title='Contact', number_of_nodes=number_of_nodes,
                           number_of_relations=number_of_relations, number_of_godot_uris=number_of_godot_uris)


@app.route('/about')
def about():
    return render_template('about.html', title='About GODOT', about_text='About GODOT')


@app.route('/id/<godot_uri>')
def display_godot_uri(godot_uri):
    # get data/path and attestation links for this GODOT URI
    paths = get_godot_path("https://godot.date/id/" + godot_uri)
    attestations = get_attestations("https://godot.date/id/" + godot_uri)
    if paths:
        return render_template('detail.html', title='Detail view', id=godot_uri, paths=paths, attestations=attestations)
    else:
        return render_template('404.html'), 404


@app.route('/id/<godot_uri>/<node_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_attestation_data(godot_uri, node_id):
    form = AttestationUpdate()
    if form.validate_on_submit():
        attestation_uri = form.attestation_uri.data
        title = form.title.data
        date_string = form.date_string.data
        if update_attestation(node_id, attestation_uri, title, date_string):
            return redirect("/id/" + godot_uri)
    paths = get_godot_path("https://godot.date/id/" + godot_uri)
    attestation = get_attestation(node_id)
    if paths:
        return render_template('update_attestation_data.html', title='Edit Attestation Data', id=godot_uri, paths=paths, attestations=attestation, form=form)
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
        consul_label, godot_uri = form.consulship.data.split('|')
        day_number_label = Convert_roman_calendar.get_day_number_label(form.day_number.data)
        # return conversion result to template
        return render_template('roman_consuls_result.html', title='Roman Consuls', consulship=consul_label,
                               day_ref=form.day_ref.data, day_number=day_number_label, month=form.months.data,
                               result=result_string)
    return render_template('roman_consuls.html', title='Roman Consular Dating', form=form)


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
        attestation_uri = form.attestation_uri.data
        date_string = form.date_string.data
        date_title = form.title.data



        godot_uri = write_cyrenaica_emperor_titulature_path(roman_emperor, consul_number, consul_designatus, trib_pot_number, imperator_number, victory_titles, attestation_uri,
                                         date_string, date_title)
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
                               godot_uri=godot_uri,
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
        attestation_uri = form.attestation_uri.data
        date_string = form.date_string.data
        date_title = form.title.data
        godot_uri = write_cyrenaica_path(yrs, apollo_priest, roman_emperor, year, month, day, attestation_uri,
                                         date_string, date_title)
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
                               day=day, attestation_uri=attestation_uri, date_string=date_string, date_title=date_title, godot_uri=godot_uri.split("/")[-1])
    return render_template('cyrenaica_years.html', title='Cyrenaica Year Dating', form=form)


@app.route('/tools/openrefine')
def tools_openrefine():
    return render_template('tools_openrefine.html')


@app.route('/tools/api')
def tools_api():
    return render_template('tools_api.html')


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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
