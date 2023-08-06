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

import pytest
import numpy as np
from pymbolic import evaluate
from lappy import ndarray
from lappy.core.broadcast import broadcast
from lappy.eval import Compiler


@pytest.mark.parametrize('shapes', [
    ((12, 12), (12, 1)),
    ((12, 12), (1, 12)),
    ((12, 12), (1, 1)),
    ((12, 12), tuple()),
    ((12, 23, 1, 33), (12, 1, 81, 33)),
    ((12, 23, 1, 33), (33, )),
    ((12, 23, 1, 33), (23, 33)),
    ((12, 23, 1, 33), (23, 33), (33, ), tuple(), (1, 1, 23, 1)),
    ])
def test_broadcast_rules(shapes):

    nparrs = [np.zeros(s) for s in shapes]
    numpy_res = np.broadcast(*nparrs)

    laarrs = [ndarray(shape=s) for s in shapes]
    lappy_res = broadcast(*laarrs)

    assert numpy_res.ndim == lappy_res.ndim
    assert numpy_res.shape == lappy_res.shape_val_or_str
    assert numpy_res.size == lappy_res.size


@pytest.mark.parametrize('shapes', [
    ((12, 12), (12, 1)),
    ((12, 12), (1, 12)),
    ((12, 12), (1, 1)),
    ((12, 12), tuple()),
    ((12, 23, 1, 33), (12, 1, 81, 33)),
    ((12, 23, 1, 33), (33, )),
    ((12, 23, 1, 33), (23, 33)),
    ((12, 23, 1, 33), (23, 33), (33, ), tuple(), (1, 1, 23, 1)),
    ])
def test_symbolic_broadcast_rules(shapes):

    # lappy only knows ndims when doing broadcast
    ndims = [len(shape) for shape in shapes]

    nparrs = [np.zeros(s) for s in shapes]
    numpy_res = np.broadcast(*nparrs)

    laarrs = [ndarray(ndim=nd) for nd in ndims]
    lappy_res = broadcast(*laarrs)

    assert numpy_res.ndim == lappy_res.ndim

    # inform lappy with actual shapes to evaluate exprs
    for i in range(len(laarrs)):
        laarrs[i] = laarrs[i].with_shape_data(shapes[i])

    compiler = Compiler()
    closures = [compiler(arr) for arr in laarrs]
    arr_contexts = [clos.data_map for clos in closures]
    broadcast_ctx = {}
    for ctx in arr_contexts:
        broadcast_ctx.update(ctx)

    for arr in laarrs:
        print(arr.env)

    # shape and size are now expressions
    # evaluate those concretely with a sum
    for lar in laarrs:
        broadcast_ctx.update(lar.env)

    # check shape
    lappy_res_shape = [
            evaluate(lappy_res._shape_exprs[i], broadcast_ctx)
            for i in range(lappy_res.ndim)]
    assert tuple(lappy_res_shape) == numpy_res.shape

    # check size
    lappy_res_size = evaluate(lappy_res.size, broadcast_ctx)
    assert lappy_res_size == numpy_res.size
