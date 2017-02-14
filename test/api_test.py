import requests
import unittest
import json
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
    
    def get_config(self):
        resp = requests.get(self.api('config'), verify=False)        
        config = resp.json()
        return config 

    def get_enrollments(self):
        resp = requests.get(self.api('enroll'), verify=False)        
        enrollments = resp.json()
        return enrollments
        
    def add_enrollment(self, enrollment):
        resp = requests.post(self.api('enroll'), 
            verify=False, 
            data=json.dumps(enrollment))        
        enrollment_result = resp.json()
        return enrollment_result

class ApiTest(unittest.TestCase):
    def setUp(self):
        self.client = OsqueryClient()
        
    def test_get_info(self):
        info = self.client.get_info()
        self.assertIsNotNone(info)
        
    def test_get_config(self):
        config = self.client.get_config()
        self.assertIsNotNone(config)
        
    def test_get_enroll(self):
        enrollments = self.client.get_enrollments()
        self.assertIsNotNone(enrollments) 
        
    def test_enroll_node(self):
        enrollment_result = self.client.add_enrollment({
            'enroll_secret': 'any_secret',
            'host_identifier': 'test_localhost'    
        })
        self.assertIsNotNone(enrollment_result)
        self.assertIsNotNone(enrollment_result['node_key'])
        self.assertIsNotNone(enrollment_result['node_invalid'])
        