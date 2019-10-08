FROM ubuntu:18.04
MAINTAINER sasdf
RUN apt-get update
RUN apt-get install xinetd -y

RUN apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m securenote

COPY home /home/securenote
COPY xinetd /etc/xinetd.d/xinetd

RUN chown -R root:root /home/securenote && \
    chown -R root:root /etc/xinetd.d/xinetd && \
    find / -type d -perm /0002 -exec chmod o-w {} + 2>/dev/null ; \
    find / -type f -perm /0002 -exec chmod o-w {} + 2>/dev/null ; \
    echo 'Finish'

RUN diff /lib/x86_64-linux-gnu/libc.so.6 /home/securenote/task/libc

CMD ["/usr/sbin/xinetd","-dontfork"]
