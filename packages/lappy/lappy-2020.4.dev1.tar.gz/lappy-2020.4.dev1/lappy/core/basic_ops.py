# -*- coding: utf-8 -*-
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
from pymbolic import var, evaluate, substitute
from pymbolic.primitives import Variable, Product, Subscript

from lappy.exceptions import AxisError
from lappy.core.ufuncs import minimum, maximum
from lappy.core.conditional import conditional
from lappy.core.array import (
        Array, to_lappy_shape, to_lappy_unsigned, isscalar)
from lappy.core.preconditions import (
        EvaluationPrecondition,
        make_size_conservation_condition)

# {{{ masking


class MaskedArrayFactory(object):
    """Factory class of the sub-arrays produced by indexing with a boolean
    array with equal shape.

    Filtered arrays cannot be created as stand-alone expressions; they
    are used solely for the lhs of an assignment. For example, to execute

        A[A > 0] = B[A > 0]

    It is achieved by overloading __setitem__() of the LHS.

    If the user asks for the value of A[A > 0], the kernel will compute
    the full array A and the boolean array (A > 0). And then lappy will
    simply use numpy to give the results.
    """

    def __init__(self, base, mask):
        assert isinstance(base, Array)
        assert isinstance(mask, Array)
        assert base.ndim == mask.ndim
        self.base_arr = base
        self.mask_arr = mask
        # TODO: precondition on equal shapes

    def __call__(self):
        # TODO: make a special kind of array, whose evaluation returns multiple
        # results, which form the final reults after some post-processing.
        #
        # e.g., A[A > 0]
        raise NotImplementedError()

# }}} End masking

# {{{ indexing


class SubArrayFactory(object):
    """Factory class of the sub-arrays produced by indexing with a tuple of
    (generalized) indices.

    For the syntax and semantics are the same as numpy arrays
    https://docs.scipy.org/doc/numpy/reference/arrays.indexing.html

    .. attribute:: base_arr

        the base array being indexed.

    .. attribute:: selectors

        a list of selection objects.

    .. attribute:: ndim

        ndim of the output array.

    .. attribute:: advanced_indexing

        list of bools, whether is using advanced indexing for each axis.

    .. attribute:: boolean_masking

        list of bools, whether is masked with a boolean array for each axis.
        Meaningful only if advanced_indexing is True.
    """

    # {{{ constructor

    def __init__(self, base, selobj=None):
        """
        :param base_arr: the base array.
        :param selectors: the selection object.
        """
        assert isinstance(base, Array)
        self.base_arr = base

        # normalize the selectors list
        if isinstance(selobj, tuple):
            selist = list(selobj)
        elif isinstance(selobj, (int, Array, list, np.ndarray)):
            selist = [selobj, ]
        elif selobj is None:
            selist = []
        else:
            raise TypeError()

        assert isinstance(selist, list)
        n_ell = 0
        for idx in selist:
            if idx is Ellipsis:
                n_ell += 1

        if n_ell > 1:
            raise IndexError(
                    "an index can only have a single ellipsis ('...')")
        elif n_ell == 0:
            # hand un-addressed axes with a trailing ellipsis
            selist.append(Ellipsis)
            n_ell += 1

        self.selectors = selist
        self.ndim = self._get_out_ndim()
        self._expand_ellipsis()

        self.advanced_indexing = self._prepare_advanced_indexing()
        assert len(self.advanced_indexing) == self.ndim

        self.boolean_masking = self._prepare_boolean_masking()
        assert len(self.boolean_masking) == self.ndim

    # }}} End constructor

    # {{{ consume the selection object

    def _get_out_ndim(self):
        """Compute the rank (ndim) of the output array.
        """
        ndim = 0
        n_annihil_dim = 0
        for sel in self.selectors:
            if isinstance(sel, slice):  # slicing
                ndim += 1
            elif sel is None:  # np.newaxis
                ndim += 1
            elif isscalar(sel):  # scalar indexing
                n_annihil_dim += 1
            elif isinstance(sel, (tuple, list, np.ndarray, Array)):
                sel_arr = np.array(sel)
                if sel_arr.dtype is np.dtype(bool) or sel_arr.dtype is bool:
                    # boolean indexing "flattens"
                    ndim += 1
                else:
                    # integer indexing keeps the dimension
                    ndim += sel_arr.ndim
            else:
                if sel is not Ellipsis:
                    raise TypeError()

        return max(ndim, self.base_arr.ndim, n_annihil_dim)

    def _prepare_advanced_indexing(self):
        """Identify if the selection object is/contains advanced indexing
        for each output axis.
        """
        advanced = [False, ] * self.ndim
        for isel, sel in enumerate(self.selectors):
            if isinstance(sel, Array):
                advanced[isel] = True
        return advanced

    def _prepare_boolean_masking(self):
        """Identify if the selection object is/contains advanced indexing
        via boolean masking for each output axis.
        """
        bool_masked = [False, ] * self.ndim
        for isel, sel in enumerate(self.selectors):
            if isinstance(sel, Array):
                if sel.dtype == bool or self.dtype == np.bool_:
                    bool_masked[isel] = True
        return bool_masked

    def _complete_slice(self, slc, iaxis):
        """Fill in all information for a partially specified slice.

        :param slc: an (incomplete) slice object.
        :param iaxis: the index of the axis being sliced.
        """
        assert isinstance(slc, slice)
        dim_name = self.base_arr.shape[iaxis]
        dim = self.base_arr._extract(dim_name)

        step_none = slc.step is None
        if step_none:
            step = 1
        else:
            step = slc.step

        start = slc.start
        start_none = slc.start is None
        if not start_none:
            start = conditional(start < 0, start + dim, start)

        stop = slc.stop
        stop_none = slc.stop is None
        if not stop_none:
            stop = conditional(stop < 0, stop + dim, stop)

        start_p = 0 if start_none else maximum(0, minimum(dim, start))
        stop_p = dim if stop_none else maximum(start_p, minimum(dim, stop))

        start_m = dim - 1 if start_none \
            else maximum(-1, minimum(dim - 1, start))
        stop_m = -1 if stop_none else maximum(-1, minimum(start_m, stop))

        start = conditional(step > 0, start_p, start_m)
        stop = conditional(step > 0, stop_p, stop_m)

        return slice(start, stop, step)

    def _expand_ellipsis(self):
        """Expand ellipsis into proper number of slices.
        """
        ell_id = self.selectors.index(Ellipsis)
        fullslice = slice(None, None, None)
        self.selectors[ell_id:ell_id + 1] = (
                (fullslice, ) * (self.base_arr.ndim - len(self.selectors) + 1))

    # }}} End consume the selection object

    # {{{ basic indexing

    def _basic_getitem(self, basic_selectors):
        """Tthe basic_selectors must only consist of:
        slices, integers, Ellipsis, and np.newaxis (None).
        """
        ca = 0  # current axis
        i_newaxis = 0
        new_shape = []
        new_inames = []
        rhs_index_exprs = []

        new_namespace = self.base_arr.namespace.copy()
        new_namespace[self.base_arr.name] = (
                self.base_arr.as_stateless(),
                self.base_arr.namespace[self.base_arr.name][1].copy())

        new_name = self.base_arr._make_default_name()

        for i_sel, sel in enumerate(basic_selectors):
            if sel is None:
                # newaxis does not advance the ca pointer
                new_shape.append(to_lappy_unsigned(1))
                new_inames.append(var('__indexing_%s_newaxis_inames_%d'
                                      % (self.base_arr.name, i_newaxis)))
                i_newaxis += 1

            elif ca >= self.base_arr.ndim:
                raise IndexError('too many indices for array')

            elif isinstance(sel, slice):
                se = self._complete_slice(sel, iaxis=ca)

                se_size = (se.stop - se.start + se.step - 1) // se.step
                new_shape.append(se_size)

                iname = self.base_arr.inames[ca]
                new_inames.append(iname)

                if isinstance(se.start, Array):
                    start = se.start.expr
                    new_namespace[se.start.name] = (
                            se.start,
                            se.start.namespace[se.start.name][1].copy())
                else:
                    start = se.start

                if isinstance(se.step, Array):
                    step = se.step.expr
                    new_namespace[se.step.name] = (
                            se.step,
                            se.step.namespace[se.step.name][1].copy())
                else:
                    step = se.step

                rhs_index_exprs.append(
                        start + step * iname)
                ca += 1

            elif isscalar(sel):
                new_shape.append(1)
                iname = self.base_arr.inames[ca]
                new_inames.append(iname)
                rhs_index_exprs.append(sel)
                ca += 1

            else:
                raise TypeError('invalid index type: %s'
                                % type(basic_selectors[i_sel]))

        # NOTE: since complex expressions cannot be subscrpted,
        # if the expression is non trivial, this will automatically
        # add a temporary.
        new_expr = Subscript(
                var(self.base_arr.name),
                index=tuple(rhs_index_exprs))

        obj = {
            'name': new_name,
            'inames': tuple(new_inames),
            'expr': new_expr,
            'value': None,
            'domain_expr': self.base_arr.domain_expr,
            'env': self.base_arr.env.copy(),
            'namespace': new_namespace,
            'preconditions': self.base_arr.preconditions,
            'ndim': self.ndim,
            'shape': new_shape,
            'dtype': self.base_arr.dtype,
            'is_integral': self.base_arr.is_integral,
            'integer_domain': self.base_arr.integer_domain,
            }
        arr = self.base_arr.__class__(**obj)

        if not self.base_arr._has_trivial_expr():
            # make previous results cse to ensure correct dependence
            arr.pin(self.base_arr.name, cse=True)

        return arr

    # }}} End basic indexing

    # {{{ advanced indexing

    def _advanced_getitem(self):
        """Handle advanced indexing of two cases:

        1) array of size_t
        2) array of bool
        """
        raise NotImplementedError()

    # }}} End advanced indexing

    def __call__(self):
        """Create the sub-array.
        """
        if any(self.advanced_indexing):
            return self._advanced_getitem()

        return self._basic_getitem(self.selectors)

# }}} End indexing

# {{{ reshape


def reshape(array, newshape, order='C', name=None, inames=None):
    """Reshape an array to the given shape.

    :param array: Array to be reshaped.

    :param newshape: int or tuple of ints.
        The new shape should be compatible with the original shape.
        If an integer, then the result will be a 1-D array of that length.
        One shape dimension can be -1. In this case, the value is inferred
        from the length of the array and remaining dimensions.

    :param order: str in {'C', 'F'}, optional.
        Read the elements of the input array using this index order, and
        place the elements into the reshaped array using this index order.

        ‘C’ means to read / write the elements using C-like index order,
        with the last axis index changing fastest, back to the first axis index
        changing slowest.

        ‘F’ means to read / write the elements using Fortran-like index order,
        with the first index changing fastest, and the last index changing
        slowest.

        The order is "mental" only and may or may not reflect the actual memory
        layout.

    :param name: Name of the reshaped array, optional.

    :param inames: Name of indices of the reshaped array, optional.

    :return: A copy of the reshaped array.
    """
    if isinstance(newshape, (tuple, list)):
        new_ndim = len(newshape)
        newshape = list(newshape)
    else:
        # reshape into 1-D array
        assert np.isscalar(newshape)
        assert int(newshape) == newshape
        assert newshape > 0 or newshape == -1
        new_ndim = 1

        if newshape == -1:
            newshape = to_lappy_unsigned(array.size)
        newshape = [newshape, ]

    new_precond = list(array.preconditions)

    # if there is a -1 in newshape, infer its value at runtime
    if -1 in newshape:
        if newshape.count(-1) > 1:
            raise ValueError("can only specify one unknown dimension")

        shadow = tuple(s for s in newshape if s != -1)
        shadow_expr = tuple(
            var(s.name) if hasattr(s, 'name') else s
            for s in shadow)

        missing_id = newshape.index(-1)
        newshape[missing_id] = array.size // Product(shadow_expr)

        def newaxis_is_integral(context):
            """The shape must be an integer along the newaxis.
            """
            old_size = evaluate(array.size, context)
            _shadow_size = evaluate(Product(shadow_expr), context)

            act_new_shape = tuple(
                var(s.name) if hasattr(s, 'name') else s
                for s in newshape)

            if not old_size % _shadow_size == 0:
                raise ValueError("cannot reshape array of size %s into shape %s"
                        % (str(old_size), str(act_new_shape)))
            return old_size % _shadow_size == 0

        # add pre-eval runtime checks on size consistency
        new_precond.append(
            EvaluationPrecondition(newaxis_is_integral))

    if name is None:
        if len(array.name) > 1 and array.name[:2] == '__':
            name_prefix = ''
        else:
            name_prefix = '__'
        name = (name_prefix + array.name
                + '_reshaped%d' % array.__class__._counter)  # noqa: W0212

    if inames is None:
        if len(name) > 1 and name[:2] == '__':
            name_prefix = ''
        else:
            name_prefix = '__'
        inames = tuple(
            var(name_prefix + name + '_inames_%d' % iaxis)
            for iaxis in range(new_ndim))
    else:
        assert len(inames) == new_ndim
        assert all(isinstance(inm, Variable) for inm in inames)

    if not np.isscalar(array.size):
        # add pre-eval runtime checks on size conservation
        check_size_conservation = make_size_conservation_condition(array, newshape)
        new_precond.append(check_size_conservation)
    else:
        # static assersion
        if not np.prod(newshape) == array.size:
            raise ValueError("cannot reshape array of size %d into %s"
                    % (array.size, str(newshape)))

    if order == 'C':
        flat_id = inames[0]
        axis_range = range(1, new_ndim)
    elif order == 'F':
        flat_id = inames[-1]
        axis_range = reversed(range(0, new_ndim - 1))
    else:
        raise ValueError("order must be either 'C' or 'F' (got %s)" % str(order))

    # id in the flattened array
    for iaxis in axis_range:
        flat_id = flat_id * newshape[iaxis] + inames[iaxis]

    if order == 'C':
        iname_subs = {
                array.inames[0]: flat_id // array._shadow_size(range(1, array.ndim))
                }
        for iaxis in range(1, array.ndim):
            flat_id = flat_id % array._shadow_size(range(iaxis, array.ndim))
            iname_subs[array.inames[iaxis]] = flat_id // array._shadow_size(
                    range(iaxis + 1, array.ndim))
    else:
        assert order == 'F'
        iname_subs = {
            array.inames[-1]: flat_id // array._shadow_size(range(array.ndim - 1))
            }
        for iaxis in range(-2, -array.ndim - 1, -1):
            flat_id = flat_id % array._shadow_size(range(array.ndim + iaxis + 1))
            iname_subs[array.inames[iaxis]] = flat_id // array._shadow_size(
                range(array.ndim + iaxis))

    new_arr = array.with_name(name, False)
    new_arr.inames = inames
    new_arr.preconditions = new_precond

    newshape = to_lappy_shape(newshape)
    new_arr.shape = tuple(s.name for s in newshape)
    for s in newshape:
        new_arr._meld_namespace(s.namespace, s.as_stateless())
        new_arr._meld_env(s.env)

    new_arr.namespace[array.name] = (
            array.as_stateless(),
            array.namespace[array.name][1].copy())
    new_arr.namespace[name] = (None, {})

    if (not array._has_trivial_expr()) or (not array._has_trivial_domain_expr()):
        # make previous results cse to ensure correct dependencies
        # whenever the reshaped array has nontrivial (domain) expression
        new_arr.pin(array.name, cse=True)

    new_arr.expr = substitute(array.expr, iname_subs)
    if array._has_trivial_domain_expr():
        new_arr.domain_expr = new_arr._make_default_domain_expr()
    else:
        # make new index domain and take union with the previous domain
        raise NotImplementedError()

    return new_arr

# }}} End reshape

# {{{ transpose


def transpose(array, axes=None, name=None):
    """Transpose.

    :param array: Input array.

    :param axes: By default, reverse the dimensions, otherwise permute the axes
        according to the values given.

    :param name: Name of the transposed array, optional.

    :return: A copy of transposed array.
    """
    ndim = array.ndim
    if axes is None:
        axes = list(range(ndim - 1, -1, -1))
    else:
        axes = list(axes)

    if not len(axes) == ndim:
        raise ValueError("axes don't match array")
    ax_flags = [0, ] * ndim
    for i in range(ndim):
        if axes[i] >= ndim or axes[i] < -ndim:
            raise AxisError("axis %d is out of bounds for array of dimension %d"
                    % (axes[i], ndim))
        if axes[i] < 0:
            axes[i] += ndim
        if ax_flags[axes[i]] > 0:
            raise ValueError("repeated axis in transpose")
        ax_flags[axes[i]] += 1

    if name is None:
        if len(array.name) > 1 and array.name[:2] == '__':
            name_prefix = ''
        else:
            name_prefix = '__'
        name = (name_prefix + array.name
                + '_T%d' % array.__class__._counter)  # noqa: W0212

    new_arr = array.with_name(name, False)

    new_arr.inames = tuple(array.inames[axes[i]] for i in range(ndim))
    new_arr.shape = tuple(array.shape[axes[i]] for i in range(ndim))
    return new_arr

# }}} End transpose
