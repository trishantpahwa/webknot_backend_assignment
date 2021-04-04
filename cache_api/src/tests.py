import unittest
from dotenv import load_dotenv
from os import environ
import json
import requests
load_dotenv('.test.env')


class Testing(unittest.TestCase):

    base_url = environ['base_url']

    def test_ifsc_endpoint(self):
        for ifsc_code, expected_status_code in {'IOBA0000955': 200, 'PUNB0482700': 200, 'RATN0000254': 200, 'AAAA0000254': 404, 'RMGB0000460': 200, 'aaa': 422, '': 422, '11111111111': 422, '!@!@!AAA3333': 422}.items():
            response = requests.get(self.base_url + '/ifsc-search?ifsc_code=' + ifsc_code)
            print(ifsc_code)
            print('Response status_code should be equal to ' + str(expected_status_code))
            print('Status code: ' + str(response.status_code))
            print('Body: ' + str(json.loads(response.text)))
            self.assertEqual(response.status_code, expected_status_code)
        
