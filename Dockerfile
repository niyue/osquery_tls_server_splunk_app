FROM splunk/splunk:6.5.2

#RUN add-apt-repository "deb [arch=amd64] https://osquery-packages.s3.amazonaws.com/xenial xenial main"
RUN apt-get update \
	&& apt-get install -y vim \
	&& apt-get install -y curl 


EXPOSE 8000
EXPOSE 8089
