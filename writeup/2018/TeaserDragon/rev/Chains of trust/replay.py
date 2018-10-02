import struct
import socket
import pickle
import threading

# Create connections
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 7679))
server.listen(5)

# Load all traffics
with open('packets.pkl', 'rb') as f:
    packets = pickle.load(f)


def recv(client, n):
    """ Receive n bytes from the socket """
    chunk = b''
    while n > 0:
        ch = client.recv(n)
        if ch == b'':
            raise EOFError()
        chunk += ch
        n -= len(ch)
    assert(n == 0)
    return chunk


def handle(client):
    """ Replay the traffic """
    try:
        skip = False
        for i, p in enumerate(packets):
            # skip following communication if a code chunk is skipped.
            if skip and p['type'] != 2:
                continue

            print(f'[*] Replay packet {i}')
            if p['type'] == 0: # Output packets
                res = recv(client, len(p['data']))
            elif p['type'] == 1: # Input packets
                client.sendall(p['data'])
            elif p['type'] == 2: # Code packets
                skip = p["data"] in [10, 68, 72, 76, 81, 82, 87]
                if not skip:
                    print(f'[*] Replay code {p["data"]}')
                    input('cont')
                    with open(f'codes/{p["data"]}.bin', 'rb') as f:
                        data = f.read()
                    data = struct.pack('<I', len(data)) + data
                    client.sendall(data)

        # Keep the connection open
        while True:
            recv(client, 1024)
    except EOFError:
        pass

# Main loop of threaded server
while True:
    client, addr = server.accept()
    threading.Thread(target=handle, args=(client,)).start()
