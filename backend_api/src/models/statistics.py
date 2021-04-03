from time import time


class statistics:

    __data = []

    def search(self, ifsc):
        self.__data.append({'ifsc': ifsc, 'timestamp': time()})

    def get_data(self, order='ASC', limit=None):
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
