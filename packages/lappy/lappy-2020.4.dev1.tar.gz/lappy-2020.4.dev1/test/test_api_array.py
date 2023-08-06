from __future__ import division, absolute_import, print_function

__copyright__ = "Copyright (C) 2019 Xiaoyu Wei"

__license__ = """
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import numpy as np
from lappy.core import Array, to_lappy_array
import pytest


@pytest.mark.parametrize('nparr', [
    np.ones(10),
    np.zeros([2, 3, 4]),
    np.random.rand(1200).reshape([3, 4, 5, 5, 4]),
    np.array(range(10), dtype=np.int32),
    ])
def test_construction_from_numpy_array(nparr):
    arr = to_lappy_array(nparr)
    assert isinstance(arr, Array)
    assert arr._get_shape_vals_or_strs() == nparr.shape
    assert arr.dtype == nparr.dtype


@pytest.mark.parametrize('name,shape,dtype', [
    ('a', (1, 2, 3), np.float64),
    ('b', (5, 2, 'm'), np.float64),
    ('c', ('m', 'n', 'p'), np.int32),
    ('d', (1, 'm', 'n'), np.int32),
    ('e', (23, '2', 'n'), np.complex128),
    ])
def test_construction_abstract(name, shape, dtype):

    # convert integers to int
    normalized_shape = list(shape)
    for i, s in enumerate(normalized_shape):
        try:
            normalized_shape[i] = int(s)
        except ValueError:
            pass
    normalized_shape = tuple(normalized_shape)

    # all kwargs
    arr = Array(name=name, shape=shape, dtype=dtype)
    assert arr.name == name
    assert arr.ndim == len(shape)
    assert arr._get_shape_vals_or_strs() == normalized_shape
    assert arr.dtype == dtype

    # name and shape are positional args
    arr = Array(name, shape, dtype=dtype)
    assert arr.name == name
    assert arr.ndim == len(shape)
    assert arr._get_shape_vals_or_strs() == normalized_shape
    assert arr.dtype == dtype

    # shape given by a string
    shape_str = ', '.join(str(s) for s in shape)
    arr = Array(name, shape_str, dtype=dtype)
    assert arr.name == name
    assert arr.ndim == len(shape)
    assert arr._get_shape_vals_or_strs() == normalized_shape
    assert arr.dtype == dtype
