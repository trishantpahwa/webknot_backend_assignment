import pandas as pd
from os import environ

class ifsc:
    '''
        $$$$= IFSC =$$$$
        description: An instance of ifsc class contains the data of a bank's branch.
        variables: 
         - BANK: (required) str
         - IFSC: (required) str
         - MICR_CODE: (required) str
         - BRANCH: (required) str
         - ADDRESS: (required) str
         - STD_CODE: (required) str
         - CONTACT: (required) str
         - CITY: (required) str
         - DISTRICT: (required) str
         - STATE: (required) str
        functions:
         - get_dict: Returns the object as a dict.
    '''
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
    '''
        description: Loads IFSC Data to primary memory from excel file's first sheet and return it as dict(<str>,<ifsc object>), indexed by their IFSC codes.
        parameters: 
         - [environment_variable] DATASTORE: (required) str
        returns: dict(<str>, <ifsc object>)
    '''
    print('Loading ifsc data...')
    data = pd.read_excel(environ.get('DATASTORE'), sheet_name=0)
    # ['BANK', 'IFSC', 'MICR CODE', 'BRANCH', 'ADDRESS', 'STD CODE', 'CONTACT', 'CITY', 'DISTRICT', 'STATE']
    # | ! | Can also save it as first 4 digits of the ifsc grouped as keys and then remaining, justing indexing the ifsc
    data = data.set_index('IFSC').to_dict('index')
    __data = {}
    for k, v in data.items():
        __data[k] = ifsc(v['BANK'], k, v['MICR CODE'], v['BRANCH'], v['ADDRESS'],
                         v['STD CODE'], v['CONTACT'], v['CITY'], v['DISTRICT'], v['STATE'])
    return __data

def search_ifsc(data, ifsc):
    '''
        description: Searches for data corresponding to an IFSC code, and returns it if found.
        parameters:
         - data: (required) dict(<str>, <ifsc object>)
         - ifsc: (required) str
        returns: dict({
                "ADDRESS": "XXXXXXXXXXXXXXXXXXXX",  # Address of a branch
                "BANK": "XXXXXXXXXXXXXXXXXXXX",  # Name of the bank
                "BRANCH": "XXXXXXXXXXXXXXXXXXXX",  # Name of the bank's branch
                "CITY": "XXXXXXXXXXXXXXXXXXXX",  # City where the bank's branch is located
                "CONTACT": 0000000,  # Contact of the branch
                "DISTRICT": "XXXXXXXXXXXXXXXXXXXX",  # District where the bank's branch is located
                "IFSC": "XXXXXXXXXXXXXXXXXXXX",  # IFSC Code of the branch
                "MICR CODE": 123456789,  # MICR Code of the branch
                "STATE": "XXXXXXXXXXXXXXXXXXXX",  # State where the bank's branch is located
                "STD_CODE": 1  # Code of the state where the bank's branch is located
            })
    '''
    __data = None
    for k, v in data.items():
        if k == ifsc:
            __data = v.get_dict()
            break
    return __data