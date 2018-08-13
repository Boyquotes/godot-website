from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm, RomanConsularDating, CyrenaicaYears
from app.convert import Convert_roman_calendar
from app.neo4j_utilities import get_godot_path, get_attestations


@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')


@app.route('/user/<name>/')
def user_greeting(name):
    return render_template('user.html', title='Welcome', user=name)


@app.route('/browse/')
def browse():
    # browse_data = get_browse_data()
    return render_template('browse.html', title='Browse Data', browse_text='Browse Data')


@app.route('/contact/')
def contact():
    return render_template('contact.html', title='Contact')


@app.route('/about/')
def about():
    return render_template('about.html', title='About GODOT', about_text='About GODOT')


@app.route('/id/<godot_uri>/')
def display_godot_uri(godot_uri):
    # get data/path and attestation links for this GODOT URI
    paths = get_godot_path("https://godot.date/id/" + godot_uri)
    attestations = get_attestations("https://godot.date/id/" + godot_uri)
    return render_template('detail.html', title='Detail view', id=godot_uri, paths=paths, attestations=attestations)


@app.route('/convert/roman_consuls/', methods=['GET', 'POST'])
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
        return render_template('roman_consuls_result.html', title='Roman Consuls', consulship=consul_label, day_ref=form.day_ref.data, day_number=day_number_label, month=form.months.data, result=result_string)
    return render_template('roman_consuls.html', title='Roman Consular Dating', form=form)


@app.route('/cyrenaica/years/', methods=['GET', 'POST'])
def cyrenaica_years():
    form = CyrenaicaYears()
    if form.validate_on_submit():
        return render_template('cyrenaica_years_result.html', title='Cyrenaica Year Dating')
    return render_template('cyrenaica_years.html', title='Cyrenaica Year Dating', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        # return redirect('/index')
        return render_template('user.html', title='Home', user=form.username.data)
    return render_template('login.html', title='Sign In', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
