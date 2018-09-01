from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, URL, NumberRange, Optional


class CyrenaicaYears(FlaskForm):
    year_reference_system = SelectField('Year Reference System:',
                                        choices=[('None', 'None'),
                                                 ('Unknown', 'Year of Unknown System'),
                                                 ('Era: Actian', 'Actian Era Year'),
                                                 ('Regnal: Roman Emperors', 'Regnal Year (Roman Emperor)'),
                                                 ('Eponymous Officials: Apollo Priest (Cyrenaica)', 'Eponymous Apollo Priest'),
                                                 ])
    year = IntegerField('Year:', validators=[
                        Optional(), NumberRange(min=1, message='minimum value = 1')])
    apollo_priests_cyrenaica = SelectField('Apollo Priest Cyrenaica',
                                           choices=[('', ''),
                                                    ('https://godot.date/id/9piiTw6eaVqycL99bxNzi2',
                                                     'Διονύσιος Σότα (-19/-18)'),
                                                    ('https://godot.date/id/5H5gZigQeHgNXSJRkgde97',
                                                     'Φίλισκος Φιλίσκου φύσει δὲ Εὐφάνευς (-17/-16)'),
                                                    ('https://godot.date/id/EcfEQPopbxSYmSwVVkz4nW',
                                                     'Νεικόστρατος (-16/-15)'),
                                                    ('https://godot.date/id/UyJESVqvsYT96izftTB5Km',
                                                     'Παντα [--] (-15/-14)'),
                                                    ('https://godot.date/id/D2XBxd7ECHVUMF4kmpobrJ',
                                                     'Βαρκαῖος Εὐφάνευς (begin of last quarter of 1. century BC)'),
                                                    ('https://godot.date/id/5iw2q96T36nqyARjioqmPf',
                                                     'Εὐβάτας (begin of last quarter of 1. century BC)'),
                                                    ('https://godot.date/id/j7tvWJqyL5EQaxKZE4sEon',
                                                     'Κλήσιππος (begin of last quarter of 1. century BC)'),
                                                    ('https://godot.date/id/vWpdYxpaCaer4Dd5FgLjf7',
                                                     'Ἀριστοτέλης Σώσιος (end of 1. century BC)'),
                                                    ('https://godot.date/id/Mjs3Vt25ydaTn9HDDUqxkk',
                                                     'Εὐκλῆς Αἰγλάνορος (end of 1. century BC)'),
                                                    ('https://godot.date/id/Ncj9svySm7z5bEkijLxYnD',
                                                     'Παυσανίας Φιλίσκω φύσει δὲ Εὐφάνευς (2/3)'),
                                                    ('https://godot.date/id/FDThVUMuqD3x3FbQZDXqaL',
                                                     'Ἰσοκράτης Κλεάρχω (3/4)'),
                                                    ('https://godot.date/id/6xXHZdr4hynScjR7MMX4g8',
                                                     'Ἀρίσταρχος Θευχρήστω'),
                                                    ('https://godot.date/id/VDcvtP7xTbggnVv3eyVrTR',
                                                     'Θεύχρηστος Διονυσίω (19/20)'),
                                                    ('https://godot.date/id/A8eGUYF8Em3GH9JgH9dxpn',
                                                     'Φάος Κλεάρχω τῶ Φιλοπάτριδος'),
                                                    ('https://godot.date/id/V495FbWa3kJaF7etMPUCA2',
                                                     'Ἴστρος Ἀγαθίνω'),
                                                    ('https://godot.date/id/6oxGqk8MWNj5K3opYM7oSC',
                                                     'Ἀσκληπιάδης Ἐπικράτευς'),
                                                    ('https://godot.date/id/AAhfx8bXbeSjHLim8RhXAR',
                                                     'Εὐφάνης Ἰσοκράτευς'),
                                                    ('https://godot.date/id/p2eLfVsPLEcHqDGRzffgpk',
                                                     'Πανταλέων Πανταλέοντος'),
                                                    ('https://godot.date/id/DW52ZAMtkMXmbh5rNywYBj',
                                                     'Ἰσοκράτης Ἀγχιστράτω'),
                                                    ('https://godot.date/id/2FKhaAcunWjsHikwZCEYo2',
                                                     'Φιλόξενος Φιλίσπω φύσει δὲ Εὐφάνευς'),
                                                    ('https://godot.date/id/GBtCJH47HFmwiusYpUSkjV',
                                                     'Αἰγλανωρ Πτολεμαίω (ca. 35 AD)'),
                                                    ('https://godot.date/id/GPuxpdKj9fSLMKp6L9JZTk',
                                                     'Φάος Καρνήδα'),
                                                    ('https://godot.date/id/bDedq4FJvmkEnV49AAUbeA',
                                                     'Φίλων Εὐφράνορος (38/39)'),
                                                    ('https://godot.date/id/jL4HHZGNZ9Q5cmpVBiw98Q',
                                                     'Φίλιππος Ἀριστάνδρω'),
                                                    ('https://godot.date/id/MacqAjxoqcRdvdgE48YGJG',
                                                     'Κλέαρχος Εὐφάνευς'),
                                                    ('https://godot.date/id/GwggoRLm4rTeKpt5tbfmMa',
                                                     'Ἴστρος Ἴστρω τῶ Ἀγαθίνω'),
                                                    ('https://godot.date/id/Mxb94DmXiQNLw5Wy85MCXg',
                                                     'Πραξιάδας Πραξιἀδα τῶ Φιλίννα'),
                                                    ('https://godot.date/id/coCKma48UMkmyy332PzBSh',
                                                     'Εὐκλείδας Εὐκλείδα τῶ Εὐκλείδα'),
                                                    ('https://godot.date/id/wFHNT2X2jUUuDQPhCECMR4',
                                                     'Σεραπίων Ἀριστάνδρω'),
                                                    ('https://godot.date/id/MQnvAdVry6nUdYnbfnzpBW',
                                                     'Ζηνίων Σώσου'),
                                                    ('https://godot.date/id/7PX8UmF4z8hLotGsqziS7C',
                                                     'Κλέαρχος Καρνήδα'),
                                                    ('https://godot.date/id/BJhvUXaMPjzxnVerm7CGAY',
                                                     'Μᾶρκος Κλέαρχος Φλάμμα Ἰσοκράτευς'),
                                                    ('https://godot.date/id/MnmjWdosX7vPD3ropaNSVY',
                                                     'Λούκιος Καρνήδας Φλάμμα Ἰσοκράτευς'),
                                                    ('https://godot.date/id/YgQZ5BBXMgCbxJA7omyLR7',
                                                     'Ἄσκλαπος Ἰσοκράτους τοῦ Αγχιστράτω'),
                                                    ('https://godot.date/id/jCs9wTEMxmL6gs6gfPPGWb',
                                                     'Ἀγχίστρατος Καρτισθένευς'),
                                                    ('https://godot.date/id/BgjDohjTN4rFKdEHzJ6yz4',
                                                     'Τιβέριος Κλαύδιος Παγκλῆς'),
                                                    ('https://godot.date/id/qacHM2dq7i3P4We2Ur2fWk',
                                                     'Μᾶρκος Αντώνιος Γέμελλος (begin of reign of Nero)'),
                                                    ('https://godot.date/id/Cf6Sw2iKKw8Qk8EDedSnbh',
                                                     'Τιβέριος Κλαύδιος Πρείσκος'),
                                                    ('https://godot.date/id/THs62HPxrkRohRFaQj2SQF',
                                                     'Τιβέριος Κλαύδιος Ἀρίστανδρος'),
                                                    ('https://godot.date/id/TUwefxxrPS2dCYwEj48zRE',
                                                     'Τιβέριος Κλαύδιος Ἴστρος Φιλίσκου (59/60)'),
                                                    ('https://godot.date/id/4f8q4HUKGKpiJVmPALCyYH',
                                                     'Τιβέριος Κλαύδιος Ἄσκλαπος Φιλίσκου (60/61)'),
                                                    ('https://godot.date/id/EqfoHVY9LWXNgf4wvNPvNc',
                                                     'Μᾶρκος Ἀσίνιος Φίλωνος υἱὸς Εὐφράνωρ'),
                                                    ('https://godot.date/id/8XKkazfKaEYN7ixSZAHfFh',
                                                     'Τιβέριος Κλαύδιος Τιβερίω Κλαυδίω ἀρχιερέος υἱὸς Καρνήδας'),
                                                    ('https://godot.date/id/qhnMjLQrVasXsXMZZe6K4n',
                                                     'Μᾶρκος Ἄντωνιος Κεριάλις Πτολεμαίου τοῦ Πτολεμαίου υἱὸς Αἰγλάνωρ'),
                                                    ('https://godot.date/id/iw6iQj6UXpgLBSPHvSULV5',
                                                     'Μητρόδωρος Μητροδώρου τοῦ Μητροδώρου'),
                                                    ('https://godot.date/id/wZhSuXL3oZgBdLqs8tdsu7',
                                                     'Τιβέριος Κλαύδιος Ἄρχιππος (67/68)'),
                                                    ('https://godot.date/id/AfxJ3XRPg5jPn8sZnQBf4C',
                                                     'Μᾶρκος Ἀντώνιου Μᾶρκου Ἀντωνίος Φλάμμα υἱὸς Κασκέλλιος (68/69)'),
                                                    ('https://godot.date/id/wyKickAE6PmfERKfNAjjv6',
                                                     'Σώτας Διονυσίου (begin of reign of Vespasian)'),
                                                    ('https://godot.date/id/NK8g3Hituk5nQTWnxjCnvb',
                                                     'Τιβέριος Κλαύδιος Κλέαρχος'),
                                                    ('https://godot.date/id/DL3YXTKUvd2Gx2mouu63M5',
                                                     'Μᾶρκος Ἀντώνιος Μᾶρκου Ἀντωνίου Φλάμμα υἱὸς Ἀριστομένης (73/74)'),
                                                    ('https://godot.date/id/z54odruR8FiE6qga9LRY66',
                                                     'Τιβέριος Κλαύδιος Τιβερίω Κλαυδίος Ἴστρου υἱὸς Φίλισκος (75/76)'),
                                                    ('https://godot.date/id/YqgFohY2ek8UkzeSbrJCfg',
                                                     'Τειμαγένης Θευδώρου (77/78)'),
                                                    ('https://godot.date/id/f5kqCGVRWTNRfXzuQF8Sr9',
                                                     'Εὐφράνωρ Άντιπάτρω (79/80)'),
                                                    ('https://godot.date/id/ZxHSS5FYxBApeJUQ7dTinV',
                                                     'Φάβιος Φιλίσκου υἱὸς Φίλιππος (89/90)'),
                                                    ('https://godot.date/id/oTaPFTyk3UBg9SXgRWqeqH',
                                                     'Τιβέριος Κλαύδιος Ἴστρος (91/92)'),
                                                    ('https://godot.date/id/nE6KCutFbUYAFphXcbvdNm',
                                                     'Ἄλεξις Καρνήδα (third quarter of 1. century AD)'),
                                                    ('https://godot.date/id/eKaRSMGxewgWRwhc8hXeo7',
                                                     'Καρνήδας Ἀλέξιος (third quarter of 1. century AD)'),
                                                    ('https://godot.date/id/aEcSe4C5wYPxWxXwwsDoBT',
                                                     'Φίλων Φιλοκώμω (third quarter of 1. century AD)'),
                                                    ('https://godot.date/id/QFyAqQeQbbPpErw8bh7FM9',
                                                     'Βαρκαῖος Φίλωνος (third quarter of 1. century AD)'),
                                                    ('https://godot.date/id/AagYWK7E26b9B9yeyJ2mvV',
                                                     'Ἀγχιστ[ρατ-] (1. century AD)'),
                                                    ('https://godot.date/id/wD4kLRqFjQqGGTk9NjvkSK',
                                                     'Ἄσκλαπος (1. century AD)'),
                                                    ('https://godot.date/id/NXo8qnSggrZsVLtDSZuCJJ',
                                                     'Θεο[-] Ἀγαθ[-] (1. century AD)'),
                                                    ('https://godot.date/id/FyPmJRTDsouJHBFRdvETzJ',
                                                     'Τιβέριος Κλαύδιος Πτολεμαῖος (1. century AD)'),
                                                    ('https://godot.date/id/pEtaDKnVaHsPVkNxVSCY4e',
                                                     'Λούκιος (1. century AD)'),
                                                    ('https://godot.date/id/JgwzYhBsPhjvzmBbAVwoET',
                                                     'Ξοῦθος (1. century AD)'),
                                                    ('https://godot.date/id/V3uW3NwrR4dMQWp5P5GLkj',
                                                     '[--]ευς Πτολεμαῖου υἱὸς Πτολεμαῖος (1. century AD)'),
                                                    ('https://godot.date/id/poqawGNwxo5sikRQ2YobEA',
                                                     'Φιλων Ἀγαθίνω (1. century AD)'),
                                                    ('https://godot.date/id/LDS2a3tBqYm2BTkGjrDAoB',
                                                     'Φλάμμας (1. century AD)'),
                                                    ('https://godot.date/id/BxPwRqcdGcMK2kYpMhNpLA',
                                                     '[--]ευς Πα[--] (1. century AD)'),
                                                    ('https://godot.date/id/WuAZpfxBwzbDmzjiN3yfPT',
                                                     '[--] Πτυλμαίου υἱὸ[ς --]ας (1. century AD)'),
                                                    ('https://godot.date/id/LUvP7xTzrYaXcoWYGCi3eK',
                                                     'Τιβέριος Κλαύδιος Ἐπικράτευς υἱὸς Ἀσκλαπιάδας (late 1. century AD)'),
                                                    ('https://godot.date/id/aopoeWW8J62W9JYD6yzHQn',
                                                     'Μᾶρκος Ἀντώνιος Κασκέλλιος (late 1. century AD)'),
                                                    ('https://godot.date/id/8PYaSTrNDexnZWctHAoDWg',
                                                     'Τίτος Φλάβιος Σαβεῖνος υἱὸς Παυσανίου Παθσανίας (late 1. century AD)'),
                                                    ('https://godot.date/id/57bLC6TpDLijhrZmyAbjKP',
                                                     'Τιβέριος Κλαυδίου Φειδίμου υἱὸς Ἴστρος (100/101)'),
                                                    ('https://godot.date/id/PhnMW5eA8AK6fYfvYkbmmf',
                                                     'Κοίντος Φάβιος Καρνεάδης (101/102)'),
                                                    ('https://godot.date/id/6SozK7YH7umQcDUZ42FYEM',
                                                     'Τιβέριος Κλαύδιος Ἄτταλος Τιβερίου Κλαυδίου Κλεάρχου υἱὸς (102/103)'),
                                                    ('https://godot.date/id/aZS3jh2ZAqzRk9AcrH7vuD',
                                                     'Τίτος Φλάβιος Εὐκλείδας (103/104)'),
                                                    ('https://godot.date/id/pLzPBXsLwAcvs4TEP87Hbi',
                                                     'Τιβέριος Κλαύδιος Φιλόξενος Ἀντωνιανός (104/105)'),
                                                    ('https://godot.date/id/yDH2L39UZZ3TJRTpB6QbXn',
                                                     'Γάιος Ποστόμιος Ὀπτάτος (106/107)'),
                                                    ('https://godot.date/id/CSzGrj2kRFa5m4WjnuJjNE',
                                                     'Τιβέριος Κλαύδιος Καρτισθένης Εὐφράνωρ (108/109)'),
                                                    ('https://godot.date/id/4kVppVAwjaniXrAC9jUWfM',
                                                     'Πόπλιος Σήστιος Πολλίων (111/112)'),
                                                    ('https://godot.date/id/bpFffnnMUVLcaSCBJFWuWR',
                                                     '[--] Κλαύδιος [--] (begin of 2. century AD)'),
                                                    ('https://godot.date/id/t9JwTfuaKUAbsj8xtRr5PK',
                                                     'Τιβέριος Κλαύδιος Ἀρίστομένης Μᾶγνος ὁ καὶ Περικλῆς (begin of 2. century AD)'),
                                                    ('https://godot.date/id/Gtn3iaQcPvfMaTLgShw46e',
                                                     'Ῥουτὶλιος (begin of 2. century AD)'),
                                                    ])
    roman_emperors = SelectField('Roman Emperor:',
                                           choices=[('', ''),
                                                    ('Augustus', 'Augustus'),
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
                                                    ('Diocletian', 'Diocletian'),
                                                    ])
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
                                                 ('epagomenal days','epagomenal days'),
                                                 ])
    day = IntegerField('Day:', validators=[
        Optional(), NumberRange(min=1, max=30, message='value between 1 and 30')])
    attestation_uri = StringField('Attestation URI:', validators=[DataRequired(), URL()])
    date_string = StringField('Date String:', validators=[DataRequired()])
    title = StringField('Title:', validators=[DataRequired()])
    reset = SubmitField('Reset...')
    submit = SubmitField('Submit...')


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
