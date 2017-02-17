import app_config
import json
import time
from base_api_endpoint import RestEndpoint

import logging
logger = logging.getLogger('splunk.rest')

class DistributedWrite(RestEndpoint):
    def handle_POST(self):
        logger.info('action=distributed_write')
        query_results = json.loads(self.request["payload"])
        node_key = query_results.get('node_key')
        logger.debug('action=distributed_write_all_query_results node_key=%s results=%s', node_key, query_results)
        query_statuses = query_results['statuses']
        logger.info('action=distributed_write_query_results results=%s node_key=%s', len(query_statuses), node_key)
        for query_id, status in query_statuses.iteritems():
            self._write_query_result(query_id, status, node_key, query_results)

        SUCCESS = {
            "node_invalid": False
        }
        self._write_json(SUCCESS)

    def _write_query_result(self, query_id, status, node_key, query_results):
        source = query_id + '_' + node_key
        if self._is_query_success(status):
            rows = query_results['queries'][query_id]
            now = str(int(time.time()))
            for row in rows:
                logger.debug('action=process_query_result_row query_id=%s node_key=%s row=%s', query_id, node_key, row)
                row['_query_id'] = query_id
                row['_node_key'] = node_key
                self._send_event(row, app_config.TARGET_INDEX, 'query_results', source, event_time=now)
        else:
            self._send_event({'query_id': query_id, 'node_key': node_key, 'status': status},
                app_config.TARGET_INDEX, 'failed_queries', source)

    def _is_query_success(self, status):
        return status == '0'
