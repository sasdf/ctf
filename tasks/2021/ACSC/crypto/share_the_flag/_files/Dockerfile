FROM python:3.8-slim

RUN apt-get -y update --fix-missing && \
    apt-get -y upgrade && \
    apt-get -y install xinetd && \
    useradd share_the_flag && \
    echo "Done"

COPY challenge/xinetd /etc/xinetd.d/xinetd
COPY challenge/chall.py /chall.py
COPY challenge/flag.txt /flag.txt
WORKDIR /

CMD ["/usr/sbin/xinetd", "-dontfork"]
