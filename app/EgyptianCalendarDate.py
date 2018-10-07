import requests
import json


class EgyptianCalendarDate:

    def __init__(self, period, reign, year, month, day):
        self.period = period
        self.reign = reign
        self.year = year
        self.month = month
        self.day = day

    def convert_to_julian(self):
        url = "http://online-resourcen.de/api/%s/%s/%s/%s/%s" % (self.period, self.reign, self.year, self.month, self.day)
        response = requests.get(url).json()
        if response['status'] == 'success':
            return response['data']
