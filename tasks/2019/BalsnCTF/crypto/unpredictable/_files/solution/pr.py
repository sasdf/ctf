from scipy import stats
import numpy as np
import itertools


def getprob(N, p=0.5, eps=1e-10):
    eps = eps / 2
    left, right = stats.gamma.ppf([eps, 1-eps], N, scale=p)
    x = np.arange(int(left), int(right))
    y = stats.gamma.pdf(x, N, scale=p)
    return x.tolist(), y


def getindices(p=0.5, eps=1e-8):
    x1, y1 = getprob(397, p=p)
    x2, y2 = getprob(624, p=p)
    x = list(itertools.product(range(len(x1)), range(len(x2))))
    y = np.array([y1[a] * y2[b] for a, b in x])
    i = y.argsort()[::-1]
    x = [(x1[x[ii][0]], x2[x[ii][1]]) for ii in i]
    y = y[i]
    s = np.cumsum(y)
    end = np.where(s > (1 - eps))[0]
    if len(end) > 0:
        end = end[0]
    else:
        end = len(x)
    return x[:end]
