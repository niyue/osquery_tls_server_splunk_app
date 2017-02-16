import requests
from requests.auth import HTTPBasicAuth
import unittest
import json
from urlparse import urljoin
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

BASE_URL = 'https://localhost:8089'
USERNAME = 'admin'
PASSWORD = 'changeme'

class OsqueryClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url    
    
    def api(self, path):
        return urljoin(self.base_url, '/services/osquery/' + path) 
    
    def get_info(self):
        resp = requests.get(self.api('info'), verify=False)        
        info = resp.json()
        return info
        
    def submit_ad_hoc_query(self, query):
        resp = requests.post(self.api('ad_hoc_queries'), verify=False, data=json.dumps({
            'query': query    
        }))        
        result = resp.json()
        return result 
    
    def get_config(self, node_key):
        resp = requests.post(self.api('config'), verify=False, data=json.dumps({
            'node_key': node_key
        }))        
        config = resp.json()
        return config 
        
    def add_log(self, node_key, log_type, events):
        resp = requests.post(self.api('logger'), verify=False, data=json.dumps({
            'node_key': node_key,
            'log_type': log_type,
            'data': events
        }))        
        result = resp.json()
        return result 

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
        
    def read_queries(self, node_key):
        resp = requests.post(self.api('distributed_read'), 
            verify=False, 
            data=json.dumps({'node_key': node_key}))        
        queries = resp.json()
        return queries
        
    def write_query_results(self, node_key, queries, statuses):
        resp = requests.post(self.api('distributed_write'), 
            verify=False, 
            data=json.dumps({
                'node_key': node_key,
                'queries': queries,
                'statuses': statuses}))        
        result = resp.json()
        return result
        
    def run_submit_ad_hoc_query_command(self, command):
        job_export_api = urljoin(self.base_url, '/services/search/jobs/export') 
        resp = requests.post(job_export_api, 
            verify=False, 
            data={'search': command},
            params={'output_mode': 'json'},
            auth=HTTPBasicAuth(USERNAME, PASSWORD))        
        results = resp.json()
        return results


class ApiTest(unittest.TestCase):
    def setUp(self):
        self.client = OsqueryClient()
        
    def test_get_info(self):
        info = self.client.get_info()
        self.assertIsNotNone(info)
        
    def test_get_config(self):
        config = self.client.get_config('test_node_key')
        self.assertIsNotNone(config)
        self.assertFalse(config['node_invalid'])
        
    def test_add_log(self):
        result = self.client.add_log('test_node_key', 'status', [])
        self.assertIsNotNone(result)
        self.assertFalse(result['node_invalid'])
        
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
        
    def test_read_queries(self):
        queries = self.client.read_queries('test_node_key')
        self.assertIsNotNone(queries)
        self.assertFalse(queries['node_invalid'])
        
    def test_write_query_results(self):
        result = self.client.write_query_results('test_node_key', {
            'test_query_id': {
                'pid': '1',
                'name': 'osqueryd'
            }
        }, {'test_query_id': 0})
        self.assertIsNotNone(result)
        self.assertFalse(result['node_invalid'])
        
    def test_submit_ad_hoc_query(self):
        result = self.client.submit_ad_hoc_query('SELECT * FROM processes')
        self.assertIsNotNone(result) 
        self.assertIsNotNone(result['query_id']) 
        self.assertIsNotNone(result['query']) 
        
    def test_run_ad_hoc_query_command(self):
        results = self.client.run_submit_ad_hoc_query_command('| osquery "SELECT * FROM processes"')
        self.assertIsNotNone(results) 
        self.assertEqual(2, len(results['result']))
        self.assertIsNotNone(results['result']['query_id'])
        self.assertEqual('SELECT * FROM processes', results['result']['query'])
        
    
        