from base_api_endpoint import RestEndpoint

SIMPLE_CONFIG = {
    "schedule": {
        "process_query": {"query": "select * from processes", "interval": 60},
    },
    "node_invalid": False,
}

class NodeConfig(RestEndpoint):
    def handle_POST(self):
        self._write_json(SIMPLE_CONFIG)