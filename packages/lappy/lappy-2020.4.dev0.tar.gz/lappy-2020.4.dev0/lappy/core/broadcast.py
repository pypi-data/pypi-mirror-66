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
from functools import partial
from pymbolic import evaluate, substitute, var
from pymbolic.primitives import Product, Expression, Max

from lappy.core.array import to_lappy_shape, to_lappy_array, make_default_name
from lappy.core.tools import is_nonnegative_int
from lappy.core.preconditions import EvaluationPrecondition


class BroadcastResult(object):
    """Encapsulates the broadcasting result.
    The object acts like an array when performing shape-related queries.

    .. attribute:: name

        name of the broadcast, used to name the resulting arrays.

    .. attribute:: base_arrays

        list of (lazy) arrays, whose api should support .shape and .ndim
        queries.

    .. attribute:: broadcast_arrays

        arrays that are broadcast. If an array is unchanged, an exact copy
        is made; otherwise a new array is created from it.

    .. attribute:: ndim

        ndim of the broadcast result

    .. attribute:: shape

        shape of the broadcast result. Unlike Array.shape which is a tuple of
        :class:`Unsigned`, it is simply a tuple of integers or strings of names,
        since broadcasting tracks only the name mappings, not the detailed
        expressions therein.

    .. attribute:: size

        size (number of elements) of the broadcast result

    .. attribute:: inames

        all broadcast results share the same set of inames

    .. attribute:: preconditions

        list of extra preconditions to make the broadcast feasible

    NOTE: only fixed (statically known) ndims are supported
    """
    _counter = 0
    _name_prefix = '__lappy_broadcast_res_'

    def __init__(self, array_list):
        self.base_arrays = array_list
        self.preconditions = []

        self.name = self._make_broadcast_name()
        self._broadcase_base_arrays()
        self.inames = self._make_broadcast_inames()

        self._make_broadcast_arrays()

    def _has_trivial_domain_expr(self):
        return all([arr._has_trivial_domain_expr() for arr in self.base_arrays])

    def _make_broadcast_name(self):
        return make_default_name(self.__class__)

    def _make_broadcast_inames(self):
        if self.ndim == 0:
            return ()
        assert self.ndim > 0
        return tuple(var('__%s_inames_%d' % (self.name, d))
                     for d in range(self.ndim))

    def _broadcase_base_arrays(self):
        """Compute the ndim, shape and size of the broadcast result.
        """
        ndims = [arr.ndim for arr in self.base_arrays]
        self.ndim = max(ndims)

        # values when available, names otherwise
        shapes = [arr._get_shape_vals_or_strs() for arr in self.base_arrays]

        # gather shape expressions
        expr_map = {}
        for arr in self.base_arrays:
            for s in arr.shape:
                if s not in expr_map:
                    expr_map[var(s)] = arr._extract(s).expr
                else:
                    # same name must have the same runtime values
                    # (may have different expressions)
                    def check_name_value_consistency(context, s):
                        s_val = evaluate(s.expr, context)
                        another_s_val = evaluate(
                            expr_map[var(s.name)], context)
                        return s_val == another_s_val
                    self.preconditions.append(EvaluationPrecondition(
                        partial(check_name_value_consistency, s=s)))

        # implicitly reshape to the same ndim
        # (right-aligned)
        for ishape, shape in enumerate(shapes):
            assert isinstance(shape, tuple)
            shapes[ishape] = (1, ) * (self.ndim - len(shape)) + shape

        # check shape compatibility
        # bshape_pre stores value or expressions with array's shape names
        bshape_pre = {i: 1 for i in range(self.ndim)}
        for shape in shapes:
            for iaxis, si in enumerate(shape):
                if bshape_pre[iaxis] == 1:
                    if isinstance(si, int):
                        bshape_pre[iaxis] = si
                    else:
                        assert isinstance(si, str)
                        bshape_pre[iaxis] = var(si)
                elif isinstance(bshape_pre[iaxis], int):
                    if bshape_pre[iaxis] == si:
                        pass
                    elif si == 1:
                        pass
                    elif isinstance(si, Expression):
                        # add precondition
                        # allow symbol == 1 or symbol == constant at runtime
                        assert isinstance(si, str)

                        def check_broadcast_symbol_val(context, iaxis, si):
                            si_val = evaluate(var(si), context)
                            return si_val in (bshape_pre[iaxis], 1)

                        self.preconditions.append(EvaluationPrecondition(
                            partial(check_broadcast_symbol_val, si=si, iaxis=iaxis)))

                        bshape_pre[iaxis] = Max((bshape_pre[iaxis], si))
                    else:
                        raise ValueError(
                            "operands could not be broadcast "
                            "together with shapes %s"
                            % ' '.join(str(s.shape) for s in self.base_arrays))
                else:
                    # bshape_pre has an symbolic member
                    assert isinstance(bshape_pre[iaxis], Expression)
                    if si == 1:
                        pass
                    elif isinstance(si, int):
                        # allow symbol == 1 or symbol == constant at runtime
                        assert isinstance(bshape_pre[iaxis], Expression)

                        def check_broadcast_symbol_val(context, iaxis):
                            lhs_val = evaluate(bshape_pre[iaxis], context)
                            return lhs_val in (bshape_pre[iaxis], 1)

                        self.preconditions.append(EvaluationPrecondition(
                            partial(check_broadcast_symbol_val, iaxis=iaxis)))

                        bshape_pre[iaxis] = Max((bshape_pre[iaxis], si))
                    else:
                        assert isinstance(si, str)
                        if var(si) == bshape_pre[iaxis]:
                            pass
                        else:
                            # establish 'symbol == symbol' equality
                            assert isinstance(bshape_pre[iaxis], Expression)
                            assert isinstance(si, str)

                            def check_broadcast_symbol_val(context, iaxis, si):
                                lhs_val = evaluate(bshape_pre[iaxis], context)
                                si_val = evaluate(var(si), context)
                                return (lhs_val == si_val) or (
                                    lhs_val == 1) or (si_val == 1)

                            self.preconditions.append(EvaluationPrecondition(
                                partial(
                                    check_broadcast_symbol_val, si=si, iaxis=iaxis)))

                            bshape_pre[iaxis] = Max((bshape_pre[iaxis], var(si)))

        # expand expressions
        for key, bs in bshape_pre.items():
            if isinstance(bs, Expression):
                bshape_pre[key] = substitute(bs, expr_map)
            elif is_nonnegative_int(bs):
                bshape_pre[key] = int(bs)
            else:
                raise RuntimeError()

        bshape = tuple(bshape_pre[i] for i in range(self.ndim))
        self._shape_exprs = bshape
        self._size_expr = Product(self._shape_exprs)

        # Unsigneds of broadcast shape
        self.shape = to_lappy_shape(self._shape_exprs)

    def _make_broadcast_arrays(self):
        """After knowing ndim, shape and size symbolically, construct the broadcast
        copies of the input arrays.
        """
        self.broadcast_arrays = []

        for base_arr in self.base_arrays:
            dim_offset = self.ndim - base_arr.ndim
            assert dim_offset >= 0

            # ints and strs
            in_shape = base_arr._get_shape_vals_or_strs()

            if dim_offset == 0:
                if in_shape == self.shape_val_or_str:
                    # unchanged
                    self.broadcast_arrays.append(base_arr)
                    continue

            name = base_arr.name
            if len(name) > 1 and name[:2] == '__':
                name_prefix = ''
            else:
                name_prefix = '__'
            name = (name_prefix + name
                    + '_broadcast%d' % base_arr.__class__._counter)  # noqa: W0212

            brdc_arr = base_arr.with_name(name, False)

            assert isinstance(self.ndim, int) and self.ndim >= 0
            brdc_arr.shape = tuple(s.name for s in self.shape)
            for s in self.shape:
                brdc_arr._decl(s)

            # make new inames
            brdc_arr.inames = self.inames

            # make a new copy with broadcast expression
            #
            # account for semi-dynamic broadcasting, i.e., passing shape value 1
            # at runtime, by fetching from (out_iname % in_shape).
            # TODO: when it is known that such broadcasting cannot happen, this
            #       may be optimized out in loopy by imposing constraints like
            #       out_iname < in_shape
            expr_mapping = {}
            for inm, new_inm, in_shape_i in zip(
                    (None, ) * dim_offset + base_arr.inames,
                    brdc_arr.inames,
                    (None, ) * dim_offset + base_arr._shape_expr):
                if inm is not None:
                    expr_mapping[inm] = new_inm % in_shape_i

            brdc_arr.expr = substitute(brdc_arr.expr, expr_mapping)
            if self._has_trivial_domain_expr():
                brdc_arr.domain_expr = brdc_arr._make_default_domain_expr()
            else:
                raise NotImplementedError()

            # capture the base array
            brdc_arr.namespace[base_arr.name] = (
                            base_arr.as_stateless(),
                            base_arr.namespace[base_arr.name][1].copy()
                            )

            self.broadcast_arrays.append(brdc_arr)

        assert len(self.base_arrays) == len(self.broadcast_arrays)

    @property
    def shape_val_or_str(self):
        return tuple(s if is_nonnegative_int(s) else str(s)
                for s in self._shape_exprs)

    @property
    def size(self):
        from pymbolic.mapper.evaluator import UnknownVariableError
        try:
            return evaluate(self._size_expr)
        except UnknownVariableError:
            return self._size_expr


def broadcast(*arrays):
    """Creates an object that mimics broadcasting.
    """
    arrays = list(arrays)
    for aid in range(len(arrays)):
        if np.isscalar(arrays[aid]):
            arrays[aid] = to_lappy_array(arrays[aid])
    return BroadcastResult(arrays)
