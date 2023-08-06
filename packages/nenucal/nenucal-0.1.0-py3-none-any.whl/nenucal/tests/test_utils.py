import numpy as np

from nenucal import utils


def test_chunks():
    for i in range(50):
        l = np.arange(np.random.randint(1, 200))
        n_max = np.random.randint(1, 100)
        chunks = list(utils.chunks(l, n_max))
        print(len(l), n_max, len(chunks))
        assert len(chunks) >= np.floor(len(l) / n_max)
        assert len(chunks) <= np.ceil(len(l) / n_max)
        assert np.allclose(np.concatenate(chunks), l)


def test_slice_dim():
    l = np.random.randn(100, 20, 5)
    assert np.allclose(utils.slice_dim(l, 1, slice(1, 3)), l[:, 1:3])
    assert np.allclose(utils.slice_dim(l, 1, slice(1, None)), l[:, 1:])
    assert np.allclose(utils.slice_dim(l, 0, slice(None, 20)), l[:20, :])
    assert np.allclose(utils.slice_dim(l, 2, slice(None, -1)), l[:, :, :-1])
