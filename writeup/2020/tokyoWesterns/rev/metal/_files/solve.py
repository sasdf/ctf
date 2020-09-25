import numpy as np

with open('flag.enc', 'rb') as f:
    data = f.read()

data = np.frombuffer(data, dtype=np.double).reshape(-1, 2, 8, 8)

flag = b''
for diag, enc in data:
    LA = diag[0]
    LM = diag[1:].reshape(8, 7)

    V = np.zeros_like(enc)
    for i in range(8):
        for j in range(8):
            lhs = np.sum(np.log(np.abs(LA[i] - np.concatenate([LA[:i], LA[i+1:]]))))
            rhs = np.sum(np.log(np.abs(LA[i] - LM[j])))
            V[i,j] = np.exp((rhs - lhs) / 2)

    dec = enc / V
    flag += np.round(dec).astype(np.uint8).tobytes()

with open('flag.png', 'wb') as f:
    f.write(flag)

#TWCTF{Is_it_possible_to_get_the_eigenvectors_of_a_matrix_using_only_its_eigenvalues?}
