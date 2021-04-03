from time import time


class statistics:
    '''
        %%%% statistics %%%%
        description: Statistics of logs for each successful request, whose data was found, with recorded timestamp
        variables:
         - __data: list<dict<str, str>>
        functions:
         - search: Inserts entry into the log for the searched IFSC code.
         - get_data: Formats the statistics data w.r.t order and limit
    '''
    __data = []

    def search(self, ifsc):
        '''
            description: Inserts entry into the log for the searched IFSC code.
            parameters:
             - ifsc: (required) str
            returns: None
        '''
        self.__data.append({'ifsc': ifsc, 'timestamp': time()})

    def get_data(self, order='ASC', limit=None):
        '''
            description: Formats the statistics data w.r.t order and limit
            parameters:
             - order: (optional, default="DESC") str
             - limit: (optional, default=10) int
            returns: list<dict<str,str>>
        '''
        if order == 'ASC':
            if limit is not None:
                return self.__data[:limit]
            else:
                return self.__data
        elif order == 'DESC':
            if limit is not None:
                return (self.__data)[-(int(limit)):][::-1]
            else:
                return self.__data[::-1]


# s = statistics()

# s.search('test1')
# s.search('test2')
# s.search('test3')
# s.search('test4')
# s.search('test5')
# s.search('test6')

# print(s.get_data('ASC', 5))
# print(s.get_data('DESC', 2))
