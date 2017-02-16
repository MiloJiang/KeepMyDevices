import unittest
import requests
import json

class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://127.0.0.1:5000"

    def tearDown(self):
        pass

    def testAuth(self):
        url = self.base_url + '/auth'
        payload = {'username': 'admin', 'password': 'admin'}
        r = requests.post(url, json=payload)
        self.token = json.loads(r.text)["access_token"]
        # print r.text
        self.assertIn(u'access_token', r.text)

        url = self.base_url + '/api/v1/device'
        headers = {'Authorization': 'JWT ' + self.token}
        r = requests.get(url, headers=headers)
        print r.text

if __name__ == '__main__':
    unittest.main()