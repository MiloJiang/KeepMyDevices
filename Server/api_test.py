import unittest
import requests
import json
from datetime import datetime

class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://127.0.0.1:5000"

    def getToken(self):
        url = self.base_url + '/auth'
        payload = {'username': 'admin', 'password': 'admin'}
        r = requests.post(url, json=payload)
        self.token = json.loads(r.text)["access_token"]
        return self.token

    def tearDown(self):
        pass

    def testAuth(self):
        url = self.base_url + '/auth'
        payload = {'username': 'admin', 'password': 'admin'}
        r = requests.post(url, json=payload)
        self.token = json.loads(r.text)["access_token"]
        print r.text
        self.assertIn(u'access_token', r.text)

        url = self.base_url + '/api/v1/device'
        headers = {'Authorization': 'JWT ' + self.token}
        r = requests.get(url, headers=headers)
        print r.text

    def testUpdate(self):
        url = self.base_url +'/api/v1/device'
        self.getToken()
        headers = {'Authorization': 'JWT ' + self.token}
        payload = {'brand': 'testbrand',
                   'model': 'testmodel',
                   'sn': '11',
                   }
        r = requests.post(url, headers=headers, json=payload)
        print r.text

        payload = {'brand': 'testbrand',
                   'model': '',
                   'sn': '12',
                   'timestamp': str(datetime.now())
                   }
        r = requests.post(url, headers=headers, json=payload)
        print r.text



if __name__ == '__main__':
    unittest.main()