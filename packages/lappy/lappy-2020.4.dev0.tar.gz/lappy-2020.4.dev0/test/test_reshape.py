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
import pyopencl as cl
import lappy as la
import numpy as np

from pyopencl.tools import (  # noqa
        pytest_generate_tests_for_pyopencl as pytest_generate_tests)


@pytest.mark.parametrize('in_shape,out_shape', [
    ((12, ), (2, 3, 2)),
    ((1024, ), (2, 4, 8, 16)),
    ((1024, ), (2, 4, 8, -1)),
    ((2, 3), 6),
    ((2, 3, 4), 24),
    ((3, 2, 1, 4), 24),
    ((1213, ), -1),
    ((1, 6, 255), -1),
    ((3, 2, 1, 4), -1),
    ((3, 2, 1, 4), (-1, )),
    ((2, 3), (3, 2)),
    ((2, 3, 4), (2, 12)),
    ((1, 2, 3, 4), (2, 1, 2, 2, 3)),
    ((1, 2, 3, 4), (2, 1, -1, 2, 3)),
    ((1, 3, 2, 3, 4), (6, 12)),
    ])
@pytest.mark.parametrize('order', ['C', 'F'])
def test_reshape(ctx_factory, in_shape, out_shape, order, dtype=np.float64):
    cl_ctx = ctx_factory()
    queue = cl.CommandQueue(cl_ctx)
    ndim = len(in_shape)

    A = la.ndarray('A', ndim=ndim)  # noqa: N806
    B = A.reshape(out_shape, order=order, name='B')  # noqa: N806

    data = np.random.rand(*in_shape).astype(dtype)

    C = B.with_data(A=data).with_name('C')  # noqa: N806

    lappy_val = C.eval(queue)
    numpy_val = data.reshape(out_shape, order=order)

    assert np.allclose(lappy_val, numpy_val)
