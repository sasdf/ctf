import requests
import codecs
import multiprocessing as mp
from tqdm import tqdm


sess = requests.Session()

URL = 'https://remotecontrol-iothub.web.ctfcompetition.com/SendIRCommand'


def crc8(data):
    # Expect a list of integer
    # LFSR calculation of CRC8-CCITT
    crc = 0
    for v in data:
        crc = crc ^ (v << 8)
        for i in range(8):
            if (crc & 0x8000):
                crc = crc ^ (0x1070 << 3)
            crc = crc << 1
    return bytes([(crc >> 8)])


def buildPkt(cmd, argument):
    p = bytes([0x55, len(argument) + 4, cmd] + list(argument))
    return p + crc8(p)


def buildNECSig(cmd):
    ret = []
    for s in range(8):
        if (cmd >> s) & 1:
            ret += [1] + [0] * round(2250 / 560 - 1)
        else:
            ret += [1] + [0]
    return ret

    
def buildNEC(addr, cmd):
    sig = []
    sig += [1] * round(9000 / 560) # leading burst
    sig += [0] * round(4500 / 560) # leading pause
    sig += buildNECSig(addr)
    sig += buildNECSig(addr ^ 0xff)
    sig += buildNECSig(cmd)
    sig += buildNECSig(cmd ^ 0xff)
    sig += [1] # Final burst

    assert len(sig) == 121

    sz = (len(sig) + 7) // 8

    # Find the correct bit order
    # sig = int(''.join(map(str, sig)), 2).to_bytes(sz, 'big')
    # sig = int(''.join(map(str, sig)), 2).to_bytes(sz, 'little')
    # sig = int(''.join(map(str, sig[::-1])), 2).to_bytes(sz, 'big')
    sig = int(''.join(map(str, sig[::-1])), 2).to_bytes(sz, 'little')

    return sig
    

def worker(i):
    addr, cmd = i // 256, i % 256
    addr = 0x00
    realpkt = b'\0' * 50 + buildNEC(addr, cmd) + b'\0' * 50
    # realpkt = bytes((i + 0x12) ^ e for i, e in enumerate(realpkt))
    packet = buildPkt(0x81, realpkt)
    packet_hex = codecs.encode(packet, 'hex').decode()
    res = requests.post(URL, data=packet_hex)
    r = res.text.strip()
    if r != packet_hex[4:-2]:
        return r
    return None


pool = mp.Pool(64)
# for x in tqdm(pool.imap_unordered(worker, range(0, 65536)), total=65536):
for x in tqdm(pool.imap_unordered(worker, range(0, 256)), total=256):
    if x:
        tqdm.write(x)
        break
pool.terminate()
pool.join()
