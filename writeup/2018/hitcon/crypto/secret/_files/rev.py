def PKCS7(data, size): pass
def KDF(key): pass
def S_layer(a, b): pass
S3 = []


def enc(key, iv, data):
    # Initialize
    data, size = data
    rounds = PKCS7(data, size)
    subkeys = KDF(key)

    # Split into chunks
    data = [data[i: i+16] for i in range(0, rounds, 16)]

    # Encrypt
    for i in range(0, rounds // 16):
        state = data[i]
        if i:
            state ^= data[i - 1]
        else:
            state ^= iv

        state ^= subkeys[0]

        for m in range(1, 11):
            state = [S3[s] for s in state]
            state[13], state[1], state[5], state[9] = state[1], state[5], state[
                9], state[13]
            state[10], state[2] = state[2], state[10]
            state[14], state[6] = state[6], state[14]
            state[7], state[3], state[15], state[11] = state[3], state[15], state[
                11], state[7]
            if m != 10:
                for ii in range(4):
                    col = [state[4 * ii + zz] for zz in range(4)]
                    A = S_layer(2, col[0])
                    B = S_layer(3, col[1])
                    state[4 * ii] = col[2] ^ B ^ A ^ col[3]
                    A = S_layer(2, col[1])
                    B = S_layer(3, col[2])
                    state[4 * ii + 1] = col[3] ^ B ^ A ^ col[0]
                    A = S_layer(2, col[2])
                    B = S_layer(3, col[3])
                    state[4 * ii + 2] = col[0] ^ B ^ A ^ col[1]
                    A = S_layer(2, col[3])
                    B = S_layer(3, col[0])
                    state[4 * ii + 3] = col[1] ^ B ^ A ^ col[2]
            state ^= subkeys[m]
        data[i] = state
