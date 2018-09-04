from flask import render_template, flash, redirect
from flask_simplelogin import SimpleLogin, get_username, login_required
from app import app
from app.forms import RomanConsularDating, CyrenaicaYears
from app.convert import Convert_roman_calendar
from app.neo4j_utilities import get_godot_path, get_attestations, get_browse_data, write_cyrenaica_path, \
    get_number_of_nodes, get_number_of_relations, get_number_of_godot_uris, get_list_of_yrs, get_browse_data_number_of_results


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
    if browse_data:
        return render_template('browse.html', title='Browse Data', browse_data=browse_data, list_of_yrs=list_of_yrs, yrs=yrs, page=page, total_hits=total_hits)
    else:
        return render_template('503.html'), 503


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
    print(paths)
    attestations = get_attestations("https://godot.date/id/" + godot_uri)
    if paths:
        return render_template('detail.html', title='Detail view', id=godot_uri, paths=paths, attestations=attestations)
    else:
        return render_template('503.html'), 503


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
        if godot_uri:
            return render_template('cyrenaica_years_result.html', title='Cyrenaica Year Dating', yrs=yrs,
                               apollo_priest=apollo_priest, roman_emperor=roman_emperor, year=year, month=month,
                               day=day, attestation_uri=attestation_uri, date_string=date_string, date_title=date_title, godot_uri=godot_uri.split("/")[-1])
        else:
            return render_template('503.html'), 503
    return render_template('cyrenaica_years.html', title='Cyrenaica Year Dating', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
