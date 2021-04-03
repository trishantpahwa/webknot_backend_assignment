import pandas as pd
from os import environ
import collections


class leaderboard:

    __data = {}  # BANK: COUNT - BANK

    def load_bank_leaderboard_data(self):
        data = pd.read_excel(environ.get('DATASTORE'), sheet_name=1, verbose=True)
        self.__data = data.set_index('BANK').to_dict('index')

    def get_leaderboard(self, order='DESC', limit=10):
        if order == 'DESC':
            banks = list(self.__data)[1:limit+1]
        elif order == 'ASC':
            banks = (list(self.__data)[-limit:])[::-1]
        data = []
        for bank in banks:
            data.append({'bank': bank, 'count': self.__data[bank]})
        return data

    def get_total(self):
        return {'BANK': 'Total Result', 'Count - BANK': self.__data['Total Result']}

    def update_after_search(self, ifsc):
        self.__data[ifsc]['Count - BANK'] += 1
        self.__data['Total Result']['Count - BANK'] += 1


# l = leaderboard()

# l.load_bank_leaderboard_data()
# print(l.get_leaderboard('DESC'))
# l.update_after_search('STATE BANK OF INDIA')
# print(l.get_leaderboard('DESC'))

