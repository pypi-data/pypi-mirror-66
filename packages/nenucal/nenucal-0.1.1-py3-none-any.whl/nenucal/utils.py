# Mixed utilities
#
# Author: F. Mertens

import numpy as np


def chunks(arr, n_max):
    n = int(np.ceil(len(arr) / np.ceil(len(arr) / n_max)))
    for i in range(0, len(arr), n):
        yield arr[i:i + n]


def factors(n):
    r = np.arange(1, int(n ** 0.5) + 1)
    x = r[np.mod(n, r) == 0]
    return np.unique(np.concatenate((x, n / x), axis=None))


def slice_dim_idx(a, axis, s):
    idx = [slice(None) for k in range(a.ndim)]
    idx[axis] = s
    return tuple(idx)


def slice_dim(a, axis, s):
    return a[slice_dim_idx(a, axis, s)]


def mean_consecutive(a, n=2, axis=0, return_n=False):
    if isinstance(a, np.ma.MaskedArray):
        a_sum = np.add.reduceat(a.filled(0), np.arange(0, a.shape[axis], n), axis=axis)
        a_n_sum = np.add.reduceat((~a.mask).astype(int), np.arange(0, a.shape[axis], n), axis=axis)
        if return_n:
            return np.ma.array(a_sum / a_n_sum, mask=(a_n_sum == 0)), a_n_sum
        return np.ma.array(a_sum / a_n_sum, mask=(a_n_sum == 0))
    a_sum = np.add.reduceat(a, np.arange(0, a.shape[axis], n), axis=axis)
    return a_sum / float(n)


def diff_consecutive(a, axis=0):
    d = slice_dim(np.diff(a, axis=axis), axis, slice(None, None, 2))
    if isinstance(d, np.ma.MaskedArray) and d.mask.ndim == 0:
        d.mask = np.zeros_like(d)

    return d
