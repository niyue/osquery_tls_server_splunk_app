import splunk.rest
import json
import uuid
import socket
from uHEC import http_event_collector

ENROLL_SECRET = 'this_is_enroll_secret'
TARGET_INDEX = 'main'

http_event_collector_key_json = '00000000-0000-0000-0000-000000000000'
http_event_collector_host = 'localhost'

hec = http_event_collector(http_event_collector_key_json, 
    http_event_collector_host)

FAILED_ENROLL_RESPONSE = {
    "node_invalid": True
}

ENROLL_RESPONSE = {
    "node_key": "this_is_a_node_secret"
}

SIMPLE_CONFIG = {
    "schedule": {
        "process_query": {"query": "select * from processes", "interval": 60},
    },
    "node_invalid": False,
}

class RestEndpoint(splunk.rest.BaseRestHandler):
    def writeJson(self, data):
        self.response.setHeader('content-type', 'application/json')
        self.response.write(json.dumps(data))
  
class ServerInfo(RestEndpoint):
    def handle_GET(self):
        info = {
            "name": "osquery TLS server",
            "version": "1.0"
        }
        self.writeJson(info)
        
class NodeConfig(RestEndpoint):
    def handle_POST(self):
        self.writeJson(SIMPLE_CONFIG)
        
class Logger(RestEndpoint):
    
    SUCCESS = {'node_invalid': False}
    
    def handle_POST(self):
        event = json.loads(self.request["payload"])
        self._add_log(event)
        self.writeJson(Logger.SUCCESS)
        
    def _add_log(self, event):
        payload = {}
        payload.update({'index': TARGET_INDEX})
        payload.update({'sourcetype': 'events'})
        payload.update({'source': event.get('node_key')})
        payload.update({'host': socket.gethostname()})
        payload.update({'event': event})
        hec.sendEvent(payload)
        
class EnrollmentCollection(RestEndpoint):
    def handle_GET(self):
        enrollments = [{
            "name": "node1",
            "id": "123"
        }, {   
            "name": "node2",
            "id": "456"
        }]
        self.writeJson(enrollments)
        
    def handle_POST(self):
        enrollment = json.loads(self.request["payload"])
        #if ENROLL_SECRET != enrollment['enroll_secret']:
        #    self.writeJson(FAILED_ENROLL_RESPONSE)
        #else:
        enroll_secret = enrollment['enroll_secret']
        host_identifier = enrollment['host_identifier']
        node_key = str(uuid.uuid4())
        self._add_node_enrollment(host_identifier, node_key)        
        enroll_success = {
            'node_key': node_key,
            'node_invalid': False
        } 
        self.writeJson(enroll_success)

    def _add_node_enrollment(self, host_identifier, node_key):
        payload = {}
        payload.update({'index': TARGET_INDEX})
        payload.update({'sourcetype': 'enrollment'})
        payload.update({'source': host_identifier})
        payload.update({'host': socket.gethostname()})
        payload.update({'event': {
            'node_key': node_key
        }})
        hec.sendEvent(payload)
        
    
