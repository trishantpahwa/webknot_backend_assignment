import unittest
from dotenv import load_dotenv
from os import environ
import json
from time import time
import requests
load_dotenv('.test.env')


class Testing(unittest.TestCase):

    base_url = environ['base_url']
    stats = [] # Stores path to test statistics route results | list<dict<str,timestamp>>

    def test_ifsc_endpoint(self):
        for ifsc_code, expected_status_code in {'ALLA0210277': 200, 'ANDB0000632': 200, 'BKID0009509': 200, 'CBIA0280502': 404, 'IOBA0000957': 200, '1122IOBA0000957': 422, 'IOBA00009AA': 404, 'asda': 422, '': 422}.items():
            url = self.base_url + '/ifsc-search?ifsc_code=' + ifsc_code
            print('Testing => ' + url + '\n')
            response = requests.get(url)
            self.stats.append({'ifsc_code': ifsc_code, 'timestamp': time()})
            print(ifsc_code)
            print('Response status_code should be equal to ' + str(expected_status_code))
            print('Status code: ' + str(response.status_code))
            print('Body: ' + str(json.loads(response.text)))
            self.assertEqual(response.status_code, expected_status_code)
    
    def test_leaderboard(self):
        for sortorder, fetchcount_list in {'ASC': ['', 1, 3, 5, 10, 15, 20, '', '', -1, 0], 'DESC': [1, '', 3, '', 10, 15, 20, '', '', -1, 0], 'INVALID_SORT_TYPE': ['', 1, 3, 7, 13, 15, 20, '', '', -1, 0], '': ['', 1, 3, 5, 10, 15, 20, '', '', -1, 0]}.items():
            for fetchcount in fetchcount_list:
                query = '?'
                if(sortorder == 'ASC' or sortorder == 'DESC' or sortorder == ''):
                    expected_status_code = 200
                    query += 'sortorder=' + sortorder
                    if sortorder == '':
                        expected_status_code = 422
                else:
                    expected_status_code = 422
                if(fetchcount != ''):
                    if(query != '?'):
                        query += '&'
                    query += 'fetchcount=' + str(fetchcount)
                    if fetchcount > 0 and sortorder != '':
                        expected_status_code = 200
                    else:
                        expected_status_code = 422
                else:
                    if fetchcount == '':
                        expected_status_code = 200
                        if sortorder == '' or sortorder == 'INVALID_SORT_TYPE':
                            expected_status_code = 422
                    else:
                        expected_status_code = 422
                if query == '?':
                    query = ''
                    expected_status_code = 200
                url = self.base_url + '/leaderboard' + query
                print('Testing => ' + url + '\n')
                response = requests.get(url)
                self.stats.append({'path': '/leaderboard', 'timestamp': time()})
                print('Expected code: ' + str(expected_status_code))
                print('Response code: ' + response.status_code)
                print('Body: '+ str(json.loads(response.text)))
                if(expected_status_code == 200 and fetchcount != '' and fetchcount > 0):
                    self.assertEqual(len(json.loads(response.text)['data']), fetchcount)
                self.assertEqual(response.status_code, expected_status_code)

    
    def test_statistics(self):
        print(self.stats)
        for sortorder, fetchcount_list in {'ASC': ['', 1, 3, 5, 10, 15, 20, '', '', -1, 0], 'DESC': [1, '', 3, '', 10, 15, 20, '', '', -1, 0], 'INVALID_SORT_TYPE': ['', 1, 3, 7, 13, 15, 20, '', '', -1, 0], '': ['', 1, 3, 5, 10, 15, 20, '', '', -1, 0]}.items():
            for fetchcount in fetchcount_list:
                query = '?'
                if(sortorder == 'ASC' or sortorder == 'DESC' or sortorder == ''):
                    expected_status_code = 200
                    query += 'sortorder=' + sortorder
                    if sortorder == '':
                        expected_status_code = 422
                else:
                    expected_status_code = 422
                if(fetchcount != ''):
                    if(query != '?'):
                        query += '&'
                    query += 'fetchcount=' + str(fetchcount)
                    if fetchcount > 0 and sortorder != '':
                        expected_status_code = 200
                    else:
                        expected_status_code = 422
                else:
                    if fetchcount == '':
                        expected_status_code = 200
                        if sortorder == '' or sortorder == 'INVALID_SORT_TYPE':
                            expected_status_code = 422
                    else:
                        expected_status_code = 422
                if query == '?':
                    query = ''
                    expected_status_code = 200
                url = self.base_url + '/statistics' + query
                print('Testing => ' + url + '\n')
                response = requests.get(url)
                print('Expected code: ' + str(expected_status_code))
                print('Response code: ' + str(response.status_code))
                print('Body: '+ str(json.loads(response.text)))
                self.assertEqual(response.status_code, expected_status_code)
                if(expected_status_code == 200 and fetchcount != '' and fetchcount > 0):
                    if len(self.stats) < fetchcount:
                        self.assertLessEqual(len(json.loads(response.text)['data']), fetchcount)
                    else:
                        self.assertEqual(len(json.loads(response.text)['data']), fetchcount)
