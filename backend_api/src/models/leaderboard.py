import pandas as pd
from os import environ
import collections


class leaderboard:
    '''
       ^^^^ Leaderboard ^^^^ 
       description: leaderboard class to bind data_structures and functions together.
       variables:
        - __data: dict({<str>,<int>})
       functions:
        - load_bank_leaderboard_data: Loads the leaderboard data from the excel file sheet 2.
        - get_leaderboard: Returns data from the leaderboard w.r.t order and limits defined.
        - get_total: Returns the total number of branches of all banks in India. [First record]
    '''
    __data = {}

    def load_bank_leaderboard_data(self):
        '''
            description: Loads the leaderboard data from the excel file sheet 2.
            parameters:
             - [environment_variable] DATASTORE: (required) str
            returns: None
        '''
        print('Loading leaderboard data...')
        data = pd.read_excel(environ.get('DATASTORE'), sheet_name=1)
        self.__data = data.set_index('BANK').to_dict('index')

    def get_leaderboard(self, order='DESC', limit=10):
        '''
            description: Returns data from the leaderboard w.r.t order and limits defined.
            parameters:
             - order: (optional, default="DESC") str
             - limit: (optional, default=10) int
            returns: list<dict<str, int>>
        '''
        if order == 'DESC':
            banks = list(self.__data)[1:limit+1]
        elif order == 'ASC':
            banks = (list(self.__data)[-limit:])[::-1]
        data = []
        for bank in banks:
            data.append({bank: self.__data[bank]['Count - BANK']})
        return data

    def get_total(self):
        '''
            description: Returns the total number of branches of all banks in India. [First record]
            parameters: None
            returns: dict<str, int>
        '''
        return {'BANK': 'Total Result', 'Count - BANK': self.__data['Total Result']}


# l = leaderboard()

# l.load_bank_leaderboard_data()
# print(l.get_leaderboard('DESC'))
# l.update_after_search('STATE BANK OF INDIA')
# print(l.get_leaderboard('DESC'))

