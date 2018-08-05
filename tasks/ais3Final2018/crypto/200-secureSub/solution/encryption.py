import io
import uu


def uuencode(data):
    data = data + b'\0' * (-len(data) % 3)
    inp = io.BytesIO(data)
    out = io.BytesIO()
    uu.encode(inp, out)
    return out.getvalue()


def uudecode(data):
    inp = io.BytesIO(data)
    dec = io.BytesIO()
    uu.decode(inp, dec)
    dec = dec.getvalue()
    dec = dec[:-2] + dec[-2:].rstrip(b'\0')
    return dec


def encrypt(data, mapping):
    encoded = uuencode(data)
    encoded = encoded.split(b'\n')
    head, data, tail = encoded[:1], encoded[1: -3], encoded[-3:]
    data = [line[:1] + bytes(mapping[c - 32] for c in line[1:]) for line in data]
    encrypted = b'\n'.join(head + data + tail)
    encrypted = uudecode(encrypted)
    return encrypted
