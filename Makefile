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

osqueryd:
	osqueryd --verbose \
		--pidfile /tmp/osqueryd.pid \
		--database_path /tmp/osquery.db/ \
		--tls_hostname localhost:8089 \
		--tls_server_certs ./assets/cacert.pem \
		--enroll_tls_endpoint /services/osquery/enroll \
		--enroll_secret_path ./assets/test_enroll_secret.txt \
		--config_plugin tls \
		--logger_plugin tls  \
		--config_tls_endpoint /config \
		--logger_tls_endpoint /log

		#--distributed_plugin=tls \
		#--distributed_tls_read_endpoint /distributed_read \
		#--distributed_tls_write_endpoint /distributed_write \
		#--disable_distributed=false \
		#--distributed_interval=60

.PHONY: test
	
