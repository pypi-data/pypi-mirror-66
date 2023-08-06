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
import lappy as la
import pyopencl as cl
import lappy.core.ufuncs as math

import pytest

from pyopencl.tools import (  # noqa
        pytest_generate_tests_for_pyopencl as pytest_generate_tests)


@pytest.mark.parametrize('ufunc,shapes,dtype', [
        ('sin', [(500, ), (10, ), (1, )], np.float64),
        ('cos', [(25, 100), (100, 20), ], np.float64),
        ('exp', [(2, 4, 8), (1, 2, 3), ], np.complex128),
        ])
def test_unary_ufunc(ctx_factory, ufunc, shapes, dtype):
    cl_ctx = ctx_factory()
    queue = cl.CommandQueue(cl_ctx)
    ndim = len(shapes[0])

    # symbolic code is reused for different shapes (same ndim)
    mat = la.ndarray('A', ndim=ndim, dtype=dtype)
    fmat = getattr(math, ufunc)(mat).with_name('B')

    for shape in shapes:
        # input data
        mat_data = np.random.rand(*shape).astype(dtype)
        bound_mat = fmat.with_data(A=mat_data).with_name('C')

        # eval
        lappy_res = bound_mat.eval(queue)
        numpy_res = getattr(np, ufunc)(mat_data)

        # compare with numpy
        assert np.allclose(numpy_res, lappy_res)


@pytest.mark.parametrize('ufunc,shapes,dtype', [
        ('add', [(500, ), (10, ), (1, )], np.float64),
        ('subtract', [(25, 100), (100, 20), ], np.float64),
        ('multiply', [(2, 4, 8), (1, 2, 3), ], np.complex128),
        ])
def test_binary_ufunc(ctx_factory, ufunc, shapes, dtype):
    cl_ctx = ctx_factory()
    queue = cl.CommandQueue(cl_ctx)
    ndim = len(shapes[0])

    sym_shape = tuple('s%d' % i for i in range(ndim))

    mat_a = la.ndarray('A', shape=sym_shape, dtype=dtype)
    mat_b = la.ndarray('B', shape=sym_shape, dtype=dtype)

    fmat = getattr(math, ufunc)(mat_a, mat_b).with_name('C')

    for shape in shapes:
        # input data
        mat_a_data = np.random.rand(*shape).astype(dtype)
        mat_b_data = np.random.rand(*shape).astype(dtype)

        bound_mat = fmat.with_data(
                A=mat_a_data,
                B=mat_b_data
                ).with_name('C')

        # eval
        lappy_res = bound_mat.eval(queue)
        numpy_res = getattr(np, ufunc)(mat_a_data, mat_b_data)

        # compare with numpy
        assert np.allclose(numpy_res, lappy_res)


@pytest.mark.parametrize('shapes', [
        ((256, 256, 3), (3, )),
        ((8, 1, 6, 1), (7, 1, 5)),
        ((7, 1, 5), (8, 7, 6, 5)),
        ((5, 4), (1, ), ),
        ((1, ), (5, 4), ),
        ((5, 4), (4, ), ),
        ((4, ), (5, 4), ),
        ])
@pytest.mark.parametrize('ufunc', ['add', 'subtract', 'multiply', 'divide'])
@pytest.mark.parametrize('dtype', [np.float64, ])
def test_binary_ufunc_with_broadcast(ctx_factory, ufunc, shapes, dtype):
    cl_ctx = ctx_factory()
    queue = cl.CommandQueue(cl_ctx)

    ndim_a = len(shapes[0])
    ndim_b = len(shapes[1])
    sym_shape_a = tuple('s_a_%d' % i for i in range(ndim_a))
    sym_shape_b = tuple('s_b_%d' % i for i in range(ndim_b))

    mat_a = la.ndarray('A', shape=sym_shape_a, dtype=dtype)
    mat_b = la.ndarray('B', shape=sym_shape_b, dtype=dtype)

    fmat = getattr(math, ufunc)(mat_a, mat_b).with_name('C')

    shape_a, shape_b = shapes
    mat_a_data = np.random.rand(*shape_a).astype(dtype)
    mat_b_data = np.random.rand(*shape_b).astype(dtype)

    bound_mat = fmat.with_data(
            A=mat_a_data,
            B=mat_b_data
            ).with_name('C')

    # eval
    lappy_res = bound_mat.eval(queue)
    numpy_res = getattr(np, ufunc)(mat_a_data, mat_b_data)

    # compare with numpy
    assert np.allclose(numpy_res, lappy_res)
