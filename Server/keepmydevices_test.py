import os
import keepmydevices
import unittest
import tempfile

class KeepMyDevicesTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, keepmydevices.app.config['DATABASE'] = tempfile.mkstemp()
        keepmydevices.app.config['TESTING'] = True
        self.app = keepmydevices.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(keepmydevices.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()