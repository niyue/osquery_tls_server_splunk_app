from base_api_endpoint import RestEndpoint
import json
import app_config

class Logger(RestEndpoint):
    
    SUCCESS = {'node_invalid': False}
    
    def handle_POST(self):
        event = json.loads(self.request["payload"])
        self._add_log(event)
        self._write_json(Logger.SUCCESS)
        
    def _add_log(self, event):
        self._send_event(event, app_config.TARGET_INDEX, 'event', event.get('node_key'))