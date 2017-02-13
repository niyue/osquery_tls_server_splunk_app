import splunk.rest
import json

class RestEndpoint(splunk.rest.BaseRestHandler):
    def writeJson(self, data):
        self.response.write(json.dumps(data))
  
class ServerInfo(RestEndpoint):
    def handle_GET(self):
        info = {
            "name": "osquery TLS server",
            "version": "1.0"
        }
        self.writeJson(info)
        
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
        new_node = json.loads(self.request["payload"])
        enrollments = [{
            "name": "node1",
            "id": "123"
        }, {   
            "name": "node2",
            "id": "456"
        }]
        enrollments.append(new_node)
        self.writeJson(enrollments)
