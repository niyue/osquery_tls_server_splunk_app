import splunk.rest
import json
import uuid
import socket
import time
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

def _now():
    return str(int(time.time()))

def _send_event(event, index, sourcetype, source, event_time=_now()):
    payload = {}
    payload.update({'index': index})
    payload.update({'sourcetype': sourcetype})
    payload.update({'source': source})
    payload.update({'host': socket.gethostname()})
    payload.update({'event': event})
    payload.update({'time': event_time})
    hec.sendEvent(payload)

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
        _send_event(event, TARGET_INDEX, 'event', event.get('node_key'))
        
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
        event = {'event': {
            'node_key': node_key
        }}
        _send_event(event, TARGET_INDEX, 'enrollment', host_identifier)
        
class DistributedRead(RestEndpoint):
    def handle_POST(self):
        node_info = json.loads(self.request["payload"])
        node_key = node_info.get('node_key')
        queries = {
            "queries": {
                str(uuid.uuid4()): "SELECT * FROM osquery_info",
                str(uuid.uuid4()): "SELECT * FROM processes"
            },
            "node_invalid": False
        }
        for query_id, query in queries['queries'].iteritems():
            _send_event({'node_key': node_key, 'query_id': query_id, 'query': query}, 
                TARGET_INDEX, 'issued_query', node_key)
        
        self.writeJson(queries)
        
class DistributedWrite(RestEndpoint):
    def handle_POST(self):
        query_results = json.loads(self.request["payload"])
        query_statuses = query_results['statuses']
        node_key = query_results.get('node_key')
        for query_id, status in query_statuses.iteritems():
            self._write_query_result(query_id, status, node_key, query_results)
                
        SUCCESS = {
            "node_invalid": False
        }
        self.writeJson(SUCCESS)
        
    def _write_query_result(self, query_id, status, node_key, query_results):
        source = query_id + '_' + node_key
        if self._is_query_success(status):
            rows = query_results['queries'][query_id]
            now = _now()
            for row in rows:
                row['_query_id'] = query_id
                row['_node_key'] = node_key
                _send_event(row, TARGET_INDEX, 'query_results', source, event_time=now)
        else:
            _send_event({'query_id': query_id, 'node_key': node_key, 'status': status}, TARGET_INDEX, 'failed_queries', source)
        
    def _is_query_success(self, status):
        return status == '0'
