from scipy.io import wavfile
import librosa
import numpy as np
import binascii
from IPython import embed

fs, data = wavfile.read('voices.wav')
data = data.astype(np.float) / 32768
spec = librosa.stft(data)
mag = 10 * np.log(np.abs(spec))[:, 170:-170]
A = (mag[660:710]).mean(0)
B = (mag[750:800]).mean(0)
C = (mag[850:900]).mean(0)
D = (mag[950:1000]).mean(0)

a = A < B
c = C < D

x = np.round(np.arange(26.4, len(A), 52.8)).astype(np.int)
a = a[x] * 1
c = c[x] * 1
print(c)
print(a)
flag = ''.join([str(e) for p in zip(c, a) for e in p])
flag = int(flag, 2)
flag = '%x' % flag
flag = binascii.a2b_hex(flag)
print(flag)

print(len(c))


"""
660:710
750:800
850:900
950:1000
"""
