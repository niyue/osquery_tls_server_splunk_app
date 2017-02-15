build:
	vagrant destroy --force; VAGRANT_LOG=info vagrant up
	
ssh:
	docker exec -it osquery bash
	
restart:
	docker exec osquery "/opt/splunk/bin/splunk" restart

install:
	docker exec osquery ln -sf /vagrant/package /opt/splunk/etc/apps/osquery_tls_server_splunk_app
	docker exec osquery cp -rf /vagrant/provision/server.conf /opt/splunk/etc/system/local
	make restart
	
up: build
	echo "waiting splunk server to initialize"
	sleep 180
	make install
	
test:
	nosetests test/*_test.py -v --with-id

build_osquery_client:
	docker build --file osqueryDockerfile --tag niyue/osquery .

osqueryd:
	docker run --add-host SplunkServerDefaultCert:172.17.0.1 niyue/osquery

.PHONY: test
	
