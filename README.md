Prerequisite
======================================
* Install [Docker for Mac](https://docs.docker.com/docker-for-mac/)
* Install [Vagrant](https://www.vagrantup.com)

Overview
=====================================
This project implements an [osquery](http://osquery.io/) TLS server for [all its remote APIs](https://github.com/facebook/osquery/blob/master/docs/wiki/deployment/remote.md), including:

* enrollment API
* configuration API
* distributed read API and distributed API

Users can install this app in Splunk and can submit osquery into all osquery clients enrolled and present the data from all enrolled nodes in Splunk.

Screenshots
=====================================
## How it works

![architecture](./assets/arch.png "architecture")

## Query for OS distro distribution
![OS distro distribution query](./assets/os-distro-query.png "OS distro distribution query")

## Visualizing the osquery execution using timeline
* The `query_submitted` swimming lane indicates an osquery is submitted
* Each swimming lane is an enrolled node with osquery installed, each dot on the lane indicates either the query is retrieved by the node or the query result is sent back to the server from the node
![osquery execution timeline](./assets/query-execution-timeline.png "osquery execution timeline")


Get it up and running
======================
* Set up a running environment using Vagrant and Docker for Mac
	* `make up`
	* This will create a Docker container running Splunk Enterprise with the `osquery_tls_server_splunk_app` installed
* Create a cluster of containers with osquery installed
	* Build the Docker images, `make build_osquery_client` 
	* Create a Docker swarm cluster, `docker swarm init`
	* Create the Docker containers within the Docker swarm cluster, `docker stack deploy --compose-file docker-stack.yml osqueryd`
	* All containers will enroll into the osquery TLS serer splunk app automatically

You should now be able to access the Splunk enterprise web UI via http://localhost:8000 with admin/changeme as credentials.


Issue osquery to the TLS server
======================

* (Optional) Install Splunk time line app (https://splunkbase.splunk.com/app/3120/) for visualizing the query submission/query reading/query result writing process by using the following query as real time query (recent 300 seconds):
	`index=main (sourcetype="submitted_query" OR sourcetype="issued_query" OR sourcetype="query_results") | eval title=node_key | fillnull value=query_submitted title | sort - title | table _time, title, sourcetype`
	
* Submit Splunk search like this in search box:
	`` `osquery("SELECT name, major, minor FROM os_version")` | eval distro=name + " " + major | stats count by distro``
	
* One more demo for detecting not on disk process:
	* `docker ps` to find a osquery container id
	* `docker exec -it ${some_osquery_container_id} bash`
	* start a background process in this container, `top &`
	* simulating an intrusion by replacing a running process's binary, `mv /usr/bin/sudo /usr/bin/top`
	* Submit a Splunk search like this to detect this intrusion:
		`` `osquery("SELECT name, pid, path FROM processes WHERE on_disk=0")` ``
	
* For more queries, please consult osquery's [doc](https://osquery.io/docs/tables/)


TODO
=========
* Some of the app configurations, such as the target index used for storing data and the credentials used to talk to Splunk/HEC are hard coded in package/bin/app_config.py, and should be externalized into some configuration file later.
* So far, the osquery will be sent to all enrolled nodes, which may not be desireable in some case, this could be improved by introducing more functions when distributing the queries.