import pandas as pd
from os import environ

class ifsc:
    BANK = ''
    IFSC = ''
    MICR_CODE = ''
    BRANCH = ''
    ADDRESS = ''
    STD_CODE = ''
    CONTACT = ''
    CITY = ''
    DISTRICT = ''
    STATE = ''

    def __init__(self, bank, ifsc, micr_code, branch, address, std_code, contact, city, district, state):
        self.BANK = bank
        self.IFSC = ifsc
        self.MICR_CODE = micr_code
        self.BRANCH = branch
        self.ADDRESS = address
        self.STD_CODE = std_code
        self.CONTACT = contact
        self.CITY = city
        self.DISTRICT = district
        self.STATE = state

    def get_dict(self):
        return {
            "BANK": self.BANK,
            "IFSC": self.IFSC,
            "MICR CODE": self.MICR_CODE,
            "BRANCH": self.BRANCH,
            "ADDRESS": self.ADDRESS,
            "STD_CODE": self.STD_CODE,
            "CONTACT": self.CONTACT,
            "CITY": self.CITY,
            "DISTRICT": self.DISTRICT,
            "STATE": self.STATE
        }


def load_ifsc_data():
    data = pd.read_excel(environ.get('DATASTORE'), sheet_name=0, verbose=True)
    # ['BANK', 'IFSC', 'MICR CODE', 'BRANCH', 'ADDRESS', 'STD CODE', 'CONTACT', 'CITY', 'DISTRICT', 'STATE']
    # Can also save it as first 4 digits of the ifsc grouped as keys and then remaining, justing indexing the ifsc
    data = data.set_index('IFSC').to_dict('index')
    __data = {}
    for k, v in data.items():
        __data[k] = ifsc(v['BANK'], k, v['MICR CODE'], v['BRANCH'], v['ADDRESS'],
                         v['STD CODE'], v['CONTACT'], v['CITY'], v['DISTRICT'], v['STATE'])
    return __data

def search_ifsc(data, ifsc):
    __data = None
    for k, v in data.items():
        if k == ifsc:
            __data = v.get_dict()
            break
    return __data