

class Convert_roman_calendar():

    day_number_label = {
        1: '',
        2: 'a.d. II (pridie)',
        3: 'a.d. III',
        4: 'a.d. IV',
        5: 'a.d. V',
        6: 'a.d. VI',
        7: 'a.d. VII',
        8: 'a.d. VIII',
        9: 'a.d. IX',
        10: 'a.d. X',
        11: 'a.d. XI',
        12: 'a.d. XII',
        13: 'a.d. XIII',
        14: 'a.d. XIV',
        15: 'a.d. XV',
        16: 'a.d. XVI',
        17: 'a.d. XVII',
        18: 'a.d. XVIII',
        19: 'a.d. XIX'
    }

    def get_day_number_label(id):
        """ returns label for day parameters as in query form
            ex.: 2 = a.d. II (pridie)
        """
        print(type(id))
        return Convert_roman_calendar.day_number_label.get(int(id), '')

    def get_date_from_index_number(i):
        """ return date string for index_number
            e.g.: "July 28"
        """
        if i < 1:
            i = i + 365
        if i >= 1 and i < 32:
            return str(i).zfill(2) + " January "
        elif i >= 32 and i < 61:
            return str(i-31).zfill(2) + " February "
        elif i >= 61 and i < 91:
            return str(i-60).zfill(2) + " March "
        elif i >= 91 and i < 121:
            return str(i-90).zfill(2) + " April "
        elif i >= 121 and i < 152:
            return str(i-120).zfill(2) + " May "
        elif i >= 152 and i < 182:
            return str(i-151).zfill(2) + " June "
        elif i >= 182 and i < 213:
            return str(i-181).zfill(2) + " July "
        elif i >= 213 and i < 244:
            return str(i-212).zfill(2) + " August "
        elif i >= 244 and i < 274:
            return str(i-243).zfill(2) + " September "
        elif i >= 274 and i < 305:
            return str(i-273).zfill(2) + " October "
        elif i >= 305 and i < 335:
            return str(i-304).zfill(2) + " November "
        elif i >= 335 and i <= 365:
            return str(i-334).zfill(2) + " December "

    def consulship(day, ref, month, year):
        day_index_number = 0
        first_day_index_number = {
            'January': 1,
            'February': 32,
            'March': 61,
            'April': 91,
            'May': 121,
            'June': 152,
            'July': 182,
            'August': 213,
            'September': 244,
            'October': 274,
            'November': 305,
            'December': 335
        }

        idus_day_index_number = {
            'January': first_day_index_number['January'] + 13,
            'February': first_day_index_number['February'] + 13,
            'March': first_day_index_number['March'] + 15,
            'April': first_day_index_number['April'] + 13,
            'May': first_day_index_number['May'] + 15,
            'June': first_day_index_number['June'] + 13,
            'July': first_day_index_number['July'] + 15,
            'August': first_day_index_number['August'] + 13,
            'September': first_day_index_number['September'] + 13,
            'October': first_day_index_number['October'] + 15,
            'November': first_day_index_number['November'] + 13,
            'December': first_day_index_number['December'] + 13
        }

        nonae_day_index_number = {
            'January': first_day_index_number['January'] + 5,
            'February': first_day_index_number['February'] + 5,
            'March': first_day_index_number['March'] + 7,
            'April': first_day_index_number['April'] + 5,
            'May': first_day_index_number['May'] + 7,
            'June': first_day_index_number['June'] + 5,
            'July': first_day_index_number['July'] + 7,
            'August': first_day_index_number['August'] + 5,
            'September': first_day_index_number['September'] + 5,
            'October': first_day_index_number['October'] + 7,
            'November': first_day_index_number['November'] + 5,
            'December': first_day_index_number['December'] + 5
        }

        if ref == "Kalends":
            day_index_number = first_day_index_number[month] - int(day) + 1
        elif ref == "Ides":
            day_index_number = idus_day_index_number[month] - int(day)
        elif ref == "Nones":
            day_index_number = nonae_day_index_number[month] - int(day)

        return Convert_roman_calendar.get_date_from_index_number(day_index_number) + ' ' + year
