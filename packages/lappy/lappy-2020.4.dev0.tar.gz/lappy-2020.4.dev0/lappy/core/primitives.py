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

from six.moves import intern

from pymbolic.primitives import AlgebraicLeaf
from pymbolic.primitives import Expression
from pymbolic.primitives import QuotientBase
from pymbolic.primitives import Variable

from lappy.core.mapper import SetExpressionStringifyMapper

# {{{ Array computation primitives


class FloatingPointRemainder(QuotientBase):
    """
    .. attribute:: numerator
    .. attribute:: denominator
    """

    mapper_method = intern("map_floating_point_remainder")


class Assignment(AlgebraicLeaf):
    """Assignments split the expression into multiple loopy statements.

    The result of an assignment is the value that "passes through" the
    assignment.
    """

    init_arg_names = ("lhs", "rhs")

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs


class Reduction(AlgebraicLeaf):
    """Reduce is a parallel algorithmic primitive. Unlike :class:`Sum`, reuction
    operates over the index domain of an array, which may be parametrized.

    Note that there is no 'scan' primitive, as array-valued expressions are
    prohibited. Scan is expressed as an array where each element is the result of
    a reduction with an affine kernel. For example,

        scan('+', A)[i] = reduce('+', A, "[i] -> {[j] : 0 <= j < i}")

    .. attribute:: op

        A binary ufunc used for the reduction.

    .. attribute:: array

        The array to be reduced, e.g. Variable('A').

    .. attribute:: kernel

        The kernel of the index mapping, i.e., the domain over which the reduction
        is performed, a domain expression (that compiles to an ISL basic set).
    """

    init_arg_names = ("op", "array", "kernel")

    def __init__(self, op, array, kernel):
        self.op = op
        self.array = array
        self.kernel = kernel

# }}} End Array computation primitives

# {{{ Integer set computation primitives


EMPTY_SET = 0
UNIVERSE_SET = 1  # complement of the empty set


class SetExpression(Expression):
    """Expression with replaced stringifier.

    The expression tree has two layers, a lower layer of PwAffs and an upper layer of
    Sets.
    The leaf nodes are PwAffs, and the internal layer above the comparison nodes are
    Sets. All nodes further above are also Sets.
    """
    # {{{ disable unused methods for easier debugging

    def __add__(self, *args, **kwargs):
        raise NotImplementedError()

    def __radd__(self, *args, **kwargs):
        raise NotImplementedError()

    def __sub__(self, *args, **kwargs):
        raise NotImplementedError()

    def __rsub__(self, *args, **kwargs):
        raise NotImplementedError()

    def __mul__(self, *args, **kwargs):
        raise NotImplementedError()

    def __rmul__(self, *args, **kwargs):
        raise NotImplementedError()

    def __div__(self, *args, **kwargs):
        raise NotImplementedError()

    def __truediv__(self, *args, **kwargs):
        return self.__div__(*args, **kwargs)

    def __rdiv__(self, *args, **kwargs):
        raise NotImplementedError()

    def __floordiv__(self, *args, **kwargs):
        raise NotImplementedError()

    def __rfloordiv__(self, *args, **kwargs):
        raise NotImplementedError()

    def __mod__(self, *args, **kwargs):
        raise NotImplementedError()

    def __rmod__(self, *args, **kwargs):
        raise NotImplementedError()

    def __pow__(self, *args, **kwargs):
        raise NotImplementedError()

    def __rpow__(self, *args, **kwargs):
        raise NotImplementedError()

    def __lshift__(self, other):
        raise NotImplementedError()

    def __rlshift__(self, other):
        raise NotImplementedError()

    def __rshift__(self, other):
        raise NotImplementedError()

    def __rrshift__(self, other):
        raise NotImplementedError()

    def __inv__(self):
        raise NotImplementedError()

    def __or__(self, other):
        raise NotImplementedError()

    def __ror__(self, other):
        raise NotImplementedError()

    def __xor__(self, other):
        raise NotImplementedError()

    def __rxor__(self, other):
        raise NotImplementedError()

    def __and__(self, other):
        raise NotImplementedError()

    def __rand__(self, other):
        raise NotImplementedError()

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()

    def eq(self, *args, **kwargs):
        raise NotImplementedError()

    def ne(self, *args, **kwargs):
        raise NotImplementedError()

    def le(self, *args, **kwargs):
        raise NotImplementedError()

    def lt(self, *args, **kwargs):
        raise NotImplementedError()

    def ge(self, *args, **kwargs):
        raise NotImplementedError()

    def gt(self, *args, **kwargs):
        raise NotImplementedError()

    def not_(self, *args, **kwargs):
        raise NotImplementedError()

    # }}} End disabled methods

    def make_stringifier(self, originating_stringifier=None):
        return SetExpressionStringifyMapper()

    def or_(self, other):
        if isinstance(self, PwAff) or isinstance(other, PwAff):
            raise ValueError("cannot compute set union of %s and %s"
                             % (str(self), str(other)))
        if isinstance(other, SetUnion):
            return SetUnion((self, ) + other.children)
        else:
            return SetUnion((self, other))

    def and_(self, other):
        if isinstance(self, PwAff) or isinstance(other, PwAff):
            raise ValueError("cannot compute set intersection of %s and %s"
                             % (str(self), str(other)))
        if isinstance(other, SetIntersection):
            return SetIntersection((self, ) + other.children)
        else:
            return SetIntersection((self, other))

    def _make_pwaff_comparison(self, op, other):
        if not isinstance(self, PwAff) and isinstance(other, PwAff):
            raise ValueError("cannot do pwaff comparison with %s and %s"
                    % (str(self), str(other)))
        return PwAffComparison(self, op, other)


class PwAffComparison(SetExpression):
    """PwAffs form sets via the comparison node.

    .. attribute:: left
    .. attribute:: operator

        One of ``[">", ">=", "==", "!=", "<", "<="]``.

    .. attribute:: right
    """

    init_arg_names = ("left", "operator", "right")

    def __init__(self, left, operator, right):
        self.left = left
        self.right = right
        if operator not in [">", ">=", "==", "!=", "<", "<="]:
            raise RuntimeError("invalid operator")
        self.operator = operator

    def __getinitargs__(self):
        return self.left, self.operator, self.right

    mapper_method = intern("map_pwaff_comparison")


class _MultiChildSetExpression(SetExpression):
    init_arg_names = ("children",)

    def __init__(self, children):
        assert isinstance(children, tuple)

        self.children = children

    def __getinitargs__(self):
        return self.children,


class SetUnion(_MultiChildSetExpression):
    """
    .. attribute:: children

        A :class:`tuple`.
    """
    def or_(self, other):
        if isinstance(other, PwAff):
            raise ValueError()
        if isinstance(other, SetUnion):
            return SetUnion(self.children + other.children)
        else:
            return SetUnion(self.children + (other, ))

    mapper_method = intern("map_set_union")


class SetIntersection(_MultiChildSetExpression):
    """
    .. attribute:: children

        A :class:`tuple`.
    """
    def and_(self, other):
        if isinstance(other, PwAff):
            raise ValueError()
        if isinstance(other, SetIntersection):
            return SetIntersection(self.children + other.children)
        else:
            return SetIntersection(self.children + (other, ))

    mapper_method = intern("map_set_intersection")


class PwAff(SetExpression):
    """PwAff: variables used to construct piecewise-affine expressions.

    .. attribute:: name
    """
    init_arg_names = ("name",)
    mapper_method = intern('map_pwaff')

    def __init__(self, name):
        assert name
        self.name = intern(name)

    def __getinitargs__(self):
        return self.name,

    def __lt__(self, other):
        if isinstance(other, Variable):
            return self.name.__lt__(other.name)
        else:
            return NotImplemented

    def __setstate__(self, val):
        super(Variable, self).__setstate__(val)

        self.name = intern(self.name)

    def le(self, other):
        return self._make_pwaff_comparison('<=', other)

    def lt(self, other):
        return self._make_pwaff_comparison('<', other)

    def ge(self, other):
        return self._make_pwaff_comparison('>=', other)

    def gt(self, other):
        return self._make_pwaff_comparison('>', other)

    def eq(self, other):
        return self._make_pwaff_comparison('==', other)

    def ne(self, other):
        return self._make_pwaff_comparison('!=', other)

    def __add__(self, other):
        if not isinstance(other, (PwAff, int)):
            return ValueError()
        if isinstance(other, PwAffSum):
            return PwAffSum((self,) + other.children)
        else:
            return PwAffSum((self, other))

    def __radd__(self, other):
        assert isinstance(other, int)
        return PwAffSum((other, self))

    def __sub__(self, other):
        return self + (-1) * other

    def __rsub__(self, other):
        return self + (-1) * other

    def __floordiv__(self, other):
        if not isinstance(other, int) and other > 0:
            return ValueError()
        return PwAffFloorDiv(self, other)

    def __mod__(self, other):
        if not isinstance(other, int) and other > 0:
            return ValueError()
        return PwAffRemainder(self, other)

    def __mul__(self, other):
        if not isinstance(other, (PwAff, int)):
            return ValueError()
        if isinstance(other, PwAffProduct):
            return PwAffProduct((self,) + other.children)
        else:
            return PwAffProduct((self, other))

    def __rmul__(self, other):
        assert isinstance(other, int)
        return PwAffProduct((other, self))


class _MultiChildPwAff(PwAff):
    init_arg_names = ("children",)

    def __init__(self, children):
        assert isinstance(children, tuple)

        self.children = children

    def __getinitargs__(self):
        return self.children,


class SetVar(PwAff):
    """Set variable.
    """

    mapper_method = 'map_set_variable'


class SetParam(PwAff):
    """Set parameter.
    """

    mapper_method = 'map_set_parameter'


class SetZero(PwAff):
    """The constant 0.
    """
    def __init__(self):
        super(SetZero, self).__init__('ZERO')

    mapper_method = 'map_set_zero'


class PwAffSum(_MultiChildPwAff):
    """Sum of PwAffs.

    .. attribute:: children

        A :class:`tuple`.
    """

    def __add__(self, other):
        if not isinstance(other, (int, PwAff)):
            return ValueError()
        if isinstance(other, PwAffSum):
            return PwAffSum(self.children + other.children)
        return PwAffSum(self.children + (other,))

    def __radd__(self, other):
        if not isinstance(other, int):
            return ValueError()
        if isinstance(other, PwAffSum):
            return PwAffSum(other.children + self.children)
        return PwAffSum((other,) + self.children)

    mapper_method = intern("map_pwaff_sum")


class PwAffProduct(_MultiChildPwAff):
    """Product of PwAffs. Up to one non-constant child is allowed.

    .. attribute:: children

        A :class:`tuple`.
    """
    def __mul__(self, other):
        if not isinstance(other, (PwAff, int)):
            return ValueError()
        if isinstance(other, PwAffProduct):
            return PwAffProduct(self.children + other.children)
        return PwAffProduct(self.children + (other,))

    def __rmul__(self, other):
        if not isinstance(other, int):
            return ValueError()
        return PwAffProduct((other,) + self.children)

    mapper_method = intern("map_pwaff_product")


class PwAffQuotientBase(PwAff):
    init_arg_names = ("numerator", "denominator",)

    def __init__(self, numerator, denominator=1):
        self.numerator = numerator
        self.denominator = denominator

    def __getinitargs__(self):
        return self.numerator, self.denominator

    mapper_method = None


class PwAffFloorDiv(PwAffQuotientBase):
    """
    .. attribute:: numerator
    .. attribute:: denominator
    """

    mapper_method = intern("map_pwaff_floor_div")


class PwAffRemainder(PwAffQuotientBase):
    """
    .. attribute:: numerator
    .. attribute:: denominator
    """

    mapper_method = intern("map_pwaff_remainder")

# }}} End Integer set computation primitives
