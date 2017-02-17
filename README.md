* Install Splunk time line app (https://splunkbase.splunk.com/app/3120/) for visualizing the query submission/query reading/query result writing process by using the following query:
`index=main (sourcetype="submitted_query" OR sourcetype="issued_query" OR sourcetype="query_results") | eval title=node_key | fillnull value=query_submitted title | sort - title | table _time, title, sourcetype`
