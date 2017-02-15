import json
import uuid
from base_api_endpoint import RestEndpoint
import app_config

class DistributedRead(RestEndpoint):
    def handle_POST(self):
        node_info = json.loads(self.request['payload'])
        node_key = node_info.get('node_key')
        queries = {
            'queries': {
                str(uuid.uuid4()): 'SELECT * FROM osquery_info',
                str(uuid.uuid4()): 'SELECT * FROM processes'
            },
            'node_invalid': False
        }
        for query_id, query in queries['queries'].iteritems():
            self._send_event({'node_key': node_key, 'query_id': query_id, 'query': query}, 
                app_config.TARGET_INDEX, 'issued_query', node_key)
        
        self._write_json(queries)