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

from pymbolic import var, substitute
from pymbolic.primitives import If
from lappy.core.array import Array, to_lappy_array
from lappy.core.tools import check_and_merge_precs, check_and_merge_envs


def conditional(cond, con, alt, name=None):
    """If-then-else conditional expression for arrays.

    :param cond: The condition.
    :param con: The consequent.
    :param alt: The alternative.
    :param name: (Optional) name of the resulting array.

    Behaves like the ternary operator ?: in C.
    """
    # if cond is simply a known boolean, simplify the result
    if isinstance(cond, (int, bool)):
        if cond:
            return con
        else:
            return alt

    if not isinstance(cond, Array):
        cond = to_lappy_array(cond)

    if not isinstance(con, Array):
        con = to_lappy_array(con)

    if not isinstance(alt, Array):
        alt = to_lappy_array(alt)

    # con and alt must have the same ndim
    assert con.ndim == alt.ndim

    # cond can be a scalar or of the same shape as con/alt
    if cond.ndim > 0:
        assert cond.ndim == con.ndim

    obj = dict()

    if con.domain_expr == alt.domain_expr:
        obj['domain_expr'] = con.domain_expr
    else:
        # TODO: check/add precondition that although the
        # expressions differ, the resulting domains are the same
        raise NotImplementedError()

    if con.dtype is None:
        if alt.dtype is None:
            new_dtype = None
        else:
            new_dtype = alt.dtype
    else:
        new_dtype = np.result_type(con.dtype, alt.dtype).type

    obj['dtype'] = new_dtype
    arr_class = Array

    obj['ndim'] = con.ndim

    if name is None:
        name = '__if_(%s)_then_(%s)_else_(%s)' % (
                cond.name, con.name, alt.name)

    obj['name'] = name
    obj['inames'] = tuple(
            var('__(%s)_inames_%d' % (name, d))
            for d in range(obj['ndim']))

    iname_maps = dict()
    for iaxis in range(obj['ndim']):
        iname_maps[con.inames[iaxis]] = obj['inames'][iaxis]
        iname_maps[alt.inames[iaxis]] = obj['inames'][iaxis]
        if cond.ndim > 0:
            iname_maps[cond.inames[iaxis]] = obj['inames'][iaxis]

    # replace old inames with the same (new) ones
    obj['expr'] = substitute(
            If(cond.expr, con.expr, alt.expr),
            iname_maps)

    # con and alt must have the same shape, cond can be of the same shape,
    # or be a scalar of shape (, ).
    if all(s1.name == s2.name for s1, s2 in zip(con.shape, alt.shape)):
        if cond.ndim > 0:
            if all(s0.name == s1.name
                   for s0, s1 in zip(cond.shape, con.shape)):
                obj['shape'] = cond.shape
            else:
                # TODO: check/add preconditions as needed
                raise NotImplementedError()
        else:
            obj['shape'] = con.shape
    else:
        # TODO: check/add preconditions as needed
        raise NotImplementedError()

    obj['env'] = check_and_merge_envs(cond, con, alt)
    obj['preconditions'] = check_and_merge_precs(cond, con, alt)
    obj['namespace'] = None

    obj['is_integral'] = con.is_integral & alt.is_integral

    if not obj['is_integral']:
        obj['integer_domain'] = None
    else:
        if con.integer_domain is None and alt.integer_domain is None:
            obj['integer_domain'] = None
        else:
            if con.integer_domain is None:
                obj['integer_domain'] = alt.integer_domain
            elif alt.integer_domain is None:
                obj['integer_domain'] = con.integer_domain
            else:
                obj['integer_domain'] = alt.integer_domain.union(
                        con.integer_domain)

    arr = arr_class(**obj)

    arr._meld_namespace(cond.namespace, cond.as_stateless())
    arr._meld_namespace(con.namespace, con.as_stateless())
    arr._meld_namespace(alt.namespace, alt.as_stateless())

    return arr
