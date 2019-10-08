FROM ubuntu:18.04
MAINTAINER sasdf
RUN apt-get update
RUN apt-get install xinetd -y

RUN apt-get install -y python3 python3-pip

RUN pip3 install pycrypto

RUN apt-get install -y python-minimal python-pip

RUN pip install omnihash[sha3,pyblake2] && ln -s /usr/local/bin/omnihash /bin/omnihash

RUN apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m collision

COPY home /home/collision
COPY xinetd /etc/xinetd.d/xinetd

RUN chown -R root:root /home/collision && \
    chown -R root:root /etc/xinetd.d/xinetd && \
    find / -type d -perm /0002 -exec chmod o-w {} + 2>/dev/null ; \
    find / -type f -perm /0002 -exec chmod o-w {} + 2>/dev/null ; \
    echo 'Finish'

CMD ["/usr/sbin/xinetd","-dontfork"]
