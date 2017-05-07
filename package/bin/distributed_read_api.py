import json
from base_api_endpoint import RestEndpoint
import app_config
from splunk.appserver.mrsparkle.lib import util
import os, sys
sys.path.append(os.path.join(util.get_apps_dir(), 'framework', 'contrib', 'splunk-sdk-python'))
import splunklib.client as client
import splunklib.results as results

class DistributedRead(RestEndpoint):
    def handle_POST(self):
        node_info = json.loads(self.request['payload'])
        node_key = node_info.get('node_key')
        queries_for_node = self._pending_ad_hoc_queries_for_node(node_key)
        queries = {
            'queries': queries_for_node,
            'node_invalid': False
        }
        for query_id, query in queries['queries'].iteritems():
            self._send_event({'node_key': node_key, 'query_id': query_id, 'query': query}, 
                app_config.TARGET_INDEX, 'issued_query', node_key)
        
        self._write_json(queries)
    
    def _pending_ad_hoc_queries_for_node(self, node_key):
        search = self._pending_queries_search_string(node_key)
        service = self._get_service()
        results = self._exec_search(service, search)
        self._logger().info('action=pending_queries_retrieved results=%s', len(results))
        queries = dict((r['query_id'], r['query']) for r in results)
        return queries
        
    def _pending_queries_search_string(self, node_key):
        # queries not in issued query but in recent (>= yesterday) submitted_query
        return 'search index=main sourcetype="submitted_query" earliest=-1d NOT [search index=main sourcetype=issued_query node_key=%s earliest=-1d | table query_id] | fields query_id, query' % node_key
        
    def _get_service(self):
        return client.connect(
            username=app_config.USER, 
            password=app_config.PASSWORD,
            host=app_config.HOST,
            port=app_config.PORT)
        
    def _exec_search(self, service, search):
        self._logger().info('action=about_to_execute_pending_queries_search search="%s"', search)
        job = service.jobs.create(search, **{'exec_mode': 'blocking'})
        self._logger().debug('action=finish_pending_queries_search job="%s"', job.content)
        if job.content.get('messages') and job.content.get('messages').get('error'):
            raise RuntimeError(job.content.messages['error'])
        else:
            kwargs_paginate = {'count': 0}
            search_results = job.results(**kwargs_paginate)
            reader = results.ResultsReader(search_results)
            return list(reader)
