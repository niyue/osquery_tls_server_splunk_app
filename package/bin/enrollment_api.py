from base_api_endpoint import RestEndpoint
import uuid
import json
import app_config

ENROLL_SECRET = 'this_is_enroll_secret'

FAILED_ENROLL_RESPONSE = {
    "node_invalid": True
}

ENROLL_RESPONSE = {
    "node_key": "this_is_a_node_secret"
}

class EnrollmentCollection(RestEndpoint):
    def handle_GET(self):
        enrollments = [{
            "name": "node1",
            "id": "123"
        }, {   
            "name": "node2",
            "id": "456"
        }]
        self._write_json(enrollments)
        
    def handle_POST(self):
        enrollment = json.loads(self.request["payload"])
        self._logger().info('action=enrollment_request enrollment=%s', enrollment)
        #if ENROLL_SECRET != enrollment['enroll_secret']:
        #    self._write_json(FAILED_ENROLL_RESPONSE)
        #else:
        enroll_secret = enrollment['enroll_secret']
        host_identifier = enrollment['host_identifier']
        node_key = str(uuid.uuid4())
        self._add_node_enrollment(host_identifier, node_key)        
        enroll_success = {
            'node_key': node_key,
            'node_invalid': False
        } 
        self._write_json(enroll_success)

    def _add_node_enrollment(self, host_identifier, node_key):
        event = {'event': {
            'node_key': node_key
        }}
        self._send_event(event, app_config.TARGET_INDEX, 'enrollment', host_identifier)
        