import splunk.rest
import json
import socket
import time
from uHEC import http_event_collector
import app_config
import logging

hec = http_event_collector(app_config.HTTP_EVENT_COLLECTOR_KEY_JSON, 
    app_config.HTTP_EVENT_COLLECTOR_HOST)

class RestEndpoint(splunk.rest.BaseRestHandler):
    def _logger(self):
        return logging.getLogger('splunk.rest')
    
    def _write_json(self, data):
        self.response.setHeader('content-type', 'application/json')
        self.response.write(json.dumps(data))

    def _now():
        return str(int(time.time()))
        
    def _send_event(self, event, index, sourcetype, source, event_time=_now()):
        payload = {}
        payload.update({'index': index})
        payload.update({'sourcetype': sourcetype})
        payload.update({'source': source})
        payload.update({'host': socket.gethostname()})
        payload.update({'event': event})
        payload.update({'time': event_time})
        hec.sendEvent(payload)  
        

        

