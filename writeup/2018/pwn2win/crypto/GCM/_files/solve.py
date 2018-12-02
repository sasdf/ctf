import ast
import copy
import multiprocessing as mp
from firstblood.all import uio

r = uio.tcp('200.136.252.51', 5555)
# r = uio.spawn('python2 -u gcm.py 2>&1')

token = r.line('1').line('abc').line('abc').after('token:\n').line()
token = ast.literal_eval(token)
r.close()

enc = token['enc'].hexd
enc = enc[:30] + enc[30:31].xor(b'N').xor(b'Y') + enc[31:]
token['enc'] = enc.hexe


def check(tag):
    tok = copy.copy(token)
    tok['tag'] = tag.hex
    r = uio.tcp('200.136.252.51', 5555)
    with r.timeout(5) as ti:
        res = r.line('2').after('Token: ').line(str(tok)).until('.InvalidTag')
        print(tag, res)
    r.close()
    if ti.safe:
        return None
    return tag


pool = mp.Pool(32)
for tag in pool.imap_unordered(check, range(256)):
    if tag is not None:
        token['tag'] = tag.hex
        pool.terminate()
        break

pool.terminate()
pool.join()
print('GO')
r = uio.tcp('200.136.252.51', 5555)
r.line('2').after('Token: ').line(str(token))
r.interact()
    
# print(token)

