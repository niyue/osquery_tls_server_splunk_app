import re, sys, time, splunk.Intersplunk
import logging
import uuid

logger = logging.getLogger('splunk.rest')

import app_config
import requests
import json
from urlparse import urljoin
#from requests.packages.urllib3.exceptions import InsecureRequestWarning

# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def _submit_ad_hoc_query(query):
    base_url = 'https://%s:%s' % (app_config.HOST, app_config.PORT)
    ad_hoc_query_api = urljoin(base_url, '/services/osquery/ad_hoc_queries') 
    resp = requests.post(ad_hoc_query_api, verify=False, data=json.dumps({
        'query': query    
    }))        
    result = resp.json()
    return [result]
    
def _remove_double_quotes_and_unescape(query):
    query = query[1:-1]
    query = query.replace('"', '\\"')
    return query

query = ''
if len(sys.argv) > 1:
    query = sys.argv[1]
    query = _remove_double_quotes_and_unescape(query)
    
logger.info('action=perform_osquery_command query=%s', query)
    
try:
    results, dummyresults, settings = splunk.Intersplunk.getOrganizedResults()
    results = _submit_ad_hoc_query(query)
    splunk.Intersplunk.outputResults(results)
except:
    import traceback
    stack =  traceback.format_exc()
    results = splunk.Intersplunk.generateErrorResults("Error : Traceback: " + str(stack))