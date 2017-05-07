build:
	vagrant up

rebuild:
	vagrant destroy --force; VAGRANT_LOG=info vagrant up
	
ssh:
	docker exec -it osquery bash
	
restart:
	docker exec osquery "/opt/splunk/bin/splunk" restart

clean_index:
	docker exec osquery "/opt/splunk/bin/splunk" stop
	docker exec osquery "/opt/splunk/bin/splunk" clean eventdata -index main
	docker exec osquery "/opt/splunk/bin/splunk" start

install:
	docker exec osquery ln -sf /vagrant/package /opt/splunk/etc/apps/osquery_tls_server_splunk_app
	docker exec osquery cp -rf /vagrant/assets/server.conf /opt/splunk/etc/system/local
	make restart
	
up: build
	echo "waiting splunk server to initialize"
	sleep 180
	make install
	
test:
	nosetests test/*_test.py -v --with-id

build_osquery_client:
	docker build --file osquery/Dockerfile --tag niyue/osquery .
	docker build --file osquery/centosDockerfile --tag niyue/osquery:centos .
	docker build --file osquery/centos6Dockerfile --tag niyue/osquery:centos6 .

add_clients:
	docker stack deploy --compose-file docker-stack.yml osqueryd

rm_clients:
	docker stack rm osqueryd

osqueryd:
	docker run --add-host SplunkServerDefaultCert:172.17.0.1 niyue/osquery
	
.PHONY: test
	
