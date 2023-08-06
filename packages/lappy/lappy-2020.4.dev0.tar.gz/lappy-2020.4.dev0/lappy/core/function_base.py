from __future__ import division, absolute_import, print_function

import numpy as np
from lappy import ndarray
from lappy.core.array import (
        default_env,
        LazyObjectBase, Scalar, Unsigned,
        to_lappy_scalar, to_lappy_unsigned)
from lappy.core.ufuncs import power
from lappy.core.tools import (check_and_merge_envs, check_and_merge_precs)

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

__all__ = ["arange", "linspace", "logspace"]


def arange(start, stop=None, step=1, dtype=None,
           name=None, base_env=None):
    """Return evenly spaced values within a given interval.
    Behaves like :func:`numpy.arange`.

        ```
        numpy.arange([start, ]stop, [step, ]dtype=None)
        ```

    :param start: Start of interval. The interval includes this value.
        The default start value is 0.
    :param stop: End of interval. The interval does not include this value,
    :param step: Spacing between values. The default step size is 1.
    :param dtype: The type of the output array.

    :param name: Name of the output.
    """
    if stop is None:  # the pos 1 arg is treated as stop
        stop = start
        start = 0

    if base_env is None:
        base_env = default_env()

    start = to_lappy_scalar(start)
    stop = to_lappy_scalar(stop)
    step = to_lappy_scalar(step)

    num = to_lappy_unsigned((stop - start) // step)

    obj = dict()
    obj['ndim'] = 1
    obj['shape'] = (num.name, )
    obj['env'] = check_and_merge_envs(start, stop, step)
    obj['namespace'] = {num.name: (num, dict())}
    obj['preconditions'] = check_and_merge_precs(start, stop, step)

    if name is not None:
        obj['name'] = name

    if dtype is None:
        dtype = np.result_type(start, stop, step).type
    obj['dtype'] = dtype

    arr = ndarray(**obj)
    arr.namespace[arr.name][1]['is_argument'] = False

    iname = arr.inames[0]
    arr.expr = start.expr + step.expr * iname

    arr._meld_namespace(start.namespace, start.as_stateless())
    arr._meld_namespace(stop.namespace, stop.as_stateless())
    arr._meld_namespace(step.namespace, step.as_stateless())

    return arr


def linspace(start, stop, num=50, endpoint=True, retstep=False,
             name=None, dtype=None):
    """Return evenly spaced numbers over a specified interval.
    Behaves like :func:`numpy.linspace`.

    :param start: The starting (Scalar) value.
    :param stop: The end (Scalar) value.
    :param num: Number of samples to generate. Default is 50.
    :param endpoint: Whether the last point at ``stop`` is included.
    :param retstep: If True, return the spacing as well.

    :param name: Name of the output. Auto-generate the name if None.
    :param dtype: Data type of the output.
    """
    if isinstance(endpoint, LazyObjectBase):
        raise TypeError("boolean value 'endpoint' cannot be lazy.")
    if isinstance(retstep, LazyObjectBase):
        raise TypeError("boolean value 'retstep' cannot be lazy.")
    if not isinstance(start, Scalar):
        start = to_lappy_scalar(start)
    if not isinstance(stop, Scalar):
        stop = to_lappy_scalar(stop)
    if not isinstance(num, Unsigned):
        num = to_lappy_unsigned(num)

    if endpoint:
        if num == 1:
            step = 0.
        else:
            step = (stop - start) / (num - 1)
        y = arange(0, num) * step + start
        # FIXME: add this line when support indexing
        # y[-1] = stop
    else:
        step = (stop - start) / num
        y = arange(0, num) * step + start

    if retstep:
        return y, step
    else:
        return y


def logspace(start, stop, num=50, endpoint=True, base=10.0):
    """Return numbers spaced evenly on a log scale.
    Behaves like :func:`numpy.logspace`.

    :param start: The starting (Scalar) value.
    :param stop: The end (Scalar) value.
    :param num: Number of samples to generate. Default is 50.
    :param endpoint: Whether the last point at ``stop`` is included.
    :param base: The base of the log space. Default is 10.0.
    """
    y = linspace(start, stop, num=num, endpoint=endpoint)
    return power(base, y)
