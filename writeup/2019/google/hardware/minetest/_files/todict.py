import sqlite3
import zlib
from struct import unpack
from collections import Counter, defaultdict
from tqdm import tqdm
import pickle


conn = sqlite3.connect('map.sqlite')
cur = conn.cursor()
cur.execute('SELECT pos, data FROM blocks WHERE instr(data, "mesecons") > 0;')

"""
insulated @ 0: ---
                 .
cross_over @ 0: ---
                 '
corner @ 0: --.
              |
gate @ 0: =>-

tjunction @ 0: T

clock-wise rotate
"""


def unsignedToSigned(i, max_positive):
    if i < max_positive:
        return i
    else:
        return i - 2*max_positive


def getIntegerAsBlock(i):
    x = unsignedToSigned(i % 4096, 2048)
    i = int((i - x) / 4096)
    y = unsignedToSigned(i % 4096, 2048)
    i = int((i - y) / 4096)
    z = unsignedToSigned(i % 4096, 2048)
    return x * 16, y * 16, z * 16


def readu8(data):
    ret, data = data[0], data[1:]
    return ret, data


def readu16(data):
    ret, data = unpack('>H', data[:2])[0], data[2:]
    return ret, data


def readu32(data):
    ret, data = unpack('>I', data[:4])[0], data[4:]
    return ret, data


def reads32(data):
    ret, data = unpack('>i', data[:4])[0], data[4:]
    return ret, data


def readbytes(data, n):
    assert len(data) >= n
    ret, data = data[:n], data[n:]
    return ret, data


def readzlib(data):
    decobj = zlib.decompressobj()
    ret = decobj.decompress(data)
    assert decobj.unconsumed_tail == b''
    return ret, decobj.unused_data


def chunk(arr, n):
    return [arr[i:i+n] for i in range(0, len(arr), n)]


blocks = {}

names = Counter()
print(cur.rowcount)
bar = tqdm(cur.fetchall(), total=6316)
try:
    for pos, data in bar:
        pos = getIntegerAsBlock(pos)
        version, data = readu8(data)
        flags, data = readu8(data)
        lighting, data = readu16(data)
        content_width, data = readu8(data)
        params_width, data = readu8(data)
        content, data = readzlib(data)
        if content_width == 1:
            param0 = list(content[:4096])
            param1 = list(content[4096:8192])
            param2 = list(content[8192:12288])
        else:
            param0 = list(unpack('>4096H', content[:8192]))
            param1 = list(content[8192:12288])
            param2 = list(content[12288:16384])

        params = list(zip(param0, param1, param2))
        params = chunk(chunk(params, 16), 16)
        
        metadata, data = readzlib(data)

        static_obj_ver, data = readu8(data)
        assert static_obj_ver == 0

        static_obj_count, data = readu16(data)
        static_obj = []
        for i in range(static_obj_count):
            sobj_type, data = readu8(data)
            sobj_pos_x, data = reads32(data)
            sobj_pos_y, data = reads32(data)
            sobj_pos_z, data = reads32(data)
            sobj_data_sz, data = readu16(data)
            sobj_data, data = readbytes(data, sobj_data_sz)
            static_obj.append((sobj_type, sobj_pos_x, sobj_pos_y, sobj_pos_z, sobj_data))
        assert static_obj_count == 0

        ts, data = readu32(data)

        name2id_ver, data = readu8(data)
        assert name2id_ver == 0

        name2id_count, data = readu16(data)
        name2id = {}
        for i in range(name2id_count):
            n2id_id, data = readu16(data)
            n2id_nsz, data = readu16(data)
            n2id_name, data = readbytes(data, n2id_nsz)
            name2id[n2id_id] = n2id_name.decode()
        names.update(name2id.values())

        assert data == b'\n\0\0'

        meta_ver, metadata = readu8(metadata)
        meta = {}
        if meta_ver > 0:
            # print(pos, version, flags, lighting, static_obj_count, static_obj, ts, name2id, data)
            meta_sz, metadata = readu16(metadata)
            for _ in range(meta_sz):
                meta_record = {}
                meta_pos, metadata = readu16(metadata)
                meta_pos = (meta_pos & 0xf, (meta_pos >> 4) & 0xf, (meta_pos >> 8) & 0xf)
                meta_nvars, metadata = readu32(metadata)
                for _ in range(meta_nvars):
                    meta_klen, metadata = readu16(metadata)
                    meta_key, metadata = readbytes(metadata, meta_klen)
                    meta_vlen, metadata = readu32(metadata)
                    meta_val, metadata = readbytes(metadata, meta_vlen)
                    meta_sep, metadata = readu8(metadata)
                    assert meta_sep == 0
                    meta_record[meta_key.decode()] = meta_val.decode()
                meta_inventory, metadata = metadata.split(b'EndInventory\n', 1)
                assert meta_pos not in meta
                assert meta_inventory == b''
                meta[meta_pos] = meta_record
        else:
            assert metadata == b''

        for z, zs in enumerate(params):
            for y, ys in enumerate(zs):
                for x, (p0, p1, p2) in enumerate(ys):
                    name = name2id[p0]
                    if name == 'ignore' or name == 'air' or name == 'default:stone':
                        continue
                    p = (pos[0] + x, pos[1] + y, pos[2] + z)
                    # blocks[p] = (name, p1, p2, meta.get((x, y, z), {}))
                    blocks[p] = (name, p2)

finally:
    bar.close()

with open('blocks.pkl', 'wb') as f:
    pickle.dump(blocks, f)
