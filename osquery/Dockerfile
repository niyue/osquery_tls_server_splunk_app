FROM ubuntu:trusty

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 1484120AC4E9F8A1A577AEEE97A80C63C9D8B80B
RUN echo "deb [arch=amd64] http://osquery-packages.s3.amazonaws.com/trusty trusty main" > /etc/apt/sources.list.d/osquery.list
RUN apt-get update && apt-get install osquery

COPY ./assets/cacert.pem /tmp/cacert.pem
COPY ./assets/test_enroll_secret.txt /tmp/test_enroll_secret.txt

ENTRYPOINT ["/usr/bin/osqueryd", "--verbose", "--pidfile", "/tmp/osqueryd.pid", "--database_path", "/tmp/osquery.db/", "--config_plugin", "tls", "--config_tls_endpoint", "/services/osquery/config", "--logger_tls_endpoint", "/services/osquery/logger", "--distributed_tls_read_endpoint", "/services/osquery/distributed_read", "--distributed_tls_write_endpoint", "/services/osquery/distributed_write", "--enroll_tls_endpoint", "/services/osquery/enroll", "--logger_plugin", "tls", "--distributed_plugin=tls", "--disable_distributed=false", "--distributed_interval=10"]  

CMD ["--tls_hostname", "SplunkServerDefaultCert:8089", "--tls_server_certs", "/tmp/cacert.pem", "--enroll_secret_path", "/tmp/test_enroll_secret.txt"]
