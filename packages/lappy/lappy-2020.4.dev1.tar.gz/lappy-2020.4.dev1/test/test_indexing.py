from __future__ import division, absolute_import, print_function

__copyright__ = "Copyright (C) 2020 Xiaoyu Wei"

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

import lappy as la
import numpy as np
from lappy.core.basic_ops import SubArrayFactory


def test_subarr_out_ndim():
    arr = la.ndarray('A', ndim=2)
    subfac = SubArrayFactory(
            arr,
            (slice(None, None, None), [[0, 1], [1, 1]], np.newaxis))
    print(subfac.selectors)
    print(subfac.ndim)
    print(arr.inames)
    print(arr.shape)


def test_slice_completion():
    arr = la.ndarray('A', ndim=2)
    subfac = SubArrayFactory(arr)
    sl = subfac._complete_slice(slice(None, -10, -1), 0)
    assert sl.step == -1
