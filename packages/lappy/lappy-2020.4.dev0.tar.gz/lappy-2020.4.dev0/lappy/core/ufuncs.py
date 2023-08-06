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
from pymbolic.primitives import Min, Max, Subscript
import lappy
from lappy.core.array import Array, to_lappy_array
from lappy.core.primitives import FloatingPointRemainder
from lappy.core.broadcast import broadcast


class UFunc(object):
    """Universal (element-by-element) functions.

    .. attribute:: f

        the function applied to the expression of each array element.

    .. attribute:: dtype

        dtype of the function output, useful for e.g. floor().

    .. attribute:: nargs

        The number of arguments

    .. attribute:: preserve_integral

        whether the output is integral for integral inputs.

    .. attribute:: is_integral

        whether the output is always integral (regardless of inputs).

    """
    nargs = -1

    def at(self, a, indices, *args, **kwargs):
        """Performs the ufunc operation at given indices. If the ufunc takes
        more than one arguments, those arugments are specified by the positional
        args.
        """
        if self.nargs < 1:
            raise TypeError(
                "'at' operation cannot be performed "
                "(the ufun must accept at least one argument)")
        if self.nargs != len(args) + 1:
            raise ValueError(
                "wrong number of extra operands (%d needed, %d given)"
                % (self.nargs - 1, len(args)))
        return self.__call__(a[indices], *args, **kwargs)

    def outer(self, a, b, *args, **kwargs):
        if self.nargs < 2:
            raise TypeError(
                "'at' operation cannot be performed "
                "(the ufun must accept at least two arguments)")
        if self.nargs != len(args) + 1:
            raise ValueError(
                "wrong number of extra operands (%d needed, %d given)"
                % (self.nargs - 2, len(args)))
        args = [a, b] + args

        outer_shape = [None, ] * self.nargs
        for idx in range(self.nargs):
            outer_shape[idx] = sum(
                    [[1, ] * args[i].ndim if i == idx else
                        args[i].shape for i in range(self.nargs)],
                    [])

        # reshape the arrays to be broadcastable
        for i, arr in enumerate(args):
            args[i] = arr.reshape(outer_shape[i])

        return self.__call__(*args, **kwargs)

    def __init__(self, expr_func, dtype=None,
                 preserve_integral=False, is_integral=False):
        self.dtype = dtype
        self.f = expr_func
        self.preserve_integral = preserve_integral
        self.is_integral = is_integral

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()


class UnaryOperation(UFunc):
    """Unary universal functions f = f(a).
    """
    nargs = 1

    def __call__(self, a, name=None):
        new_integer_domain = None

        if not isinstance(a, Array):
            a = to_lappy_array(a)

        # non-typed ufunc: pass-through of input's dtype
        if self.dtype is None:
            new_dtype = a.dtype
        else:
            new_dtype = self.dtype

        if name in a.namespace:
            raise ValueError("The name %s is ambiguous" % name)

        if a.namespace[a.name][1].get('is_temporary', False):
            base_expr = Subscript(var(a.name), a.inames)
        else:
            base_expr = a.expr

        obj = {
            'name': name,
            'inames': a.inames,
            'expr': self.f(base_expr), 'value': None,
            'domain_expr': a.domain_expr,
            'env': a.env.copy(),
            'namespace': a.namespace.copy(),
            'preconditions': list(a.preconditions),
            'ndim': a.ndim, 'shape': a.shape,
            'dtype': new_dtype,
            'is_integral':
                (a.is_integral and self.preserve_integral) or self.is_integral,
            'integer_domain': new_integer_domain,
            }
        arr = lappy.ndarray(**obj)

        # update self reference
        arr.namespace[a.name] = (
                a.as_stateless(), a.namespace[a.name][1].copy())
        arr.namespace[arr.name] = (None, dict())

        return arr


class BinaryOperation(UFunc):
    """Binary universal functions f = f(a, b).
    """
    nargs = 2

    def reduce(self, a, axis=0, dtype=None, name=None, keepdims=False):
        """Reduces a's dimension by one, by applying ufunc along one axis.

        For example, add.reduce() is equivalent to np.sum().

        :param a: The input array to act on.

        :param axis: The axis along which to apply the reduction; default is zero.

        :param dtype: The data-type used to represent the intermediate results.
            Defaults to the data-type of the output (as specified by the ufunc) if
            such is provided, or the data-type of the input array if no output dtype
            is provided.

        :param name: Name of the output array, optional.

        :param keepdims: If True, the axes which are reduced are left in the result
            as dimensions with size one. With this option, the result will broadcast
            correctly against the original array.
        """
        # make the reduction domain
        raise NotImplementedError()

    def accumulate(self, a, axis=0, dtype=None, name=None):
        """Accumulates the result of applying the operator to all elements,
        i.e. performs an inclusive scan with the binary ufunc.

        For example, add.accumulate() is equivalent to np.cumsum().

        NOTE: "accumulate" can have different meanings in different contexts.
        For example, ``numpy.ufunc.accumulate`` is scan, but in C++,
        ``std::accumulate`` is reduction. Here, we stay consistent with
        Numpy's definition.

        :param a: The input array to act on.

        :param axis: The axis along which to apply the accumulation; default is zero.

        :param dtype: The data-type used to represent the intermediate results.
            Defaults to the data-type of the output (as specified by the ufunc) if
            such is provided, or the data-type of the input array if no output dtype
            is provided.

        :param name: name of the output array, optional.

        Aliases of accumulate: prefix_sum, cumulative_sum, inclusive_scan, scan,
            partial_sum.
        """
        raise NotImplementedError()

    def prefix_sum(self, *args, **kwargs):
        """See accumulate.
        """
        return self.accumulate(*args, **kwargs)

    def cumulative_sum(self, *args, **kwargs):
        """See accumulate.
        """
        return self.accumulate(*args, **kwargs)

    def inclusive_scan(self, *args, **kwargs):
        """See accumulate.
        """
        return self.accumulate(*args, **kwargs)

    def scan(self, *args, **kwargs):
        """See accumulate.
        """
        return self.accumulate(*args, **kwargs)

    def partial_sum(self, *args, **kwargs):
        """See accumulate.
        """
        return self.accumulate(*args, **kwargs)

    def reduceat(self, a, indices, axis=0, dtype=None, name=None):
        """Performs a (local) reduce with specified slices over a single axis.

        The name is inherited from Numpy; the underlying algorithm is **not** a
        reduction, but a segmented scan.

        Aliases of reduceat: segmented_scan
        """
        raise NotImplementedError()

    def segmented_scan(self, *args, **kwargs):
        """See reduceat.
        """
        return self.reduceat(*args, **kwargs)

    def exclusive_scan(self, a, axis=0, dtype=None, name=None):
        """Exclusive scan.
        """
        raise NotImplementedError()

    def __call__(self, a, b, name=None):

        if not isinstance(a, Array):
            a = to_lappy_array(a)

        if not isinstance(b, Array):
            b = to_lappy_array(b)

        bres = broadcast(a, b)
        a, b = bres.broadcast_arrays

        if self.dtype is None:
            if a.dtype is None:
                new_dtype = b.dtype
            elif b.dtype is None:
                new_dtype = a.dtype
            else:
                new_dtype = np.result_type(a.dtype, b.dtype).type
        else:
            new_dtype = self.dtype

        # expression handling
        if a.namespace[a.name][1].get('is_temporary', False):
            a_expr = Subscript(var(a.name), a.inames)
        else:
            a_expr = substitute(
                    a.expr,
                    {ainame: briname
                        for ainame, briname in zip(a.inames, bres.inames)}
                    )
        if b.namespace[b.name][1].get('is_temporary', False):
            b_expr = Subscript(var(b.name), b.inames)
        else:
            b_expr = substitute(
                    b.expr,
                    {biname: briname
                        for biname, briname in zip(b.inames, bres.inames)}
                    )
        new_expr = self.f(a_expr, b_expr)
        if bres._has_trivial_domain_expr():
            new_domain_expr = None
        else:
            raise NotImplementedError()

        new_integer_domain = None
        obj = {
            'name': name,
            'inames': bres.inames,
            'expr': new_expr, 'value': None,
            'domain_expr': new_domain_expr,
            'namespace': None,
            'env': a.env.copy(),
            'preconditions': a.preconditions + b.preconditions + bres.preconditions,
            'ndim': bres.ndim, 'shape': bres._shape_exprs,
            'dtype': new_dtype,
            'is_integral':
                all([a.is_integral, b.is_integral, self.preserve_integral])
                or self.is_integral,
            'integer_domain': new_integer_domain,
            }
        arr = lappy.ndarray(**obj)

        arr.namespace[arr.name][1]['is_argument'] = False
        arr._meld_namespace(a.namespace.copy(), a.as_stateless())
        arr._meld_namespace(b.namespace.copy(), b.as_stateless())
        arr._meld_env(b.env.copy())

        return arr


# {{{ unary ufuncs

exp = UnaryOperation(lambda x: var('exp')(x))
conjugate = UnaryOperation(lambda x: var('conjugate')(x))
angle = UnaryOperation(lambda x: var('angle')(x))

sin = UnaryOperation(lambda x: var('sin')(x))
cos = UnaryOperation(lambda x: var('cos')(x))
tan = UnaryOperation(lambda x: var('tan')(x))
arcsin = UnaryOperation(lambda x: var('arcsin')(x))
arccos = UnaryOperation(lambda x: var('arccos')(x))
arctan = UnaryOperation(lambda x: var('arctan')(x))

sinh = UnaryOperation(lambda x: var('sinh')(x))
cosh = UnaryOperation(lambda x: var('cosh')(x))
tanh = UnaryOperation(lambda x: var('tanh')(x))
arcsinh = UnaryOperation(lambda x: var('arcsinh')(x))
arccosh = UnaryOperation(lambda x: var('arccosh')(x))
arctanh = UnaryOperation(lambda x: var('arctanh')(x))

abs = absolute = UnaryOperation(lambda x: var('abs')(x), preserve_integral=True)
fabs = UnaryOperation(lambda x: var('fabs')(x))

negative = UnaryOperation(lambda x: -x, preserve_integral=True)
floor = UnaryOperation(lambda x: var('floor')(x),
                       preserve_integral=True, is_integral=True)
ceil = UnaryOperation(lambda x: var('ceil')(x),
                      preserve_integral=True, is_integral=True)
around = UnaryOperation(lambda x: var('around')(x),
                        preserve_integral=True, is_integral=True)

logical_not = UnaryOperation(lambda x: x.not_())

sqrt = UnaryOperation(lambda x: var('sqrt')(x))
log = UnaryOperation(lambda x: var('log')(x))
log2 = UnaryOperation(lambda x: var('log2')(x))
log10 = UnaryOperation(lambda x: var('log10')(x))

# }}} End unary ufuncs

# {{{ binary ufuncs

add = BinaryOperation(expr_func=lambda x, y: x + y, preserve_integral=True)
subtract = BinaryOperation(expr_func=lambda x, y: x - y, preserve_integral=True)
multiply = BinaryOperation(expr_func=lambda x, y: x * y, preserve_integral=True)
divide = BinaryOperation(expr_func=lambda x, y: x / y)
floordiv = BinaryOperation(expr_func=lambda x, y: x // y, is_integral=True)
power = BinaryOperation(expr_func=lambda x, y: x**y, preserve_integral=True)

equal = BinaryOperation(lambda x, y: x.eq(y))
not_equal = BinaryOperation(lambda x, y: x.ne(y))
less_equal = BinaryOperation(lambda x, y: x.le(y))
greater_equal = BinaryOperation(lambda x, y: x.ge(y))
less = BinaryOperation(lambda x, y: x.lt(y))
greater = BinaryOperation(lambda x, y: x.gt(y))

logical_and = BinaryOperation(lambda x, y: x.and_(y))
logical_or = BinaryOperation(lambda x, y: x.or_(y))

# integer mode, and returns the same sign with y
mod = remainder = BinaryOperation(lambda x, y: x % y)

# floating point mod, and returns the same sign with x
fmod = BinaryOperation(lambda x, y: FloatingPointRemainder(x, y))

minimum = BinaryOperation(lambda x, y: Min([x, y]))
maximum = BinaryOperation(lambda x, y: Max([x, y]))

# }}} End binary ufuncs
