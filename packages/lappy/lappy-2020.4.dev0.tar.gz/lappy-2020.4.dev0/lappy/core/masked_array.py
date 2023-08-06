from __future__ import division, absolute_import, print_function

from lappy.core.array import Array

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

__doc__ = """
=============
Masked Arrays
=============
"""


class MaskedArrayError(Exception):
    pass


class MaskError(MaskedArrayError):
    pass


class MaskedArray(Array):
    """An array class with possibly masked values.
    The mask array is an array of booleans that shares the shape and inames
    with the (base) data array, and lives in the same closure.

    For a masked array A, A.expr and A.value means the data array. To get the
    value of the final results, access A.masked_value instead.

    .. attribute:: mask_expr

        expression for the mask array

    .. attribute:: mask_value

        value for the mask array

    .. attribute:: masked_value

        value of the masked array (after post-processing)
    """
    _counter = 0
    _name_prefix = '__lappy_masked_array_'
    pass
