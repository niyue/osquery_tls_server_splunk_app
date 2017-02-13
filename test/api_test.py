import requests
import unittest
from urlparse import urljoin
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

BASE_URL = 'https://localhost:8089'

class OsqueryClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url    
    
    def api(self, path):
        return urljoin(self.base_url, '/services/osquery/' + path) 
    
    def get_info(self):
        resp = requests.get(self.api('info'), verify=False)        
        info = resp.json()
        return info

    def get_enrollments(self):
        resp = requests.get(self.api('enroll'), verify=False)        
        enrollments = resp.json()
        return enrollments

class ApiTest(unittest.TestCase):
    def test_get_info(self):
        client = OsqueryClient()
        info = client.get_info()
        self.assertIsNotNone(info)
        
    def test_get_enroll(self):
        client = OsqueryClient()
        enrollments = client.get_enrollments()
        self.assertIsNotNone(enrollments)    