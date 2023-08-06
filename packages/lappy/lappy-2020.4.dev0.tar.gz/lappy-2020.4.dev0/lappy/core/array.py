# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, print_function

import warnings
import numpy as np

import islpy as isl
import pymbolic
from pymbolic import var, evaluate
from pymbolic.primitives import Lookup, Subscript, Variable, Product
from pymbolic.mapper.evaluator import UnknownVariableError

from pprint import pformat

from lappy.core.primitives import SetVar, SetParam

copyright__ = "Copyright (C) 2019 Sophia Lin, Andreas Kloeckner and Xiaoyu Wei"

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


def default_env():
    """Default environment to be captured.
    """
    return dict()


# {{{ base lazy obj class


class LazyObjectBase(object):
    """Base class for objects that are lazily evaluated.
    Lappy's lazy objects (Lapjects) are identified by their names.
    If not otherwise specified, a unique name is generated.

    .. attribute:: name

        the name of the object, should be a Python identifier and
        do not start with double underscore '__' (which is reserved
        for internal use). A lazy object's symbolic information is
        uniquely determined by the name, that is, if two lazy objects
        share the same name, they are treated as the same computation
        (but can have different captured environments).

    .. attribute:: expr

        :mod:`pymbolic` expression that describes the computation

    .. attribute:: value

        the actual data. None if not yet evaluated.

    .. attribute:: env

        the captured environment, a :class:`dict`. The environment is
        fully known before runtime, i.e., does not contain lazy objects.

        If env is None, the object is called **stateless**. Stateless objects serve
        as parts of a lazy object with state, e.g., as the input arguments.

    .. attribute:: namespace

        a dictionary with names as keys, and tuple of

            ``(stateless_lazy_object, object_desc)``

        as values, where ``object_desc`` is a dictionary of tags. Sample tags are:

            ``is_argument``: whether the object is an input argument.
            ``is_temporary``: whether the object is a temporary.

        /All tags default to False./

        The namespace associated with a lazy object contains all
        lazy objects involved during the construction of itself. Stateless
        lazy objects' namespaces should be None.

        In particular, to avoid duplications, ``None`` is used wherever infinite
        recursion occurs, e.g. ``self.namespace[self.name][0] = None``.

        Besides the input arguments, the namespace can also contain temporaries
        produced in the process of assembling the expression. Those temporaries do
        not translate to actual temporary variable in the kernel. But they could
        contain useful information otherwise lost, e.g. user-specified names of the
        intermediate results.

    .. attribute:: preconditions

        preconditions are checked at runtime, prior to calling the kernel.
        It is a list of callables, each of which can take one or more
        input arguments. If a precondition fails, an
        :class:`Exception` is thrown prior to calling the kernel.
    """
    _counter = 0
    _name_prefix = '__lappy_object_'

    # {{{ constructor

    def __init__(self, **kwargs):
        """Constructor.

        :param name:          (optional) name of the lapject
        :param expr:          the expression
        :param env:           (optional) captured environment
        :param namespace:     (optional) list of symbols
        :param value:         (optional) value of the lapject
        :param preconditions: dynamic pre-runtime checks
        """

        self.name = kwargs.pop("name", None)
        self.expr = kwargs.pop("expr")

        if self.name is None:
            self.name = self._make_default_name()

        self.namespace = kwargs.pop("namespace", None)
        self.env = kwargs.pop("env", None)

        if self.namespace is None:
            self.namespace = {self.name: (None, {'is_argument': True})}

        if self.name not in self.namespace:
            self.namespace[self.name] = (None, {'is_argument': True})

        if 'value' in kwargs.keys():
            if self.is_stateless:
                raise TypeError("cannot construct a stateless obj with value")
            elif self.value is not None:
                if self.value != kwargs['value']:
                    raise ValueError(
                            "got conflicting values set from env and value")
                else:
                    pass
            else:
                self.value = kwargs.pop("value")

        self.preconditions = kwargs.pop("preconditions", list())

    # }}} End constructor

    # {{{ namespace/env utils

    def _decl(self, lapject, tags=None):
        """Add symbol to the namespace.
        """
        if self.is_stateless:
            raise TypeError(
                    "can only declare names inside a stateful "
                    "lappy object ")
        assert isinstance(lapject, LazyObjectBase)
        name = lapject.name

        if name in self.namespace:
            raise ValueError("name %s is taken" % name)

        if lapject.has_state:
            self._meld_namespace(lapject.namespace, lapject.as_stateless())
            self._meld_env(lapject.env)
            if tags is None:
                tags = lapject.namespace[name][1].copy()

        if tags is None:
            tags = dict()
        else:
            assert isinstance(tags, dict)

        self.namespace[name] = (lapject.as_stateless(), tags)

    def _check_namespace_integrity(self, namespace=None, name=None):
        """Check that all namespace keys equals the name of the contained
        object.
        """
        if namespace is None:
            namespace = self.namespace
        if name is None:
            name = self.name
        for key, (val, tag) in namespace.items():
            if val is None:
                assert name == key
            else:
                assert val.name == key

    def _meld_namespace(self, namespace, stateless_self=None):
        """Merge with another namespace. The other namespace may contain a
        self-reference (reference to the name containing the namespace).
        If so, the ``stateless_self`` is used to substitute ``None``.

        If there are multiple definitions of a name, the function will
        try to merge the information from all sources. An exception is
        raised if conflicting information is found.
        """
        handled_selref = False
        for nm, (lapject, tags) in namespace.items():
            if lapject is None:
                if stateless_self is None:
                    raise ValueError("a stateless copy of the enclosing "
                                     "lapject is needed when importing "
                                     "a namespace with self-reference")
                if handled_selref:
                    raise ValueError("illegal namespace (contains more "
                                     "than one self-references)")
                assert isinstance(stateless_self, LazyObjectBase)
                assert stateless_self.is_stateless
                obj = stateless_self
                handled_selref = True
            else:
                obj = lapject

            if nm in self.namespace:  # try to merge information
                sfobj = self.namespace[nm][0]
                sftags = self.namespace[nm][1]
                if sfobj is None:
                    sfobj = self
                if sfobj.ndim != obj.ndim:
                    raise ValueError("conflicting ndims")
                if sfobj.shape != obj.shape:
                    raise ValueError("conflicting shapes")
                if sfobj.inames != obj.inames:
                    raise ValueError("conflicting inames")

                # merge tags
                for tag, tval in tags.items():
                    if tag in self.namespace[nm][1]:
                        if tval != sftags[tag]:
                            raise ValueError(
                                    "conflicting tag values: %s" % tag)
                    else:
                        sftags[tag] = tval

            else:
                self.namespace[nm] = (obj.as_stateless(), tags)

    def _meld_env(self, env):
        """Merge with another env.
        """
        for key, val in env.items():
            if key in self.env:
                if self.env[key] is val:
                    pass  # same value
                elif val is None:
                    pass
                elif self.env[key] is None:
                    self.env[key] = val
                else:
                    raise ValueError(
                            "Trying to merge environments with conflicting "
                            "definitions of %s" % key)
            else:
                self.env[key] = val

    # }}} End namespace/env utils

    def _extract(self, member_name):
        """Given a name, returns the lapject from the namespace, with the state
        attached.
        """
        assert isinstance(member_name, str)
        if member_name not in self.namespace:
            raise ValueError("name %s not found" % member_name)
        if member_name == self.name:
            return self
        lapject = self.namespace[member_name][0].with_state(
                env=self.env.copy(), namespace=self.namespace.copy())
        lapject.namespace[self.name] = (
                self.as_stateless(),
                self.namespace[self.name][1].copy())
        lapject.namespace[member_name] = (
                None,
                self.namespace[member_name][1].copy())
        return lapject

    def _make_default_name(self):
        return make_default_name(self.__class__)

    def __str__(self):
        """Displays the value if available, otherwise display the
        type and name for user-defined names or the expression for
        the auto-generated names.
        """
        if (not self.is_stateless) and (self.value is not None):
            return str(self.value)
        if len(self.name) >= 2 and self.name[:2] == '__':
            # auto-generated name
            return str(self.expr)
        else:
            # user-specified name
            return ("%s('%s')" % (
                self.__class__.__name__,
                self.name,))

    def __repr__(self):
        """A more comprehensive view of the contents.
        """
        repr_dict = self._to_repr_dict()
        non_keys = []
        for key, val in repr_dict.items():
            if val is None:
                non_keys.append(key)
            elif isinstance(val, tuple):
                repr_dict[key] = '(' + ', '.join(str(v) for v in val) + ')'
            elif isinstance(val, dict):
                repr_dict[key] = '{' + ', '.join(
                        str(v) for v in val.keys()) + '}'
            else:
                repr_dict[key] = str(val)

        if not self.is_integral:
            non_keys.append('is_integral')

        # remove entries with no information
        for key in non_keys:
            repr_dict.pop(key)

        try:
            # sort_dicts introduced in Py3.8
            return pformat(repr_dict, depth=1, sort_dicts=False)
        except TypeError:
            return pformat(repr_dict, depth=1)

    def __eq__(self, other):
        """Two objects are considered equal if they share the same name.

        Also allows comparing with scalar constants, which amounts to
        comparing the value with other.
        """
        if np.isscalar(other):
            return self.value == other
        else:
            return self.name == other.name

    def __bool__(self):
        """If then value is not known, the boolean value is always false.
        (Think of it as a simplified trinary logic).
        """
        if self.value is None:
            return False

        return bool(self.value)

    @property
    def is_stateless(self):
        return self.env is None

    @property
    def has_state(self):
        return self.env is not None

    @property
    def arguments(self):
        """The input argument list.
        """
        if self.is_stateless:
            raise TypeError("stateless lapject has no arguments")
        return {
                key: val[0]
                for key, val in self.namespace.items()
                if val[1].get('is_argument', True) and (
                    key not in self.env)
                }

    @property
    def bound_arguments(self):
        """The arguments that are bound to data.
        """
        if self.is_stateless:
            raise TypeError("stateless lapject has no arguments")
        return {
                key: val[0]
                for key, val in self.namespace.items()
                if val[1].get('is_argument', True) and (
                    key in self.env)
                }

    @property
    def temporaries(self):
        """The temporaries (internal nodes of the computation graph).
        """
        if self.is_stateless:
            raise TypeError("stateless lapject has no temporaries")

        return {
                key: val[0]
                for key, val in self.namespace.items()
                if not val[1].get('is_argument', False)
                }

    @property
    def value(self):
        if self.is_stateless:
            raise TypeError(
                    "cannot ask for the value of a stateless object "
                    "(use _get_value() from the top-level object instead)")
        if self.name not in self.env.keys():
            return None
        return self.env[self.name]

    @value.setter
    def value(self, val):
        if self.is_stateless:
            raise TypeError("cannot set the value of a stateless object")
        self.env[self.name] = val

    def _to_repr_dict(self):
        return {'class': self.__class__,
                'name': self.name,
                'expr': self.expr,
                'namespace': self.namespace,
                'env': self.env}

# }}} End base lazy obj class

# {{{ array class


class Array(LazyObjectBase):
    """Lazily evaluated array. An array is a stateful (partial)
    closure consisting of three basic components:

    1) a formal argument list
    2) an expression
    3) an environment

    1) and 3) are stored in a single capture list, where the value
    None represents items in the argument list. Arguments can be
    instantiated and moved into its environment. This process
    is monotonic, that is, the environment cannot be modified by
    operations other than instantiation of the arguments.

    .. attribute:: ndim

        number of dimensions specified as an
        :class:`Unsigned`. At the moment, only concrete ndim is
        supported, i.e., ndim.value must be known.

    .. attribute:: shape

        overall shape of array expression.
        Tuple of :class:`str` with length equal to ``ndim``.
        Each component of the tuple is the name of a lazy object in the
        namespace.

    .. attribute:: inames

        index names for iterating over the array.
        Tuple of :class:`pymbolic.Variable`'s.

    .. attribute:: domain_expr

        set expression for constructing the loop domain. A set expression
        has leafs of :class:`lappy.core.primitives.PwAff` variables and
        integers. The domain expression is trivial if it equals to the set
        of indices of the array elements (no "hidden" axes).

    .. attribute:: dtype

        data type, either None or convertible to loopy type. Lappy
        does not allow implicit type casting.

    .. attribute:: is_integral

        a :class:`bool` indicating whether array elements are integers

    .. attribute:: integer_domain

        an ISL set if is_integral is True, otherwise None. The set represents
        the domain for the full array. It is used to express conditions like
        non-negative integers, multiples of two, etc.
    """
    _counter = 0
    _name_prefix = '__lappy_array_'

    # {{{ constructor

    def __init__(self, name=None, shape=None, domain_expr=None, **kwargs):
        """Constructor.
        """
        if 'expr' not in kwargs:
            kwargs['expr'] = None  # will make a default expr

        if name is not None:
            kwargs['name'] = name

        stateless = kwargs.pop('stateless', False)
        if not stateless:
            # name default env
            if 'env' not in kwargs or kwargs['env'] is None:
                kwargs['env'] = default_env()

        super(Array, self).__init__(**kwargs)

        self.domain_expr = domain_expr
        ndim = kwargs.pop("ndim", None)

        if ndim is None and shape is not None:
            # infer ndim from given shape
            shape = to_lappy_shape(shape)
            ndim = int(len(shape))

        if ndim is None:
            raise ValueError("ndim cannot be determined")

        try:
            ndim = int(ndim)
        except ValueError:
            raise ValueError('ndim must be a known non-negative integer')

        if ndim > 0:
            self.inames = kwargs.pop("inames", self._make_default_inames(ndim))
        else:
            self.inames = ()
        assert isinstance(self.inames, tuple)

        if self.expr is None:
            self.expr = self._make_default_expr(ndim)

        if shape is None:
            lapshape = self._make_default_shape(ndim)
            for s in lapshape:
                self._decl(s)
            self.shape = tuple(s.name for s in lapshape)
        else:
            if all(isinstance(s, str) for s in shape):
                self.shape = tuple(shape)
                for s in self.shape:
                    # make new symbols if not given by the namespace arg
                    if s not in self.namespace:
                        sap = to_lappy_unsigned(s)
                        self._decl(sap)
            else:
                lapshape = to_lappy_shape(shape)
                self.shape = tuple(s.name for s in lapshape)
                for s in lapshape:
                    self._meld_namespace(s.namespace, s.as_stateless())
                    self._meld_env(s.env)

        if self.domain_expr is None:
            self.domain_expr = self._make_default_domain_expr()

        self.dtype = kwargs.pop("dtype", None)
        self.is_integral = kwargs.pop("is_integral", False)
        if self.is_integral:
            self.integer_domain = kwargs.pop("integer_domain", None)
        else:
            self.integer_domain = None

    # }}} End constructor

    # {{{ copy constructors, with_xxx(), as_xxx()

    def __copy__(self):
        """Used if copy.copy is called on an array. Returns a copy of the array.

        Equivalent to ``a.copy(stateless=False)``.
        """
        return self.copy(stateless=False)

    def __deepcopy__(self):
        """Used if copy.deepcopy is called on an array.
        """
        raise NotImplementedError()

    def copy(self, stateless=False):
        """Returns a new copy of self, where the attributes undergo a shallow
        copy (expect for the value).

        Note: the copy operation does not make copies of the captured array data.
        """
        if self.integer_domain is None:
            cp_integer_domain = None
        else:
            cp_integer_domain = self.integer_domain.copy()

        if stateless or self.is_stateless:
            stateless = True
            env = None
        else:
            env = self.env.copy()

        nms = self.namespace.copy()

        return self.__class__(
                name=self.name, ndim=self.ndim,
                inames=self.inames,
                shape=self.shape,
                dtype=self.dtype,
                stateless=stateless,
                expr=self.expr, is_integral=self.is_integral,
                domain_expr=self.domain_expr,
                env=env,
                namespace=nms,
                preconditions=list(self.preconditions),
                integer_domain=cp_integer_domain,
                )

    def with_state(self, namespace=None, env=None):
        """Swap out the captured state.
        """
        sarr = self.as_stateless()
        sarr.env = env
        sarr.namespace = namespace
        return sarr

    def as_stateless(self):
        """Returns a stateless copy of self.
        """
        return self.copy(stateless=True)

    def with_name(self, name, rename_arguments=True):
        """Rename the array object. Returns a new (shallow) copy of self with
        the new name.

        :param rename_arguments: If true, all occurrences of the old name will
            be replaced. Otherwise, the new array takes the old array as an
            arguments and its value is assigned to the new name.
        """
        new_arr = self.copy()
        if name == self.name or name is None:
            # warnings.warn("name is unchanged, just making a copy")
            return new_arr

        if name in self.namespace:
            raise ValueError("Name %s is already taken" % name)

        if name in self.env:
            raise ValueError(
                    "Name %s is already taken by a captured variable" % name)

        if (self.name in self.env) and rename_arguments:
            new_arr.env[name] = new_arr.env.pop(self.name)

        # new self-reference
        new_arr.namespace[name] = new_arr.namespace.pop(self.name)

        # old self-reference
        if rename_arguments:
            new_arr.expr = pymbolic.substitute(new_arr.expr,
                    {var(self.name): var(name)})
        else:
            new_arr.namespace[self.name] = (
                    self.as_stateless(), self.namespace[self.name][1])
            new_arr.namespace[name] = (
                    None, self.namespace[self.name][1].copy())
            new_arr.namespace[name][1]['is_argument'] = False

        new_arr.name = name
        return new_arr

    def with_inames(self, inames):
        """Rename the array inames. Returns a new (shallow) copy of self with
        the new inames.
        """
        new_arr = self.copy()
        assert len(inames) == len(self.inames)

        for name in inames:
            if self._has_name(name.name) and (name not in self.inames):
                raise ValueError(
                        "name %s is already taken"
                        % name
                        )

        iname_map = {
                iname: new_iname
                for iname, new_iname in zip(self.inames, inames)}

        new_arr.inames = inames
        new_arr.expr = pymbolic.substitute(self.expr, iname_map)
        return new_arr

    def with_dtype(self, dtype, new_name=None):
        """Returns a copy of self with the specified dtype.
        """
        raise NotImplementedError()

    def with_shape_data(self, shape_data,
                        new_name=None, allow_complex_expr=False):
        """Returns a copy of the array with concrete shape. ``ndim`` is
        unchanged by assigning the shape data, meaning that the inputs,
        when not None, must be positive.

        :param shape_data: a tuple of shape data. Use None to skip setting
            certain axes.

        NOTE: if the shape has nontrivial expression (not just a reference
        to a name), lappy will not solve the equation for the "independent
        variables". The behavior in such cases is undefined. For example, if
        the shape has an expression ``(n * m) % p``, this method will assign
        a value for the whole expression, and the contraint among ``m, n, p``
        given by this expression is ignored and may cause unpredictable
        issues.
        """
        assert isinstance(shape_data, (list, tuple))
        assert self.ndim == len(shape_data)

        def is_trivial(expr):
            # TODO: better ways of spotting nontrivial exprs?
            return expr.__class__.init_arg_names == ('name',)

        assert allow_complex_expr or all(
                is_trivial(self._extract(s).expr) for s in self.shape)

        if new_name is None:
            new_name = 'bound%d_' % self.__class__._counter + self.name

        new_arr = self.with_name(new_name, False)

        for s, sv in zip(self.shape, shape_data):
            if s in new_arr.env and new_arr.env[s] != sv:
                raise ValueError('found pre-existing shape data')
            else:
                new_arr.env[s] = sv

        return new_arr

    def with_data(self, **kwargs):
        """Binds specific data to a slots in the arguments, resulting in a
        new (shallow) copy of self with the bound arguments catupred into its
        environment.
        """
        if 'new_name' in kwargs:
            raise ValueError("cannot rename while binding data")

        for key in kwargs.keys():
            if key not in self.namespace:
                raise ValueError("cannot bind an undefined name: %s" % key)

            if key in self.env.keys():
                # bounding cannot be undone
                # (since un-inference is not possible)
                raise ValueError("argument named %s is already bound"
                                 % key)

            if not self.namespace[key][1].get('is_argument', False):
                raise ValueError("trying to bind data to a non-argument %s"
                        % key)

        # make a copy
        new_arr = self.copy()

        for key, val in kwargs.items():

            if hasattr(val, 'dtype'):
                if key == self.name:
                    new_arr.dtype = val.dtype
                else:
                    new_arr.namespace[key][0].dtype = val.dtype

            if hasattr(val, 'shape'):
                new_arr._set_shape_values(val.shape, key)

            if hasattr(val, 'ndim'):
                if key == self.name:
                    assert new_arr.ndim == val.ndim
                    assert len(new_arr.shape) == val.ndim
                else:
                    assert new_arr.namespace[key][0].ndim == val.ndim
                    assert len(val.shape) == val.ndim

            new_arr.env[key] = val  # actual data

        return new_arr

    # }}} End copy constructors, with_xxx(), as_xxx()

    # {{{ public (numpy-compliant) api

    @property
    def ndim(self):
        return len(self.shape)

    @property
    def size(self):
        return self._shadow_size()

    def itemsize(self):
        """TODO: dtype expression
        """
        if self.dtype is None:
            # use numpy defaults
            return np.dtype(self.dtype).itemsize
        else:
            return np.dtype(self.dtype).itemsize

    def nbytes(self):
        return self.size * self.itemsize

    def __len__(self, order='C'):
        if self.ndim == 0:
            return 0

        if order == 'C':
            return self.shape[0]
        elif order == 'F':
            return self.shape[-1]
        else:
            raise ValueError(
                    "order must be either 'C' or 'F' (got %s)" % str(order))

    # {{{ basic ops

    def reshape(self, newshape, order='C', name=None, inames=None):
        """Reshape.
        """
        from lappy.core.basic_ops import reshape
        return reshape(
                self, newshape=newshape,
                order=order, name=name, inames=inames)

    def transpose(self, axes=None, name=None):
        """Transpose.
        """
        from lappy.core.basic_ops import transpose
        return transpose(self, axes, name)

    T = transpose

    def swapaxes(self, axis1, axis2):
        """Return a view of the array with axis1 and axis2 interchanged.
        """
        raise NotImplementedError()

    def squeeze(self):
        """Remove single-dimensional entries from the shape of a.
        """
        raise NotImplementedError()

    def repeat(self):
        """Repeat elements of an array.
        """
        raise NotImplementedError()

    def fill(self):
        raise NotImplementedError()

    def astype(self):
        raise NotImplementedError()

    def resize(self, new_shape, order='C'):
        """Change shape and size of array.
        Shrinking: array is flattened, resized, and reshaped.
        Enlarging: as above, with missing entries filled with zeros.
        """
        raise NotImplementedError()

    def flatten(self):
        raise NotImplementedError()

    ravel = flatten  # unlike number, the two are equivalent in lappy

    # }}} End basic ops

    # {{{ data io

    def dump(self, with_env=True):
        """Dump the full lazy array object into a file.
        """
        raise NotImplementedError()

    def dumps(self, with_env=True):
        """Dump the full lazy array object into a string.
        """
        raise NotImplementedError()

    # }}} End data io

    # {{{ getter/setter

    def item(self, *args):
        """Copy an element of an array to a standard Python scalar
        and return it.
        """
        raise NotImplementedError()

    def itemset(self, *args):
        """Insert scalar into an array
        (scalar is cast to array's dtype, if possible).
        """
        raise NotImplementedError()

    def take(self):
        """Return an array formed from the elements of a at the
        given indices.
        """
        raise NotImplementedError()

    def put(self, indices, values, mode='raise'):
        """Set a.flat[n] = values[n] for all n in indices.
        """
        raise NotImplementedError()

    def __getitem__(self, indices):
        """Returns a new array by sub-indexing the current array.
        """
        if isinstance(indices, str):
            # structured dtype support
            raise NotImplementedError()

        if not isinstance(indices, tuple):
            # advanced indexing with an array
            assert isinstance(indices, Array)
            assert indices.ndim == self.ndim
            indices = (indices, )
        else:
            # indexing / mixture of indexing and masking
            assert isinstance(indices, tuple)

        from lappy.core.basic_ops import SubArrayFactory
        arr_fac = SubArrayFactory(self, indices)
        sub_arr = arr_fac()
        return sub_arr

    def __setitem__(self, index, value):
        """Set item described by index.
        """
        raise NotImplementedError()

    def __delitem__(self, key):
        """Delete self[key].
        """
        raise NotImplementedError()

    def __iter__(self):
        """Iterator support if ndim and shape are all fixed.
        Its behavior mimics numpy.ndarray.__iter__()
        """
        raise NotImplementedError()

    def flat(self):
        """Flat iterator support if ndim and shape are all fixed.
        Its behavior mimics numpy.ndarray.nditer()
        """
        raise NotImplementedError()

    # }}} End getter/setter

    # {{{ numpy protocols

    def __array__(self):
        """(For numpy’s dispatch). When converting to a numpy array with
        ``numpy.array`` or ``numpy.asarray``, the lazy array is evaluated
        and the result is returned.
        """
        res = self.eval()
        if isinstance(res, np.ndarray):
            return res
        else:
            return res.get()

    @property
    def __array_interface__(self):
        """The array interface (array protocol) for data buffer access.
        """
        if self.is_stateless:
            raise ValueError("array value is unknown")
        else:
            raise NotImplementedError()

    @classmethod
    def __array_function__(cls, func, types, args, kwargs):
        """Array function protocol.
           https://numpy.org/neps/nep-0018-array-function-protocol.html
        """
        raise NotImplementedError()

    @classmethod
    def __array_ufunc__(cls, ufunc, method, *inputs, **kwargs):
        """Array ufunc protocol.
           https://docs.scipy.org/doc/numpy/reference/ufuncs.html
        """
        raise NotImplementedError()

    # }}} End numpy protocols

    # {{{ arithmetics

    def __add__(self, other):
        if not isinstance(other, Array):
            other_arr = to_lappy_array(other)
        else:
            other_arr = other
        from lappy.core.ufuncs import add
        return add(self, other_arr)

    def __radd__(self, other):
        if not isinstance(other, Array):
            other_arr = to_lappy_array(other)
        else:
            other_arr = other
        from lappy.core.ufuncs import add
        return add(other_arr, self)

    def __sub__(self, other):
        if not isinstance(other, Array):
            other_arr = to_lappy_array(other)
        else:
            other_arr = other
        from lappy.core.ufuncs import subtract
        return subtract(self, other_arr)

    def __rsub__(self, other):
        if not isinstance(other, Array):
            other_arr = to_lappy_array(other)
        else:
            other_arr = other
        from lappy.core.ufuncs import subtract
        return subtract(other_arr, self)

    def __mul__(self, other):
        if not isinstance(other, Array):
            other_arr = to_lappy_array(other)
        else:
            other_arr = other
        from lappy.core.ufuncs import multiply
        return multiply(self, other_arr)

    def __rmul__(self, other):
        if not isinstance(other, Array):
            other_arr = to_lappy_array(other)
        else:
            other_arr = other
        from lappy.core.ufuncs import multiply
        return multiply(other_arr, self)

    def __div__(self, other):
        if not isinstance(other, Array):
            other_arr = to_lappy_array(other)
        else:
            other_arr = other
        from lappy.core.ufuncs import divide
        return divide(self, other_arr)

    __truediv__ = __div__

    def __rtruediv__(self, other):
        if not isinstance(other, Array):
            other_arr = to_lappy_array(other)
        else:
            other_arr = other
        from lappy.core.ufuncs import divide
        return divide(other_arr, self)

    def __divmod__(self, value):
        raise NotImplementedError()

    def __rdivmod__(self, value):
        raise NotImplementedError()

    def __pow__(self, other):
        if not isinstance(other, Array):
            other_arr = to_lappy_array(other)
        else:
            other_arr = other
        from lappy.core.ufuncs import power
        return power(self, other_arr)

    def __rpow__(self, other):
        if not isinstance(other, Array):
            other_arr = to_lappy_array(other)
        else:
            other_arr = other
        from lappy.core.ufuncs import power
        return power(other_arr, self)

    def __floordiv__(self, other):
        if not isinstance(other, Array):
            other_arr = to_lappy_array(other)
        else:
            other_arr = other
        from lappy.core.ufuncs import floordiv
        return floordiv(self, other_arr)

    def __rfloordiv__(self, other):
        if not isinstance(other, Array):
            other_arr = to_lappy_array(other)
        else:
            other_arr = other
        from lappy.core.ufuncs import floordiv
        return floordiv(other_arr, self)

    def __mod__(self, other):
        raise NotImplementedError()

    def __rmod__(self, other):
        raise NotImplementedError()

    def __iadd__(self, value):
        raise NotImplementedError()

    def __isub__(self, value):
        raise NotImplementedError()

    def __imul__(self, value):
        raise NotImplementedError()

    def __idiv__(self, value):
        raise NotImplementedError()

    def __itruediv__(self, value):
        raise NotImplementedError()

    def __ipow__(self, value):
        raise NotImplementedError()

    def __ifloordiv__(self, value):
        raise NotImplementedError()

    def __imod__(self, value):
        raise NotImplementedError()

    def __matmul__(self, value):
        raise NotImplementedError()

    def __rmatmul__(self, value):
        raise NotImplementedError()

    def __imatmul__(self, value):
        raise NotImplementedError()

    def __lshift__(self):
        raise NotImplementedError()

    def __rlshift__(self):
        raise NotImplementedError()

    def __ilshift__(self):
        raise NotImplementedError()

    def __rshift__(self):
        raise NotImplementedError()

    def __rrshift__(self):
        raise NotImplementedError()

    def __irshift__(self):
        raise NotImplementedError()

    # }}} End arithmetics

    # {{{ comparisons

    def __eq__(self, other):
        """Test for equality. Returns ``True`` if two Arrays have
        the same name. Returns a new Array with comparison expression
        otherwise.
        """
        if not isinstance(other, Array):
            other_arr = to_lappy_array(other)
        else:
            other_arr = other

        if self.name == other_arr.name:
            return True
        else:
            from lappy.core.ufuncs import equal
            return equal(self, other_arr)

    def __ne__(self, other):
        return not self == other

    def __le__(self, other):
        if not isinstance(other, Array):
            other_arr = to_lappy_array(other)
        else:
            other_arr = other
        from lappy.core.ufuncs import less_equal
        return less_equal(self, other_arr)

    def __lt__(self, other):
        if not isinstance(other, Array):
            other_arr = to_lappy_array(other)
        else:
            other_arr = other
        from lappy.core.ufuncs import less
        return less(self, other_arr)

    def __ge__(self, other):
        if not isinstance(other, Array):
            other_arr = to_lappy_array(other)
        else:
            other_arr = other
        from lappy.core.ufuncs import greater_equal
        return greater_equal(self, other_arr)

    def __gt__(self, other):
        if not isinstance(other, Array):
            other_arr = to_lappy_array(other)
        else:
            other_arr = other
        from lappy.core.ufuncs import greater
        return greater(self, other_arr)

    # }}} End comparisons

    # {{{ logical ops

    def __and__(self, value):
        raise NotImplementedError()

    def __rand__(self, value):
        raise NotImplementedError()

    def __or__(self, value):
        raise NotImplementedError()

    def __ror__(self, value):
        raise NotImplementedError()

    def __xor__(self, value):
        raise NotImplementedError()

    def __rxor__(self, value):
        raise NotImplementedError()

    def __iand__(self, value):
        raise NotImplementedError()

    def __ior__(self, value):
        raise NotImplementedError()

    def __ixor__(self, value):
        raise NotImplementedError()

    def __contains__(self, key):
        raise NotImplementedError()

    def __invert__(self):
        raise NotImplementedError()

    def all(self, axis=None, out=None, keepdims=False):
        raise NotImplementedError()

    def any(self, axis=None, out=None, keepdims=False):
        raise NotImplementedError()

    # }}} End logical ops

    # {{{ other maths

    def __abs__(self):
        """|self|
        """
        from lappy.core.ufuncs import absolute
        return absolute(self)

    def __pos__(self):
        """+self
        """
        raise NotImplementedError()

    def __neg__(self):
        """-self
        """
        from lappy.core.ufuncs import negative
        return negative(self)

    def __index__(self):
        """Called to implement operator.index(), and whenever Python needs to
        losslessly convert the numeric object to an integer object (such as in
        slicing, or in the built-in bin(), hex() and oct() functions).
        """
        if self.is_integral:
            raise NotImplementedError()
        else:
            raise ValueError()

    def __complex__(self):
        """Convert size-1 arrays to Python scalars.
        """
        raise NotImplementedError()

    def __float__(self):
        """Convert size-1 arrays to Python scalars.
        """
        raise NotImplementedError()

    def __int__(self):
        """Convert size-1 arrays to Python scalars.
        """
        raise NotImplementedError()

    def round(self):
        """Return a with each element rounded to the given number of
        decimals.
        """
        raise NotImplementedError()

    def conjugate(self):
        raise NotImplementedError()

    conj = conjugate

    def real(self):
        raise NotImplementedError()

    def imag(self):
        raise NotImplementedError()

    def max(self, axis=None, out=None, keepdims=False, initial=None, where=True):
        raise NotImplementedError()

    def min(self):
        raise NotImplementedError()

    def sort(self):
        raise NotImplementedError()

    def searchsorted(self):
        """Find indices where elements of v should be inserted in a
        to maintain order.
        """
        raise NotImplementedError()

    def mean(self):
        raise NotImplementedError()

    def sum(self):
        raise NotImplementedError()

    def var(self):
        raise NotImplementedError()

    def std(self):
        raise NotImplementedError()

    def nonzero(self):
        raise NotImplementedError()

    def partition(self):
        raise NotImplementedError()

    def prod(self):
        """Return the product of the array elements over the given axis.
        """
        raise NotImplementedError()

    product = prod

    def ptp(self):
        """Peak to peak (maximum - minimum) value along a given axis.
        """
        raise NotImplementedError()

    def anom(self):
        """Compute the anomalies (deviations from the arithmetic mean)
        along the given axis.
        """
        raise NotImplementedError()

    def argmax(self):
        raise NotImplementedError()

    def argmin(self):
        raise NotImplementedError()

    def argpartition(self):
        raise NotImplementedError()

    def argsort(self):
        raise NotImplementedError()

    def clip(self):
        """Clip (limit) the values in an array.
        """
        raise NotImplementedError()

    def cumprod(self):
        """Return the cumulative product of elements along a given axis.
        """
        raise NotImplementedError()

    def cumsum(self):
        """Return the cumulative sum of the elements along the given axis.
        """
        raise NotImplementedError()

    def diagonal(self):
        raise NotImplementedError()

    def trace(self):
        raise NotImplementedError()

    def dot(self):
        raise NotImplementedError()

    # }}} End other maths

    # }}} End public (numpy-compliant) api

    # {{{ extended public api

    def pin(self, name=None, cse=False, insert_barrier=False):
        """Declare that the array shall be treated as a temporary.
        """
        if name is None:
            name = self.name

        if cse:
            self.namespace[name][1]['is_cse'] = True

        if insert_barrier:
            self.namespace[name][1]['has_barrier'] = True

        self.namespace[name][1]['is_temporary'] = True

    # }}} End extended public api

    # {{{ private api

    def _has_trivial_expr(self):
        """Whether the expression is more complex than a leaf node.
        """
        # An array
        if isinstance(self.expr, Subscript):
            if self.expr.aggregate.__class__.init_arg_names == ('name',):
                for idx in self.expr.index_tuple:
                    if self.expr.aggregate.__class__.init_arg_names == ('name',):
                        pass
                    else:
                        return False
                return True

        # A scalar
        return self.expr.__class__.init_arg_names == ('name',)

    def _has_trivial_domain_expr(self):
        """Whenever the loop domain equals to the index domain.
        """
        return (self.domain_expr is None) or (
                self.domain_expr == self._make_default_domain_expr())

    def _get_shape_vals(self, axis=None):
        """Returns the shape values where available, None otherwise.
        """
        return tuple(self.env[s.name] if s.name in self.env else None
                     for s in self.shape)

    def _set_shape_values(self, shape, name=None):
        """Instantiate shape of a namespace member with concrete values.
        """
        for s in tuple(shape):
            assert int(s) == s
            assert s >= 0

        if name is None or name == self.name:
            sym_shape = self.shape
        elif name in self.namespace:
            sym_shape = self._extract(name).shape
        else:
            raise ValueError()

        for s, sym_s_name in zip(shape, sym_shape):
            sym_s = self._extract(sym_s_name)
            if sym_s.name in self.env:
                if self.env[sym_s_name] != s:
                    warnings.warn(
                            "captured shape value for %s is overwritten "
                            "(%s --> %s)" % (
                                sym_s.name,
                                str(self.env[sym_s.name]), str(s)))
            self.env[sym_s_name] = s

    def _get_value(self, name=None):
        """Try to get the value of a captured variable. Returns None
        if the process fails.
        """
        if name is None:
            return self.value

        if self.is_stateless:
            return None

        if name in self.env:
            return self.env[name]
        else:
            return None

    def _get_shape_vals_or_strs(self):
        """Returns the shape as a tuple of ints if the value is known, or
        strings of names otherwise.
        """
        return tuple(
                self.env[s] if s in self.env else s for s in self.shape)

    def _make_default_expr(self, *args):
        """The default expression is the array it self.

        :param ndim: optional, used when the array shape is not set.
        """
        if hasattr(self, 'shape'):
            ndim = self.ndim
        else:
            ndim, = args

        sym_arr = var(self.name)
        if ndim > 0:
            # array
            sym_indices = self._make_axis_indices(*args)
            expr = Subscript(sym_arr, index=sym_indices)
        else:
            # scalar
            expr = sym_arr
        return expr

    def _make_axis_indices(self, *args):
        """Make the inames as expressions based of array name and ndim

        :param ndim: optional, used when the array shape is not set yet.
        """
        # zero-dimensional, aka a scalar
        if hasattr(self, 'shape'):
            ndim = self.ndim
        else:
            ndim, = args

        if ndim == 0:
            return ()

        # ndim is None (up to further inference)
        if ndim is None:
            # return Lookup(Variable(self.name), "inames")
            return var('__%s_inames' % self.name)

        # constant positive dimensions
        assert ndim > 0
        # shape = Lookup(Variable(self.name), "inames")
        # return tuple(Subscript(shape, d) for d in range(self.ndim))
        return tuple(var('__%s_inames_%d' % (self.name, d))
                     for d in range(ndim))

    def _to_repr_dict(self):
        repr_dict = super(Array, self)._to_repr_dict()
        repr_dict.update({
            'ndim': self.ndim,
            'inames': self.inames,
            'domain': self.domain_expr,
            'shape': self.shape,
            'dtype': self.dtype,
            'is_integral': self.is_integral,
            'integer_domain': self.integer_domain})
        return repr_dict

    def _shadow_size(self, axes=None):
        """When axes is None, computes the full size. Otherwise computes
        the size of the projected array on the given axes.

        If the shasow size of not computable, returns an expression for it.
        """
        if axes is None:
            axes = list(range(self.ndim))
        else:
            # so that generators can be understood
            axes = list(axes)
        shape_vars = tuple(var(self.shape[ax]) for ax in axes)
        size_expr = Product(shape_vars)
        try:
            return evaluate(size_expr, self.env)
        except UnknownVariableError:
            return size_expr

    @property
    def _is_leaf(self):
        """Return True if the array expression is a flat-out read.
        """
        return self.expr == self._make_default_expr()

    def _make_default_inames(self, *args):
        """Make the default inames, simply as lookup expressions.
        """
        return self._make_axis_indices(*args)

    def _make_default_domain_expr(self, *args):
        """Make the default domain_expr representing the index domain.
        Depends on ``self.inames`` and ``self.shape``.
        """
        if self.ndim == 0:
            sv = SetVar(self.name + '_dummy_iname')
            return (sv.lt(1)).and_(sv.ge(0))

        # from Variable to PwAff:
        sns = [SetVar(iname.name) for iname in self.inames]
        bounds = [SetParam(shp) for shp in self.shape]

        dexpr_components = [
                (sv.lt(upper_bound)).and_(sv.ge(0))
                for sv, upper_bound in zip(sns, bounds)]

        dexpr = dexpr_components[0]
        for dc in dexpr_components[1:]:
            dexpr = dexpr.and_(dc)
        return dexpr

    def _make_default_shape(self, ndim):
        """Make a default shape based of name and ndim.
        Returns the shape tuple of ``Unsigned``.
        """
        # zero-dimensional, aka a scalar
        if ndim == 0:
            return ()

        # symbolic-dimensions
        if isinstance(ndim, Unsigned):
            assert ndim.ndim == 0
            return Lookup(Variable(self.name), "shape")

        # constant positive dimensions
        assert ndim > 0
        if len(self.name) > 1 and self.name[:2] == '__':
            name_prefix = ''
        else:
            name_prefix = '__'
        names = [name_prefix + self.name + '_shape_%d' % d
                 for d in range(ndim)]
        return tuple(
                Unsigned(
                    name=names[d],
                    expr=var(names[d]),
                    env=None, namespace=None)
                for d in range(ndim))

    @property
    def _shape_str(self):
        """A shape description string used for loopy kernel construction.
        """
        return ', '.join(self.shape)

    @property
    def _shape_expr(self):
        """Values for the shape (if not None), otherwise expressions.
        """
        return tuple(
                self.env[s] if s in self.env else self._extract(s).expr
                for s in self.shape)

    # }}} End private api

# }}} End array class

# {{{ special subtypes of array

# for more readable names and handy constructors


class Scalar(Array):
    """Scalar.
    """
    _counter = 0
    _name_prefix = '__lappy_scalar_'

    def __init__(self, name=None, **kwargs):
        if name is not None:
            kwargs['name'] = name
        kwargs['shape'] = ()
        kwargs['ndim'] = 0
        super(Scalar, self).__init__(**kwargs)

    def __getitem__(self, indices):
        raise TypeError("cannot sub-index a scalar")


class Int(Scalar):
    """Integer (index type).
    """
    _counter = 0
    _name_prefix = '__lappy_int_'

    def __init__(self, name=None, **kwargs):
        if name is not None:
            kwargs['name'] = name

        super(Int, self).__init__(**kwargs)
        self.is_integral = True

        assert self.shape == ()
        assert self.ndim == 0


class Unsigned(Int):
    """Non-negative integer (size type).
    """
    _counter = 0
    _name_prefix = '__lappy_unsigned_'

    def __init__(self, name=None, **kwargs):
        if name is not None:
            kwargs['name'] = name
        super(Unsigned, self).__init__(**kwargs)
        self.integer_domain = isl.BasicSet.read_from_str(
            isl.DEFAULT_CONTEXT,
            "{ [%s] : %s >= 0 }" % ((self.name, ) * 2))

        assert self.is_integral

# }}} End special subtypes of array

# {{{ convert array-like variables to lappy arrays


def to_lappy_array(arr_like, name=None, base_env=None):
    """Do nothing if the array is already a lazy array.
    Invoke a copy operation if it is a View.
    Make a lazy array with captured values for actual
    arrays (such as numpy, opencl, and cuda arrays).
    """
    if base_env is None:
        base_env = default_env()

    if isinstance(arr_like, Array):
        return arr_like

    if np.isscalar(arr_like):
        try:
            dtype = np.dtype(type(arr_like)).type
        except TypeError:
            dtype = None

        # integer type takes priority over general scalar type
        if int(arr_like) == arr_like:
            arr_class = Int
        else:
            arr_class = Scalar

        arr = arr_class(name=name, dtype=dtype, env=base_env, value=arr_like)
        arr.env[arr.name] = arr_like

        return arr

    if isinstance(arr_like, np.ndarray):
        arr = Array(
            name=name, dtype=arr_like.dtype,
            shape=arr_like.shape,
            ndim=arr_like.ndim,
            arguments=dict(),
            bound_arguments={name: None},
            env=base_env)
        arr.env[arr.name] = arr_like
        return arr

    # opencl / cuda arrays
    if str(type(arr_like)) == "<class 'pyopencl.array.Array'>":
        raise NotImplementedError()

    if str(type(arr_like)) == "<class 'pycuda.gpuarray.GPUArray'>":
        raise NotImplementedError()

    raise ValueError("Cannot convert the input to a Lappy Array.")


def to_lappy_scalar(scalar_like, name=None, base_env=None, dtype=np.float64):
    """Do nothing if the array is already an :class:`Scalar`.
    Make an :class:`Scalar` with captured values for an actual number.
    """
    if base_env is None:
        base_env = default_env()

    if scalar_like is None:
        return Scalar(name=name, env=base_env, dtype=dtype)

    if np.isscalar(scalar_like):
        try:
            scalar_like = float(scalar_like)
            return Scalar(value=scalar_like, env=base_env, dtype=dtype)
        except ValueError:
            # a string of name, not value
            assert isinstance(scalar_like, str)
            return Scalar(name=scalar_like, env=base_env, dtype=dtype)

    if isinstance(scalar_like, Array):
        assert scalar_like.ndim == 0
        assert scalar_like.shape == ()

        if not isinstance(scalar_like, Scalar):
            scalar_like = Scalar(
                    name=scalar_like.name, value=scalar_like.value,
                    dtype=dtype,
                    env=scalar_like.env.copy(),
                    namespace=scalar_like.namespace.copy())

        return scalar_like

    if isinstance(scalar_like, pymbolic.primitives.Expression):
        return Scalar(expr=scalar_like, dtype=dtype, env=base_env)

    raise ValueError("Cannot convert the input to a Lappy Scalar.")


def to_lappy_unsigned(unsigned_like, name=None, base_env=None, dtype=np.int32):
    """Do nothing if the array is already an :class:`Unsigned`.
    Make an :class:`Unsigned` with captured values for an actual number.
    """
    if base_env is None:
        base_env = default_env()

    if name is None:
        name = make_default_name(Unsigned)

    if unsigned_like is None:
        return Unsigned(
                name=name, env=base_env,
                namespace={name: (None, {'is_argument': True})},
                dtype=dtype)

    if np.isscalar(unsigned_like):
        try:
            unsigned_like = int(unsigned_like)
        except ValueError:
            # a string of name, not value
            return Unsigned(
                    name=unsigned_like, env=base_env,
                    namespace={
                        unsigned_like: (None, {'is_argument': True})},
                    dtype=dtype)

        if abs(int(unsigned_like)) - unsigned_like == 0:
            lunsigned = Unsigned(
                    name=name, value=unsigned_like, env=base_env,
                    namespace={name: (None, {'is_argument': True})},
                    dtype=dtype)
            lunsigned.env[lunsigned.name] = unsigned_like
            return lunsigned
        else:
            raise ValueError(
                    "%s is not a non-negative integer" % str(unsigned_like))

    if isinstance(unsigned_like, Array):
        assert unsigned_like.ndim == 0
        assert unsigned_like.shape == ()
        assert unsigned_like.is_integral

        if not isinstance(unsigned_like, Unsigned):
            unsigned_like = Unsigned(
                    name=unsigned_like.name,
                    value=unsigned_like.value,
                    dtype=dtype,
                    env=unsigned_like.env.copy(),
                    namespace=unsigned_like.namespace.copy(),
                    expr=unsigned_like.expr,
                    arguments=unsigned_like.arguments.copy(),
                    bound_arguments=unsigned_like.bound_arguments.copy(),
                    temporaries=unsigned_like.temporaries.copy(),
                    preconditions=unsigned_like.preconditions
                    )

        return unsigned_like

    if isinstance(unsigned_like, pymbolic.primitives.Expression):
        return Unsigned(expr=unsigned_like, dtype=dtype, env=base_env)

    raise ValueError("Cannot convert the input to a Lappy Unsigned.")


# }}} End convert array-like variables to lappy arrays

# {{{ digest shape specifiers


def to_lappy_shape(shape):
    """Accepted shape specified in one of the following forms:

    - Tuple of nonnegative integers, strings, expressions or
      Unsigned objects.
    - Comma/space-separated string.

    """
    if shape is None:
        return tuple()

    if isinstance(shape, str):
        components = []
        parts = shape.split(' ')
        for p in parts:
            components.extend(
                    [pp for pp in p.split(',') if pp]
                    )
        for i, c in enumerate(components):
            try:
                int_c = int(c)
                if not int_c == abs(int_c):
                    raise ValueError("cannot use %s as a shape parameter" % str(c))
                components[i] = to_lappy_unsigned(int(c))
            except ValueError:
                components[i] = to_lappy_unsigned(c)
        return tuple(components)

    assert isinstance(shape, (tuple, list))
    components = list(shape)
    for i, c in enumerate(shape):
        if isinstance(c, Array):
            components[i] = c
        else:
            components[i] = to_lappy_unsigned(c, name=None)

    return tuple(components)


def isscalar(obj):
    """Like np.isscalar, but also works for lazy objects.
    """
    if np.isscalar(obj):
        return True
    else:
        return isinstance(obj, Int)

# }}} End digest shape specifiers

# {{{ misc utils


def get_internal_name_prefix(name):
    """If the name is already an internal name (starting with '__'), return '';
    otherwise return '__'.
    """
    if len(name) > 1 and name[:2] == '__':
        name_prefix = ''
    else:
        name_prefix = '__'
    return name_prefix


def make_default_name(obj_class):
    """Make a default name for the lazy object class.
    """
    name = '%s%d' % (obj_class._name_prefix, obj_class._counter)
    obj_class._counter += 1
    return name

# }}} End misc utils
