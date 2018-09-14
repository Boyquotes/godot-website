from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Optional, Regexp

roman_emperors_list = [('unknown', 'unknown'), ('Augustus', 'Augustus'),
                                          ('Tiberius', 'Tiberius'),
                                          ('Caligula', 'Caligula'),
                                          ('Claudius', 'Claudius'),
                                          ('Nero', 'Nero'),
                                          ('Galba', 'Galba'),
                                          ('Otho', 'Otho'),
                                          ('Vitellius', 'Vitellius'),
                                          ('Vespasian', 'Vespasian'),
                                          ('Titus', 'Titus'),
                                          ('Domitian', 'Domitian'),
                                          ('Nerva', 'Nerva'),
                                          ('Trajan', 'Trajan'),
                                          ('Hadrian', 'Hadrian'),
                                          ('Antoninus Pius', 'Antoninus Pius'),
                                          ('Marc Aurel', 'Marc Aurel'),
                                          ('Commodus', 'Commodus'),
                                          ('Pertinax', 'Pertinax'),
                                          ('Pescennius Niger', 'Pescennius Niger'),
                                          ('Septimius Severus', 'Septimius Severus'),
                                          ('Caracalla', 'Caracalla'),
                                          ('Macrinus', 'Macrinus'),
                                          ('Elagabal', 'Elagabal'),
                                          ('Severus Alexander', 'Severus Alexander'),
                                          ('Maximinus Thrax', 'Maximinus Thrax'),
                                          ('Gordian', 'Gordian'),
                                          ('Phillippus Arabs', 'Phillippus Arabs'),
                                          ('Decius', 'Decius'),
                                          ('Gallus / Volusian', 'Gallus / Volusian'),
                                          ('Aemilian', 'Aemilian'),
                                          ('Valerian', 'Valerian'),
                                          ('Macrianus / Quietus', 'Macrianus / Quietus'),
                                          ('Gallienus', 'Gallienus'),
                                          ('Claudius Gothicus', 'Claudius Gothicus'),
                                          ('Aurelian', 'Aurelian'),
                                          ('Tacitus', 'Tacitus'),
                                          ('Probus', 'Probus'),
                                          ('Carus / Carinus', 'Carus / Carinus'),
                                          ('Diocletian', 'Diocletian')]


class CyrenaicaYears(FlaskForm):
    year_reference_system = SelectField('Year Reference System:',
                                        choices=[('None', 'None'),
                                                 ('Unknown', 'Year of Unknown System'),
                                                 ('Era: Actian', 'Actian Era Year'),
                                                 ('Eponymous Officials: Apollo Priest (Cyrenaica)', 'Eponymous Apollo Priest'),
                                                 ('Regnal: Roman Emperors', 'Regnal Year (Roman Emperor)'),
                                                 ])
    year = StringField('Year:', validators=[
                        Optional(), Regexp('^[0-9_]*$')])
    apollo_priests_cyrenaica = SelectField('Apollo Priest Cyrenaica',
                                           choices=[('[--] Κλαύδιος [--]','[--] Κλαύδιος [--]'),
                                                ('[--] Πτυλμαίου υἱὸ[ς --]ας','[--] Πτυλμαίου υἱὸ[ς --]ας'),
                                                ('[--]ευς Πα[--]','[--]ευς Πα[--]'),
                                                ('[--]ευς Πτολεμαῖου υἱὸς Πτολεμαῖος','[--]ευς Πτολεμαῖου υἱὸς Πτολεμαῖος'),
                                                ('Ἀγχιστ[ρατ-]','Ἀγχιστ[ρατ-]'),
                                                ('Ἀγχίστρατος Καρτισθένευς','Ἀγχίστρατος Καρτισθένευς'),
                                                ('Αἰγλανωρ Πτολεμαίω','Αἰγλανωρ Πτολεμαίω'),
                                                ('Ἄλεξις Καρνήδα','Ἄλεξις Καρνήδα'),
                                                ('Ἀρίσταρχος Θευχρήστω','Ἀρίσταρχος Θευχρήστω'),
                                                ('Ἀριστοτέλης Σώσιος','Ἀριστοτέλης Σώσιος'),
                                                ('Ἄσκλαπος','Ἄσκλαπος'),
                                                ('Ἄσκλαπος Ἰσοκράτους τοῦ Αγχιστράτω','Ἄσκλαπος Ἰσοκράτους τοῦ Αγχιστράτω'),
                                                ('Ἀσκληπιάδης Ἐπικράτευς','Ἀσκληπιάδης Ἐπικράτευς'),
                                                ('Βαρκαῖος Εὐφάνευς','Βαρκαῖος Εὐφάνευς'),
                                                ('Βαρκαῖος Φίλωνος','Βαρκαῖος Φίλωνος'),
                                                ('Γάιος Ποστόμιος Ὀπτάτος','Γάιος Ποστόμιος Ὀπτάτος'),
                                                ('Διονύσιος Σότα','Διονύσιος Σότα'),
                                                ('Εὐβάτας','Εὐβάτας'),
                                                ('Εὐκλείδας Εὐκλείδα τῶ Εὐκλείδα','Εὐκλείδας Εὐκλείδα τῶ Εὐκλείδα'),
                                                ('Εὐκλῆς Αἰγλάνορος','Εὐκλῆς Αἰγλάνορος'),
                                                ('Εὐφάνης Ἰσοκράτευς','Εὐφάνης Ἰσοκράτευς'),
                                                ('Εὐφράνωρ Άντιπάτρω','Εὐφράνωρ Άντιπάτρω'),
                                                ('Ζηνίων Σώσου','Ζηνίων Σώσου'),
                                                ('Θεο[-] Ἀγαθ[-]','Θεο[-] Ἀγαθ[-]'),
                                                ('Θεύχρηστος Διονυσίω','Θεύχρηστος Διονυσίω'),
                                                ('Ἰσοκράτης Ἀγχιστράτω','Ἰσοκράτης Ἀγχιστράτω'),
                                                ('Ἰσοκράτης Κλεάρχω','Ἰσοκράτης Κλεάρχω'),
                                                ('Ἴστρος Ἀγαθίνω','Ἴστρος Ἀγαθίνω'),
                                                ('Ἴστρος Ἴστρω τῶ Ἀγαθίνω','Ἴστρος Ἴστρω τῶ Ἀγαθίνω'),
                                                ('Καρνήδας Ἀλέξιος','Καρνήδας Ἀλέξιος'),
                                                ('Κλέαρχος Εὐφάνευς','Κλέαρχος Εὐφάνευς'),
                                                ('Κλέαρχος Καρνήδα','Κλέαρχος Καρνήδα'),
                                                ('Κλήσιππος','Κλήσιππος'),
                                                ('Κοίντος Φάβιος Καρνεάδης','Κοίντος Φάβιος Καρνεάδης'),
                                                ('Λούκιος','Λούκιος'),
                                                ('Λούκιος Καρνήδας Φλάμμα Ἰσοκράτευς','Λούκιος Καρνήδας Φλάμμα Ἰσοκράτευς'),
                                                ('Μᾶρκος Αντώνιος Γέμελλος','Μᾶρκος Αντώνιος Γέμελλος'),
                                                ('Μᾶρκος Ἀντώνιος Κασκέλλιος','Μᾶρκος Ἀντώνιος Κασκέλλιος'),
                                                ('Μᾶρκος Ἄντωνιος Κεριάλις Πτολεμαίου τοῦ Πτολεμαίου υἱὸς Αἰγλάνωρ','Μᾶρκος Ἄντωνιος Κεριάλις Πτολεμαίου τοῦ Πτολεμαίου υἱὸς Αἰγλάνωρ'),
                                                ('Μᾶρκος Ἀντώνιος Μᾶρκου Ἀντωνίου Φλάμμα υἱὸς Ἀριστομένης','Μᾶρκος Ἀντώνιος Μᾶρκου Ἀντωνίου Φλάμμα υἱὸς Ἀριστομένης'),
                                                ('Μᾶρκος Ἀντώνιου Μᾶρκου Ἀντωνίος Φλάμμα υἱὸς Κασκέλλιος','Μᾶρκος Ἀντώνιου Μᾶρκου Ἀντωνίος Φλάμμα υἱὸς Κασκέλλιος'),
                                                ('Μᾶρκος Ἀσίνιος Φίλωνος υἱὸς Εὐφράνωρ','Μᾶρκος Ἀσίνιος Φίλωνος υἱὸς Εὐφράνωρ'),
                                                ('Μᾶρκος Κλέαρχος Φλάμμα Ἰσοκράτευς','Μᾶρκος Κλέαρχος Φλάμμα Ἰσοκράτευς'),
                                                ('Μητρόδωρος Μητροδώρου τοῦ Μητροδώρου','Μητρόδωρος Μητροδώρου τοῦ Μητροδώρου'),
                                                ('Νεικόστρατος','Νεικόστρατος'),
                                                ('Ξοῦθος','Ξοῦθος'),
                                                ('Παντα [--]','Παντα [--]'),
                                                ('Πανταλέων Πανταλέοντος','Πανταλέων Πανταλέοντος'),
                                                ('Παυσανίας Φιλίσκω φύσει δὲ Εὐφάνευς','Παυσανίας Φιλίσκω φύσει δὲ Εὐφάνευς'),
                                                ('Πόπλιος Σήστιος Πολλίων','Πόπλιος Σήστιος Πολλίων'),
                                                ('Πραξιάδας Πραξιἀδα τῶ Φιλίννα','Πραξιάδας Πραξιἀδα τῶ Φιλίννα'),
                                                ('Ῥουτὶλιος','Ῥουτὶλιος'),
                                                ('Σεραπίων Ἀριστάνδρω','Σεραπίων Ἀριστάνδρω'),
                                                ('Σώτας Διονυσίου','Σώτας Διονυσίου'),
                                                ('Τειμαγένης Θευδώρου','Τειμαγένης Θευδώρου'),
                                                ('Τιβέριος Κλαύδιος Ἀρίστανδρος','Τιβέριος Κλαύδιος Ἀρίστανδρος'),
                                                ('Τιβέριος Κλαύδιος Ἀρίστομένης Μᾶγνος ὁ καὶ Περικλῆς','Τιβέριος Κλαύδιος Ἀρίστομένης Μᾶγνος ὁ καὶ Περικλῆς'),
                                                ('Τιβέριος Κλαύδιος Ἄρχιππος','Τιβέριος Κλαύδιος Ἄρχιππος'),
                                                ('Τιβέριος Κλαύδιος Ἄσκλαπος Φιλίσκου','Τιβέριος Κλαύδιος Ἄσκλαπος Φιλίσκου'),
                                                ('Τιβέριος Κλαύδιος Ἄτταλος Τιβερίου Κλαυδίου Κλεάρχου υἱὸς','Τιβέριος Κλαύδιος Ἄτταλος Τιβερίου Κλαυδίου Κλεάρχου υἱὸς'),
                                                ('Τιβέριος Κλαύδιος Ἐπικράτευς υἱὸς Ἀσκλαπιάδας','Τιβέριος Κλαύδιος Ἐπικράτευς υἱὸς Ἀσκλαπιάδας'),
                                                ('Τιβέριος Κλαύδιος Ἴστρος','Τιβέριος Κλαύδιος Ἴστρος'),
                                                ('Τιβέριος Κλαύδιος Ἴστρος Φιλίσκου','Τιβέριος Κλαύδιος Ἴστρος Φιλίσκου'),
                                                ('Τιβέριος Κλαύδιος Καρτισθένης Εὐφράνωρ','Τιβέριος Κλαύδιος Καρτισθένης Εὐφράνωρ'),
                                                ('Τιβέριος Κλαύδιος Κλέαρχος','Τιβέριος Κλαύδιος Κλέαρχος'),
                                                ('Τιβέριος Κλαύδιος Παγκλῆς','Τιβέριος Κλαύδιος Παγκλῆς'),
                                                ('Τιβέριος Κλαύδιος Πρείσκος','Τιβέριος Κλαύδιος Πρείσκος'),
                                                ('Τιβέριος Κλαύδιος Πτολεμαῖος','Τιβέριος Κλαύδιος Πτολεμαῖος'),
                                                ('Τιβέριος Κλαύδιος Τιβερίω Κλαυδίος Ἴστρου υἱὸς Φίλισκος','Τιβέριος Κλαύδιος Τιβερίω Κλαυδίος Ἴστρου υἱὸς Φίλισκος'),
                                                ('Τιβέριος Κλαύδιος Τιβερίω Κλαυδίω ἀρχιερέος υἱὸς Καρνήδας','Τιβέριος Κλαύδιος Τιβερίω Κλαυδίω ἀρχιερέος υἱὸς Καρνήδας'),
                                                ('Τιβέριος Κλαύδιος Φιλόξενος Ἀντωνιανός','Τιβέριος Κλαύδιος Φιλόξενος Ἀντωνιανός'),
                                                ('Τιβέριος Κλαυδίου Φειδίμου υἱὸς Ἴστρος','Τιβέριος Κλαυδίου Φειδίμου υἱὸς Ἴστρος'),
                                                ('Τίτος Φλάβιος Εὐκλείδας','Τίτος Φλάβιος Εὐκλείδας'),
                                                ('Τίτος Φλάβιος Σαβεῖνος υἱὸς Παυσανίου Παθσανίας','Τίτος Φλάβιος Σαβεῖνος υἱὸς Παυσανίου Παθσανίας'),
                                                ('Φάβιος Φιλίσκου υἱὸς Φίλιππος','Φάβιος Φιλίσκου υἱὸς Φίλιππος'),
                                                ('Φάος Καρνήδα','Φάος Καρνήδα'),
                                                ('Φάος Κλεάρχω τῶ Φιλοπάτριδος','Φάος Κλεάρχω τῶ Φιλοπάτριδος'),
                                                ('Φίλιππος Ἀριστάνδρω','Φίλιππος Ἀριστάνδρω'),
                                                ('Φίλισκος Φιλίσκου φύσει δὲ Εὐφάνευς','Φίλισκος Φιλίσκου φύσει δὲ Εὐφάνευς'),
                                                ('Φιλόξενος Φιλίσπω φύσει δὲ Εὐφάνευς','Φιλόξενος Φιλίσπω φύσει δὲ Εὐφάνευς'),
                                                ('Φιλων Ἀγαθίνω','Φιλων Ἀγαθίνω'),
                                                ('Φίλων Εὐφράνορος','Φίλων Εὐφράνορος'),
                                                ('Φίλων Φιλοκώμω','Φίλων Φιλοκώμω'),
                                                ('Φλάμμας','Φλάμμας'),
                                                    ])
    roman_emperors = SelectField('Roman Emperor:',
                                           choices=roman_emperors_list)
    egyptian_calendar_months = SelectField('Months (Egyptian):',
                                        choices=[('None', 'None'),
                                                 ('Thot', 'Thot'),
                                                 ('Phaophi', 'Phaophi'),
                                                 ('Hathyr', 'Hathyr'),
                                                 ('Choiak', 'Choiak'),
                                                 ('Tybi', 'Tybi'),
                                                 ('Mecheir', 'Mecheir'),
                                                 ('Phamenoth', 'Phamenoth'),
                                                 ('Pharmuthi', 'Pharmuthi'),
                                                 ('Pachons', 'Pachons'),
                                                 ('Payni', 'Payni'),
                                                 ('Epeiph', 'Epeiph'),
                                                 ('Mesore', 'Mesore'),
                                                 ('Epagomenal Days', 'Epagomenal Days'),
                                                 ])
    day = StringField('Day:', validators=[
        Optional(), Regexp('^[0-9_]*$')])
    attestation_uri = StringField('Attestation URI:', validators=[DataRequired()])
    date_string = StringField('Date String:', validators=[DataRequired()])
    title = StringField('Title:', validators=[DataRequired()])
    reset = SubmitField('Reset...')
    submit = SubmitField('Submit...')


class AttestationUpdate(FlaskForm):
    attestation_uri = StringField('Attestation URI:', validators=[DataRequired()])
    date_string = StringField('Date String:', validators=[DataRequired()])
    title = StringField('Title:', validators=[DataRequired()])
    reset = SubmitField('Reset...')
    submit = SubmitField('Submit...')


class AttestationDelete(FlaskForm):
    submit = SubmitField('Delete...')


class RomanConsularDating(FlaskForm):
    consulship = StringField('Consulship:', validators=[DataRequired()])
    day_ref = SelectField('Kalends/Nones/Ides:',
                          choices=[('Kalends', 'Kalends'),
                                   ('Nones', 'Nones'),
                                   ('Ides', 'Ides'),
                                   ])
    months = SelectField('Month:',
                         choices=[('January', 'January'),
                                  ('February', 'February'),
                                  ('March', 'March'),
                                  ('April', 'April'),
                                  ('May', 'May'),
                                  ('June', 'June'),
                                  ('July', 'July'),
                                  ('August', 'August'),
                                  ('September', 'September'),
                                  ('October', 'October'),
                                  ('November', 'November'),
                                  ('December', 'December'),
                                  ])
    day_number = SelectField('Day:',
                             choices=[
                                 (1, ''),
                                 (2, 'a.d. II (pridie)'),
                                 (3, 'a.d. III'),
                                 (4, 'a.d. IV'),
                                 (5, 'a.d. V'),
                                 (6, 'a.d. VI'),
                                 (7, 'a.d. VII'),
                                 (8, 'a.d. VIII'),
                                 (9, 'a.d. IX'),
                                 (10, 'a.d. X'),
                                 (11, 'a.d. XI'),
                                 (12, 'a.d. XII'),
                                 (13, 'a.d. XIII'),
                                 (14, 'a.d. XIV'),
                                 (15, 'a.d. XV'),
                                 (16, 'a.d. XVI'),
                                 (17, 'a.d. XVII'),
                                 (18, 'a.d. XVIII'),
                                 (19, 'a.d. XIX'),
                             ])
    reset = SubmitField('Reset...')
    submit = SubmitField('Convert...')


class CyrenaicaRomanImperialTitulature(FlaskForm):
    reset = SubmitField('Reset...')
    submit = SubmitField('Submit...')
    attestation_uri = StringField('Attestation URI:', validators=[DataRequired()])
    date_string = StringField('Date String:', validators=[DataRequired()])
    title = StringField('Title:', validators=[DataRequired()])
    roman_emperors = SelectField('Roman Emperor:',
                                 choices=roman_emperors_list)
    egyptian_calendar_months = SelectField('Months (Egyptian):',
                                           choices=[('None', 'None'),
                                                    ('Thot', 'Thot'),
                                                    ('Phaophi', 'Phaophi'),
                                                    ('Hathyr', 'Hathyr'),
                                                    ('Choiak', 'Choiak'),
                                                    ('Tybi', 'Tybi'),
                                                    ('Mecheir', 'Mecheir'),
                                                    ('Phamenoth', 'Phamenoth'),
                                                    ('Pharmuthi', 'Pharmuthi'),
                                                    ('Pachons', 'Pachons'),
                                                    ('Payni', 'Payni'),
                                                    ('Epeiph', 'Epeiph'),
                                                    ('Mesore', 'Mesore'),
                                                    ('Epagomenal Days', 'Epagomenal Days'),
                                                    ])
    day = StringField('Day:', validators=[
        Optional(), Regexp('^[0-9_]*$')])
    consul_number = StringField('Consul Number:', validators=[
        Optional(), Regexp('^[0-9_]*$')])
    trib_pot_number = StringField('Trib Pot Number:', validators=[
        Optional(), Regexp('^[0-9_]*$')])
    imperator_number = StringField('Imperator Number:', validators=[
        Optional(), Regexp('^[0-9_]*$')])
    victory_titles = SelectMultipleField('Victory Titles:',
                                           choices=[
                                                    ('Adiabenicus', 'Adiabenicus'),
                                                    ('Arabicus', 'Arabicus'),
                                                    ('Armeniacus', 'Armeniacus'),
                                                    ('Britannicus', 'Britannicus'),
                                                    ('Britannicus max.', 'Britannicus max.'),
                                                    ('Carpicus max.', 'Carpicus max.'),
                                                    ('Dacicus', 'Dacicus'),
                                                    ('Dacicus max.', 'Dacicus max.'),
                                                    ('Germanicus', 'Germanicus'),
                                                    ('Germanicus max.', 'Germanicus max.'),
                                                    ('Gothicus', 'Gothicus'),
                                                    ('Gothicus max.', 'Gothicus max.'),
                                                    ('Medicus', 'Medicus'),
                                                    ('Palmyrenicus max.', 'Palmyrenicus max.'),
                                                    ('Parthicus', 'Parthicus'),
                                                    ('Parthicus max.', 'Parthicus max.'),
                                                    ('Persicus max.', 'Persicus max.'),
                                                    ('Samarticus', 'Samarticus'),
                                                    ('Samarticus max.', 'Samarticus max.'),
                                                    ])









