import struct
import socket
import threading

# Create connections
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 7679))
server.listen(5)

print(f'[*] Listening')
client, addr = server.accept()
print(f'[+] Client {addr} connected')

remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
remote.connect(('18.185.88.28', 7679))
print(f'[+] Remote connected')


# Create another thread for piping outgoing traffic
def outgoing():
    while True:
        chunk = client.recv(1024)
        if chunk == b'':
            break
        remote.sendall(chunk)
threading.Thread(target=outgoing).start()


# Main thread for intercepting shellcode chunks
cnt = 0
while True:
    chunk = remote.recv(65536)
    if chunk == b'':
        break

    # Code chunks start with 4 bytes length. All chunks are about 4000 bytes,
    # so 3 and 4 byte will be zero.
    if len(chunk) >= 4 and chunk[2] == 0 and chunk[3] == 0:
        size = struct.unpack('<I', chunk[:4])[0]
        print(f'[*] Detect code {cnt}: len={size}')

        # Receive whole chunk
        size -= len(chunk) - 4
        while size > 0:
            ch = remote.recv(size)
            size -= len(ch)
            chunk += ch

        with open(f'codes/{cnt}.bin', 'wb') as f:
            f.write(chunk[4:])

        input('Continue...')
        cnt += 1

    print(len(chunk))
    client.sendall(chunk)
