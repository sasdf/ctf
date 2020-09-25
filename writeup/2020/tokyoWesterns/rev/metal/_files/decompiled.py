import random
import numpy as np


def encrypt(inp_key_t6, inp_data_t8):
    data_v34 = func_getDataMatrix(inp_data_t8, thread_y)

    assert inp_key_t6.dtype == np.uint64
    mat_org_v58 = inp_key_t6[thread_y * 64:][:64].astype(np.double).reshape(8, 8)
    mat_org_v58 *= 2.0**(-64)

    # set m[i,j] = m[j,i] or m[j,i] = m[i,j] according to tsc
    mat_org_v58 = maybe_to_random_symmetric(mat_org_v58)

    out_v66 = np.eye(8, dtype=np.double) # diagonal_mat8x8

    mat = mat_org_v58.copy()
    for _ in range(0x800):
        mc, mr = func_upper_tri_abs_argmax(mat)

        if too_small_cf_diag(mat, mr, mc):
            mat[mr,mc] = 0

        c3, c1, c2 = func_get_wtf_coeffs(mat, mr, mc)
        mat = func_mix_matrix(mat, mr, mc, c1, c2, c3)
        out_v66 = func_mix_row(out_v66, mr, mc, c1, c2)
    # print(out_v66)
    # print(mat)

    # get diagonal array, first 8 elements
    diag_elems_v87 = np.zeros(64)
    diag_elems_v87[:8] = np.diag(mat)[:8]

    # latter 8 * 7 = 56 elements
    for r in range(8):
        mat = remove_col_and_row(mat_org_v58, r)

        for _ in range(0x800):
            mc, mr = func_upper_tri_abs_argmax(mat)

            if too_small_cf_diag(mat, mr, mc):
                mat[mr,mc] = 0

            c3, c1, c2 = func_get_wtf_coeffs(mat, mr, mc)
            mat = func_mix_matrix(mat, mr, mc, c1, c2, c3)

        diag_elems_v87[r * 7 + 8:][:7] = np.diag(mat)[:7]

    out_v66 = data_v34 * np.abs(out_v66)

    return diag_elems_v87.tobytes() + out_v66.tobytes()


# _Z13getDataMatrixIdEv15cm_surfaceindexiu2CMmr8x8_T__BB_1_2_1
def func_getDataMatrix(inp_data_t8, thread_y):
    assert inp_data_t8.dtype == np.uint8
    return inp_data_t8[thread_y * 64:][:64].astype(np.double).reshape(8, 8)


# _Z16JPYgRtzJnMjnpuDbIdEvu2CMmr8x8_T_RiS2__BB_16_17_16:
def _func_upper_tri_abs_argmax(mat):
    """get position of max element in upper triangular matrix"""
    max_row = 0
    max_col = func_upper_tri_abs_argmax_row(mat, 0)
    M = np.abs(mat[0,max_col])
    for y in range(1, 7):
        e = np.abs(mat[y,func_upper_tri_abs_argmax_row(mat, y)])
        if e > M:
            max_col = func_upper_tri_abs_argmax_row(mat, y)
            max_row = y
            M = e
    return max_col, max_row


def func_upper_tri_abs_argmax(mat):
    """get position of max element in upper triangular matrix"""
    m = np.triu(np.abs(mat), 1)
    if (m == 0.0).all():
        return 0, 1
    i = m.reshape(-1).argmax()
    return i % 8, i // 8


# _Z16kpxrVWpHldSWgSHyIdEvu2CMmr8x8_T_ii_BB_18_19_18
def func_get_wtf_coeffs(mat, mr, mc):
    diff = mat[mc,mc] - mat[mr,mr]

    if diff != 0:
        c3 = np.double(0.0)
        M = mat[mr,mc]
        if M != 0:
            M2 = M * 2.0
            v181 = diff / M2
            v185 = v181 * v181 + 1.0
            v185 = np.sqrt(v185)
            v186 = np.abs(v181)
            c3 = 1.0/(v185 + v186)
            if v181 < 0:
                c3 = -c3
    else:
        c3 = np.double(1.0)

    v187 = c3 * c3 + 1.0
    v187 = np.sqrt(v187)
    c1 = 1.0/v187

    c2 = c3 * c1

    return c3, c1, c2
    # export d, c1, c2


# _Z16MlHoUTcdUynRDLWqIdEvu2CMmr8x8_T_ii_BB_19_20_19
def func_mix_matrix(mat, r, c, c1, c2, c3):
    """
             r     c
       \  .  |  .  ^  .  .  .  
       .  \  |  .  ^  .  .  .  
     r =  =  *  =  E  =  =  =  
       .  .  |  \  ^  .  .  .  
     c -  -  +  -  *  -  -  -  
       .  .  |  .  ^  \  .  .  
       .  .  |  .  ^  .  \  .  
       .  .  |  .  ^  .  .  \  
    """

    # modify * and 0
    mat[r,r] -= mat[r,c] * c3
    mat[c,c] += mat[r,c] * c3
    mat[r,c] = 0

    """
             r     c
       \  .  |  .  ^  .  .  .  
       .  \  |  .  ^  .  .  .  
     r =  =  *  =  0  =  =  =  
       .  .  |  \  ^  .  .  .  
     c -  -  +  -  *  -  -  -  
       .  .  |  .  ^  \  .  .  
       .  .  |  .  ^  .  \  .  
       .  .  |  .  ^  .  .  \  
    """

    for i in range(r):
        mat[r,i] = mat[i,r] # modify lower
        mat[i,r] = mat[i,r] * c1 - mat[i,c] * c2 # modify upper i

    for i in range(r+1, c):
        mat[i,r] = mat[r,i] # modify lower
        mat[r,i] = mat[r,i] * c1 - mat[i,c] * c2 # modify upper r

    for i in range(c+1, 8):
        mat[i,r] = mat[r,i] # modify lower
        mat[r,i] = mat[r,i] * c1 - mat[c,i] * c2 # modify upper r
    
    """
             r     c
       \  .  xa .  a  .  .  .  
       .  \  xa .  a  .  .  .  
     r x  x  *  yb 0  zc zc zc 
       .  .  y  \  b  .  .  .  
     c -  -  +  -  *  c  c  c  
       .  .  z  .  ^  \  .  .  
       .  .  z  .  ^  .  \  .  
       .  .  z  .  ^  .  .  \  
    """


    for i in range(r):
        mat[i,c] = mat[i,c] * c1 + mat[r,i] * c2 # modify upper i

    for i in range(r+1, c):
        mat[i,c] = mat[i,c] * c1 + mat[i,r] * c2 # modify upper i

    for i in range(c+1, 8):
        mat[c,i] = mat[c,i] * c1 + mat[i,r] * c2 # modify upper c

    """
             r     c
       \  .  xa .  ax .  .  .  
       .  \  xa .  ax .  .  .  
     r x  x  *  yb 0  zc zc zc 
       .  .  y  \  by .  .  .  
     c -  -  +  -  *  cz cz cz 
       .  .  z  .  ^  \  .  .  
       .  .  z  .  ^  .  \  .  
       .  .  z  .  ^  .  .  \  
    """

    return mat


# _Z16cdnzEgsXDUQhMTJHIdEvu2CMmr8x8_T_ii_BB_20_21_20
def func_mix_row(out_v66, mc, mr, a, b):
    """
             r     c
       1  .  .  .  .  .  .  .  
       .  1  .  .  .  .  .  .  
     r .  .  a  .  b  .  .  .  
       .  .  .  1  .  .  .  .  
     c .  . -b  .  a  .  .  .  
       .  .  .  .  .  1  .  .  
       .  .  .  .  .  .  1  .  
       .  .  .  .  .  .  .  1  
    """
    bak = out_v66[mc,:].copy()
    out_v66[mc,:] = out_v66[mc,:] * a - out_v66[mr,:] * b
    out_v66[mr,:] = out_v66[mr,:] * a +           bak * b

    return out_v66


# _Z16aAqwvgDTmHcpllEMIdEiu2CMmr8x8_T_i_BB_14_15_14:
def func_upper_tri_abs_argmax_row(mat, y):
    ret = y + 1
    for i in range(y + 2, 8):
        if np.abs(mat[y,i]) > np.abs(mat[y,ret]):
            ret = i
    return ret


def remove_col_and_row(mat, r):
    """remove v[:,r] and v[r,:] other cols/rows shift to topleft corner
    example:
        a a | b      a a b 0
        a a | b  ==> a a b 0
        - - + -      c c d 0
        c c | d      0 0 0 0
    """
    ret = np.zeros_like(mat)
    ret[:r,:r] = mat[:r,:r]
    ret[r:-1,:r] = mat[r+1:,:r]
    ret[:r,r:-1] = mat[:r,r+1:]
    ret[r:-1,r:-1] = mat[r+1:,r+1:]
    return ret
    

def too_small_cf_diag(m, r, c):
    """whether adding m[r,c] to m[r,r] and m[c,c] won't change its value"""
    return m[r,c] + m[r,r] == m[r,r] and m[r,c] + m[c,c] == m[c,c]


def maybe_to_random_symmetric(mat):
    """set m[i,j] = m[j,i] or m[i,j] = m[j,i] according to tsc"""
    for i in range(1, 8):
        for j in range(0, i):
            if random.getrandbits(1):
                mat[j,i] = mat[i,j]
            else:
                mat[i,j] = mat[j,i]
    return mat


#################################
### Testing decompiled result ###
#################################

def _test():
    """Run encrypt with random data"""
    global thread_y
    thread_y = 0
    seed = 43
    random.seed(seed)
    np.random.seed(seed)
    np.set_printoptions(edgeitems=16, precision=3, linewidth=140, suppress=True, floatmode='fixed')

    key = np.frombuffer(np.random.bytes(64*8), dtype=np.uint64)
    data = np.frombuffer(np.random.bytes(64), dtype=np.uint8)

    ret = encrypt(key, data)

    ret = np.frombuffer(ret, dtype=np.double).reshape(2, 8, 8)
    print(ret[0, 0])
    print(ret[0, 1:].reshape(8, 7))
    print(ret[1])

    diag_elems_v87, enc = ret
    
    LA = diag_elems_v87[0]
    LM = diag_elems_v87[1:].reshape(8, 7)

    V = np.zeros_like(enc)
    for i in range(8):
        for j in range(8):
            lhs = np.prod(LA[i] - np.concatenate([LA[:i], LA[i+1:]]))
            rhs = np.prod(LA[i] - LM[j])
            V[i,j] = rhs / lhs
    V = np.sqrt(np.abs(V))

    dec = ret[1] / V
    print(dec - data.reshape(8, 8))


    
if __name__ == '__main__':
    _test()
