FROM splunk/splunk:6.5.2-monitor

RUN apt-get update \
	&& apt-get install -y vim \
	&& apt-get install -y curl 
    
RUN mkdir -p /opt/splunk/etc/apps \
    && ln -s /vagrant/package /opt/splunk/etc/apps/osquery_tls_server_splunk_app

EXPOSE 8000 8089
