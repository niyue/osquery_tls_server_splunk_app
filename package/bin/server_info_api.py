from base_api_endpoint import RestEndpoint

class ServerInfo(RestEndpoint):
    def handle_GET(self):
        info = {
            "name": "osquery TLS server",
            "version": "1.0"
        }
        self._write_json(info)