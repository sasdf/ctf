import requests
import codecs
import hashlib
import multiprocessing as mp
from tqdm import tqdm, trange


base = 'https://quantumpyramids.web.ctfcompetition.com'
sess = requests.Session()


def sign(msg):
    body = {"message": codecs.encode(msg, 'base64').decode().replace('\n', '')}
    res = sess.post(base + '/sign', json=body)
    assert res.status_code == 200
    res = res.json()
    assert res['status'] == 'Signature created.', res
    return codecs.decode(res['signature'].encode(), 'base64')


queue = mp.Queue(128)
def worker():
    global sess
    sess = requests.Session()
    while True:
        sig = sign(b'abc')
        queue.put(sig)


procs = [mp.Process(target=worker) for i in range(3)]
for p in procs:
    p.start()


with open('sigs.txt', 'a') as f:
    bar = tqdm()
    while True:
        bar.update(1)
        sig = queue.get()
        f.write(sig.hex() + '\n')
        f.flush()
    bar.close()
