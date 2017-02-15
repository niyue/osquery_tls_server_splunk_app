import json
from base_api_endpoint import RestEndpoint
import app_config
import uuid

class AdHocQueriesCollection(RestEndpoint):
    def handle_POST(self):
        query_info = json.loads(self.request['payload'])
        query = query_info['query']
        remote_address = self.request['remoteAddr']
        query_id = query_info.get('query_id') or str(uuid.uuid4())
        self._send_event({'query_id': query_id, 'query': query}, 
                app_config.TARGET_INDEX, 'submitted_query', remote_address)
        self._write_json({
            'query_id': query_id,
            'query': query
        })
