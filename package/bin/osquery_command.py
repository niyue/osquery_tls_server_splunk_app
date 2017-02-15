import re, sys, time, splunk.Intersplunk
import logging
import uuid

logger = logging.getLogger('splunk.rest')

def _submit_ad_hoc_query(query):
    query_id = str(uuid.uuid4())
    return [{'query_id': query_id, 'query': query}]
    
query = ''
if len(sys.argv) > 1:
    query = sys.argv[1]
    
logger.info('action=perform_osquery_command query=%s', query)
    
try:
    results, dummyresults, settings = splunk.Intersplunk.getOrganizedResults()
    results = _submit_ad_hoc_query(query)
    splunk.Intersplunk.outputResults(results)
except:
    import traceback
    stack =  traceback.format_exc()
    results = splunk.Intersplunk.generateErrorResults("Error : Traceback: " + str(stack))