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

import numpy  # noqa: F401
import lappy  # noqa: F401

import pytest
from warnings import warn

# part of the numpy api is not meant to be included.
NOSUP = [
        '__array_finalize__', '__array_prepare__',
        '__array_wrap__',
        '__getstate__', '__setstate__', '__array_priority__',
        '__array_struct__', '__long__', '__setmask__',
        '_baseclass', '_comparison', '_data', '_defaulthardmask',
        '_defaultmask', '_delegate_binop', '_get_data', '_get_flat',
        '_get_mask', '_get_recordmask', '_insert_masked_print', '_print_width',
        '_print_width_1d', '_set_flat', '_set_mask', '_set_recordmask',
        '_update_from',

        # build system
        '__config__', '__NUMPY_SETUP__', '_NoValue', 'MachAr', 'WRAP',
        'Tester', 'ModuleDeprecationWarning', '_add_newdoc_ufunc', '_arg',
        '_distributor_init', '_pytesttester'

        # not well-defined for lappy arrays, since there is no direct
        # correspondence with data in memory.
        'iscontiguous', 'byteswap', 'newbyteorder', 'getfield', 'setfield',
        'strides', 'tobytes', 'tofile', 'tolist', 'tostring', 'view',
        'ALLOW_THREADS', 'BUFSIZE', 'CLIP', 'ERR_CALL', 'ERR_DEFAULT',
        'ERR_IGNORE', 'ERR_LOG', 'ERR_PRINT', 'ERR_RAISE', 'ERR_WARN',
        'FLOATING_POINT_SUPPORT', 'FPE_DIVIDEBYZERO', 'FPE_INVALID',
        'FPE_OVERFLOW', 'FPE_UNDERFLOW', 'False_', 'True_', 'RAISE',
        'MAXDIMS', 'MAY_SHARE_BOUNDS', 'MAY_SHARE_EXACT',
        'Inf', 'Infinity', 'NAN', 'NINF', 'NZERO', 'NaN', 'PINF', 'PZERO',
        'SHIFT_DIVIDEBYZERO', 'SHIFT_INVALID', 'SHIFT_OVERFLOW', 'SHIFT_UNDERFLOW',
        'UFUNC_BUFSIZE_DEFAULT', 'UFUNC_PYVALS_NAME', '_UFUNC_API',

        # not planned to support
        'DataSource', '_globals',

        # (no masked array support for now)
        'compress', 'compressed', 'count', 'base', 'baseclass',
        'choose', 'ctypes', 'data', 'fill_value', 'filled',
        'get_fill_value', 'get_imag', 'get_real',
        'harden_mask', 'hardmask', 'ids', 'mini', 'mask', 'recordmask',
        'set_fill_value', 'sharedmask', 'shrink_mask', 'soften_mask',
        'toflex', 'torecords', 'unshare_mask',

        # (no matrixlib support for now)
        '_mat',

        # attributes set during construction
        'dtype', 'shape', 'flags', 'setflags',
        ]


def warn_diff(npi, lpi, name, assert_extra_hidden=False):
    missing = []
    extra = []

    for fn in npi:
        if fn not in lpi:
            missing.append(fn)

    missing = [m for m in missing if m not in NOSUP]

    for fn in lpi:
        if fn not in npi:
            extra.append(fn)

    if len(missing) > 0:
        warn("\n>>>> Missing API in %s (%d):\n %s"
                % (name, len(missing), ', '.join(missing)))
    if len(extra) > 0:
        warn("\n>>>> Extra API in %s (%d):\n %s"
                % (name, len(extra), ', '.join(extra)))

    if assert_extra_hidden:
        assert all(ext.startswith('_') for ext in extra)

    return len(missing) + len(extra)


@pytest.mark.parametrize('path_lappy, path_numpy, name, tol', [
    ('lappy', 'numpy', 'lappy', 1000),
    ('lappy.ndarray', 'numpy.ndarray, numpy.ma.MaskedArray', 'ndarray', 1000),
    ])
def test_public_interface(path_lappy, path_numpy, name, tol):
    lpi = []
    npi = []
    for pl in path_lappy.split(', '):
        exec('lpi += dir(%s)' % pl)
    for pn in path_numpy.split(', '):
        exec('npi += dir(%s)' % pn)

    lpi = sorted(list(set(lpi)))
    npi = sorted(list(set(npi)))

    distance = warn_diff(npi, lpi, name)
    assert distance < tol
