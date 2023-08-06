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
from lappy.core.array import LazyObjectBase, Scalar

__all__ = ["check_and_merge_envs", "check_and_merge_precs",
           "is_nonnegative_int", "is_constexpr", 'ScalarType']


ScalarType = np.ScalarType + (Scalar, )


def check_and_merge_envs(*arr_list):
    """Merge captured environments.

    Enviroments (captured lists) are dictionaries with names as keys, and
    data (numpy arrays, pyopencl arrays etc.) as values.

    Raises exception when there are conflicts.
    """
    new_env = dict()
    for arr in arr_list:
        for key, val in arr.env.items():
            if key in new_env:
                if new_env[key] is val:
                    pass
                elif val is None:
                    pass
                elif new_env[key] is None:
                    new_env[key] = val
                else:
                    raise ValueError(
                            "Trying to merge environments with conflicting "
                            "definitions of %s" % key)
            else:
                new_env[key] = val
    return new_env


def check_and_merge_precs(*arr_list):
    """Merge precondition lists.

    PLs are lists of :class:`EvaluationPrecondition` objects.

    Returns the merged argument list.
    """
    mprecs = list()
    for arr in arr_list:
        mprecs.extend(arr.preconditions)

    return mprecs


def is_nonnegative_int(num):
    if not np.isscalar(num):
        return False

    try:
        nn = int(num)
    except ValueError:
        return False

    return abs(nn) - num == 0


def is_constexpr(a):
    """Check if the input value is non-lazy (has known values at codegen)
    """
    if isinstance(a, LazyObjectBase):
        # a lazy obj is constexpr only if it has known value
        return (a.value is not None)

    if isinstance(a, (list, tuple)):
        return all(is_constexpr(ele for ele in a))

    if isinstance(a, dict):
        return all(is_constexpr(ele for ele in a.values()))

    return True
