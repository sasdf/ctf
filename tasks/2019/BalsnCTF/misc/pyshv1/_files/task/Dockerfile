FROM ubuntu:18.04
MAINTAINER sasdf
RUN apt-get update
RUN apt-get install xinetd -y

RUN apt-get install -y python3 python3-pip

RUN apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m pyshv1

COPY home /home/pyshv1
COPY xinetd /etc/xinetd.d/xinetd

RUN chown -R root:root /home/pyshv1 && \
    chown -R root:root /etc/xinetd.d/xinetd && \
    find / -type d -perm /0002 -exec chmod o-w {} + 2>/dev/null ; \
    find / -type f -perm /0002 -exec chmod o-w {} + 2>/dev/null ; \
    echo 'Finish'

CMD ["/usr/sbin/xinetd","-dontfork"]
