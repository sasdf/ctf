def unshiftRight(x, shift):
    res = x
    for i in range(32):
        res = x ^ res >> shift
    return res


def unshiftLeft(x, shift, mask):
    res = x
    for i in range(32):
        res = x ^ (res << shift & mask)
    return res


def untamper(v):
    """ Reverses the tempering which is applied to outputs of MT19937 """

    v = unshiftRight(v, 18)
    v = unshiftLeft(v, 15, 0xefc60000)
    v = unshiftLeft(v, 7, 0x9d2c5680)
    v = unshiftRight(v, 11)
    return v


def tamper(v):
    v = v ^ (v >> 11)
    v = v ^ (v << 7) & 0x9d2c5680
    v = v ^ (v << 15) & 0xefc60000
    v = v ^ (v >> 18)
    return v & 0xffffffff
