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

import warnings
import functools
from traceback import format_list, extract_stack

import islpy as isl
import numpy as np
import loopy as lp
import pyopencl as cl

from pymbolic import var, substitute, evaluate
from pymbolic.mapper import CombineMapper, Mapper
from pymbolic.mapper.evaluator import UnknownVariableError

from lappy.core.array import Array
from lappy.core.mapper import SetVariableCollector, SetParameterCollector
from lappy.core.primitives import EMPTY_SET, UNIVERSE_SET

from lappy.eval import Closure


class PreconditionNotMetError(Exception):
    pass

# {{{ expression mappers


class TemporaryCollector(CombineMapper):
    """Find temporaries in the expression.
    Note that it is possible that a temporary appears multiple
    times within different inames.

    .. attribute:: arr

      reference to the lazy array object.
    """
    def __init__(self, arr):
        self.arr = arr

    def combine(self, values):
        import operator
        return functools.reduce(operator.add, values, list())

    def map_constant(self, expr):
        if hasattr(expr, 'name'):
            if expr.name in self.arr.namespace:
                tags = self.arr.namespace[expr.name][1]
                is_temp = tags.get('is_temporary', False)
                if is_temp:
                    return [expr.name, ]

        return list()

    map_algebraic_leaf = map_constant

# }}} End expression mappers

# {{{ loop domain compiler


class LoopDomainCompiler(Mapper):
    """Compiles a set expression in to an ISL set.
    """
    def map_constant(self, expr, var_dict):
        if expr == 0:
            return var_dict[0]
        return expr

    def map_set_variable(self, expr, var_dict):
        return var_dict[expr.name]

    def map_set_parameter(self, expr, var_dict):
        return var_dict[expr.name]

    def map_sum(self, expr, var_dict):
        res = var_dict[0]
        for c in expr.children:
            res += self.rec(c, var_dict)
        return res

    def map_pwaff_comparison(self, expr, var_dict):
        lhs = self.rec(expr.left, var_dict)
        rhs = self.rec(expr.right, var_dict)
        op = expr.operator

        print(type(lhs), type(rhs))

        if isinstance(lhs, int) and isinstance(rhs, int):
            exec('valid = (%s %s %s)' % (str(lhs), str(op), str(rhs)))
            if valid:  # noqa: F821
                return 1  # stands for the whole set
            else:
                return 0  # stands for the empty set

        if isinstance(lhs, int) and isinstance(rhs, isl.PwAff):
            lhs, rhs = rhs, lhs

        if isinstance(lhs, isl.PwAff) and isinstance(rhs, int):
            lhs = lhs - rhs
            rhs = var_dict[0]

        if isinstance(lhs, isl.PwAff) and isinstance(rhs, isl.PwAff):
            if op == '==':
                return lhs.eq_set(rhs)
            if op == '!=':
                return lhs.ne_set(rhs)
            if op == '<=':
                return lhs.le_set(rhs)
            if op == '<':
                return lhs.lt_set(rhs)
            if op == '>=':
                return lhs.ge_set(rhs)
            if op == '>':
                return lhs.gt_set(rhs)
            raise ValueError('unknown operator "%s"' % str(op))

        else:
            raise ValueError('cannot compile operator "%s" (lhs=%s, rhs=%s)'
                    % (op, str(expr.left), str(expr.right)))

    def map_pwaff_sum(self, expr, var_dict):
        """Mapper for sum of pwaffs.
        """
        return sum([self.rec(child, var_dict) for child in expr.children], 0)

    def map_pwaff_product(self, expr, var_dict):
        """Mapper for product of pwaffs.
        """
        res = 1
        for rc in [self.rec(child, var_dict) for child in expr.children]:
            res *= rc
        return res

    def map_pwaff_floor_div(self, expr, var_dict):
        return (self.rec(expr.numerator, var_dict)
                // self.rec(expr.denominator, var_dict))

    def map_pwaff_remainder(self, expr, var_dict):
        return (self.rec(expr.numerator, var_dict)
                % self.rec(expr.denominator, var_dict))

    def map_set_union(self, expr, var_dict):
        """Mapper for set union.

        Singular sets (empty set and its complement) are represented with ints.
        """
        children = [self.rec(child, var_dict) for child in expr.children]

        for c in children:
            if isinstance(c, int) and c == UNIVERSE_SET:
                return UNIVERSE_SET

        children = [c for c in children if not isinstance(c, int)]

        if len(children) > 0:
            res = children[0]
        else:
            res = UNIVERSE_SET

        for c in children:
            assert isinstance(res, isl.Set) and isinstance(c, isl.Set)
            res = res | c

        return res

    def map_set_intersection(self, expr, var_dict):
        """Mapper for set intersection.

        Singular sets (empty set and its complement) are represented with ints.
        """
        children = [self.rec(child, var_dict) for child in expr.children]

        for c in children:
            if isinstance(c, int) and c == EMPTY_SET:
                return EMPTY_SET

        children = [c for c in children if not isinstance(c, int)]

        if len(children) > 0:
            res = children[0]
        else:
            res = UNIVERSE_SET

        for c in children:
            assert isinstance(res, isl.Set) and isinstance(c, isl.Set)
            res = res & c

        return res

    def __call__(self, expr):
        """Returns a list of basic sets representing the loop domain.

        The variables and parameter are lexicographically ordered.
        """
        var = sorted(list(SetVariableCollector()(expr)))
        param = sorted(list(SetParameterCollector()(expr)))
        var_dict = isl.make_zero_and_vars(var, param)

        domain_pre = super(LoopDomainCompiler, self).__call__(expr, var_dict)
        if isinstance(domain_pre, isl.PwAff):
            # unconstrained domain
            raise ValueError("unconstrained (thus unbounded) loop domain")

        if isinstance(domain_pre, isl.Set):
            domain = domain_pre.coalesce().get_basic_sets()
        else:
            raise RuntimeError()

        return domain

# }}} End loop domain compiler

# {{{ compiler


class Compiler(object):
    def __init__(self, check_preconditions=False):
        self.check_preconditions = check_preconditions
        self._counter = 0

    def __call__(self, *args):
        """When given a few of :class:`Array` objects, make one loopy
        kernel that evaluates all of them.
        """
        if len(args) > 1:
            raise NotImplementedError()

        out_names = []
        for arr in args:
            assert isinstance(arr, Array)
            out_names.append(arr.name)

        knl, context = self.compile(*args)
        data_map = self._get_data_mapping(arr, knl)
        context.update(data_map)

        # FIXME: using with_name breaks precondition checking.
        # Possible Solution: keep track of name changes
        if self.check_preconditions:
            self._check_preconditions(arr.preconditions, context)

        return Closure(out_names, knl, data_map)

    def _check_preconditions(self, preconditions, context):
        """Call checkers in the list of preconditions.

        :param context: a dict which is passed to all checkers.
        """
        failed_checks = []
        for checker in preconditions:
            try:
                res = checker(context)
                if res is not None:
                    if isinstance(res, bool):
                        if res:
                            pass
                        else:
                            raise PreconditionNotMetError(
                                    "precondition checker failed: %s"
                                    % str(checker))
                    else:
                        raise ValueError(
                                "cannot understand the return value "
                                "of the precondition checker %s"
                                % str(checker))
            except Exception as e:  # noqa: W0703
                print(e)
                failed_checks.append(checker)

        err_msgs = []
        for fc in failed_checks:
            msg = ("Precondition %s not met, which was imposed at\n\n"
                   % str(checker))
            if hasattr(fc, "frame"):
                msg = msg + '\n'.join(format_list(extract_stack(
                    fc.frame)))
            err_msgs.append(msg)
        if len(failed_checks) > 0:
            precon_err_msg = (
                    "%d out of %d preconditions are not met"
                    % (len(failed_checks), len(preconditions)))
            for im, msg in enumerate(err_msgs):
                precon_err_msg = (precon_err_msg + '\n\n'
                        + '[%d / %d]: ' % (im + 1, len(failed_checks)) + msg)
            raise PreconditionNotMetError(precon_err_msg)

    def _get_data_mapping(self, arr, knl=None):
        """Make a data mapping using known data, tailored for giving inputs to
        the loopy kernel. Returns all known information if knl is None.

        :param knl: the loopy kernel
        """
        data_map = {}
        expansion_list = []

        # gather captured data
        for arr_name, varr in arr.env.items():

            if arr_name == arr.name:
                # only specify output shape, and let the backend to do the malloc
                for out_s in arr.shape:
                    if out_s not in arr.env:
                        expansion_list.append(arr._extract(out_s))
                    else:
                        data_map[out_s] = arr.env[out_s]

            elif isinstance(varr, np.ndarray):
                data_map[arr_name] = varr

            elif varr is None:
                pass  # self

            elif np.isscalar(varr):
                data_map[arr_name] = varr

            elif isinstance(varr, cl.array.Array):
                data_map[arr_name] = varr

            else:
                raise RuntimeError("unrecogonized captured variable %s" % arr_name)

        if knl is None:
            # gather all known shapes

            for s in arr.shape:
                if s in data_map:
                    continue
                if arr._get_value(s) is not None:
                    data_map[s] = arr._get_value(s)

            for arg, _ in arr.namespace.values():
                if arg is None:
                    continue  # skip self
                assert isinstance(arg, Array)
                for s in arg.shape:
                    if s not in arr.env:
                        expansion_list.append(arr._extract(s))
                    elif arg._get_value(s) is not None:
                        data_map[s] = arr.env[s]

        else:
            # try to get as much extra data that loopy wants as possible
            # also evaluates the shape expressions
            for argname, arg in knl.arg_dict.items():
                if argname in data_map:
                    continue
                if argname in arr.env:
                    data_map[argname] = arr.env[argname]
                elif argname in arr.namespace:
                    # Value unknown, but has expression.
                    # Try to expand the expression on inputs before runtime
                    # (applies to scalar expression, like shape vars)
                    expansion_list.append(arr._extract(argname))

        # Make sure not to include None's prior to evaluating expressions
        data_map = self._purge_nones(data_map)

        for se in expansion_list:
            try:
                seval = evaluate(se.expr, data_map)
            except UnknownVariableError:
                if 0:
                    warnings.warn(
                        "cannot get value for %s prior to calling "
                        "the loopy kernel" % se.name)
                continue

            if se.name in data_map:
                assert (seval is None) or (seval == data_map[se.name])
            else:
                data_map[se.name] = seval

        # Remove keyward arguments not needed by the kernel
        rm_args = []
        if knl is not None:
            for argname in data_map.keys():
                if argname not in knl.arg_dict:
                    rm_args.append(argname)
        for rmarg in rm_args:
            del data_map[rmarg]

        return data_map

    def _purge_nones(self, data_map):
        """Purge None-valued entries from a data map.
        """
        entries_to_purge = []
        for key, val in data_map.items():
            if val is None:
                entries_to_purge.append(key)
        for key in entries_to_purge:
            data_map.pop(key)
        return data_map

    def _make_assignments(self, arr, **kwargs):
        """Make the list of loopy instructions for a lazy array.

        :param substitutions: a dictionary of inlined information.
        :param is_temporary: whether the lhs is a temporary.
        """
        assignments = []

        rhs_expr = arr.expr
        if arr.ndim == 0:
            lhs_expr = var(arr.name)
        else:
            lhs_expr = var(arr.name)[arr.inames]

        if 'substitutions' in kwargs:
            rhs_expr = substitute(rhs_expr, kwargs['substitutions'])

        tc = TemporaryCollector(arr)
        temps = tc(rhs_expr)

        is_temporary = arr.namespace[arr.name][1].get('is_temporary', False)
        is_cse = arr.namespace[arr.name][1].get('is_cse', False)
        has_barrier = arr.namespace[arr.name][1].get('has_barrier', False)

        if arr.name in temps:
            # ignore self when dealing with temps of a temp
            temps.remove(arr.name)

        if is_temporary:
            if is_cse:
                assignments.append(
                        lp.Assignment(lhs_expr, rhs_expr, id=arr.name))
            else:
                # a counter for generating unique names in diamond cases
                sfx = '_%d' % self._counter
                self._counter += 1
                # FIXME: behavior of temporaries is not yet well-defined
                assignments.append(
                        lp.Assignment(lhs_expr, rhs_expr, id=arr.name + sfx))
            if has_barrier:
                raise NotImplementedError()

        else:
            assignments.append(
                    lp.Assignment(lhs_expr, rhs_expr, id=arr.name))

        # recursively add assignments for all temps
        if len(temps) > 0:
            for tmp_name in temps:
                tmp = arr._extract(tmp_name)
                assignments.extend(
                        self._make_assignments(tmp, **kwargs))

        return assignments

    def compile(self, *args, **kwargs):
        # context: where the preconditions are checked
        # data_map: passed to the loopy kernel
        # scalar_map: inlined scalars
        #
        # context = data_map + scalar_map
        context = dict()

        if len(args) > 1:
            raise NotImplementedError()
        arrs = list(args)
        arr = arrs[0]

        shape_dtype = kwargs.pop('shape_dtype', np.int32)

        if arr.domain_expr is None:
            raise ValueError()
        else:
            isl_compiler = LoopDomainCompiler()
            loop_domain = isl_compiler(arr.domain_expr)
            print(loop_domain)

        # collect kernel args
        kernel_data = []
        if arr.ndim == 0:
            kernel_data.append(
                    lp.GlobalArg(
                        arr.name, shape=(1, ), dtype=arr.dtype))
        else:
            kernel_data.append(
                    lp.GlobalArg(
                        arr.name, shape=arr._shape_str, dtype=arr.dtype))

        # evaluate scalar expressions
        # e.g.: size of arange()
        for aname, (a, atag) in arr.namespace.items():
            if a is None:
                continue
            if a.ndim == 0 and arr.env.get(aname, None) is None:
                try:
                    env = arr.env.copy()
                    val = evaluate(a.expr, env)
                    if a.dtype is not None:
                        val = a.dtype(val)
                    arr.env[aname] = val

                except UnknownVariableError as e:
                    print(e)
                    pass

        inline_scalars = True
        if inline_scalars:
            scalar_map = dict()
            assignments = self._make_assignments(arr, substitutions=scalar_map)
        else:
            assignments = self._make_assignments(arr)

        # add more kernel args (reduces a lot of guessing time)
        # e.g., link array shape vars with the arrays, dtypes, etc.
        #
        # (the trick is to add no more than actually needed)
        # FIXME: let loopy.ArgumentGuesser to find out what are needed.
        for arr_name, (varr, tag) in arr.namespace.items():
            if arr_name == arr.name:
                continue  # arr (output) handled above
            if isinstance(varr, Array) and varr.ndim > 0:
                # for now, we only specify inputs

                if varr.dtype is None:
                    dtype = np.int32 if varr.is_integral else np.float64
                else:
                    dtype = varr.dtype

                if tag.get('is_argument', False):
                    kernel_data.append(
                            lp.GlobalArg(
                                arr_name,
                                dtype=dtype,
                                shape=varr._shape_str))
                elif tag.get('is_temporary', False):
                    kernel_data.append(
                            lp.TemporaryVariable(
                                arr_name,
                                dtype=dtype,
                                shape=varr._shape_str))

            elif isinstance(varr, Array) and varr.ndim == 0:
                if varr.dtype is None:
                    dtype = np.int32 if varr.is_integral else np.float64
                else:
                    dtype = varr.dtype
                if tag.get('is_argument', False):
                    if arr_name in scalar_map:
                        pass
                    else:
                        kernel_data.append(
                            lp.ValueArg(arr_name, dtype=dtype))
            else:
                pass
                # warnings.warn(
                #    "cannot find shape information of %s" % arr_name)

        kernel_data.append('...')

        print(kernel_data)

        knl = lp.make_kernel(
                loop_domain, assignments,
                kernel_data,
                lang_version=(2018, 2))

        print(knl)

        knl = lp.set_options(knl, return_dict=True)

        if inline_scalars:
            for vn, (vv, vtag) in arr.namespace.items():
                if vv is None:
                    continue
                if vv.ndim == 0:
                    scalar_map[vn] = arr._get_value(vn)
            scalar_map = self._purge_nones(scalar_map)
            context.update(scalar_map)
            knl = lp.fix_parameters(knl, **scalar_map)

        # help with dtype inference
        extra_dtype_dict = {}
        for argname, arg in knl.arg_dict.items():
            if arg.dtype is None:
                # array args
                sym_arg = arr._extract(argname)
                if sym_arg is not None:
                    extra_dtype_dict[argname] = sym_arg.dtype

                # shape args
                if argname in arr.shape:
                    extra_dtype_dict[argname] = shape_dtype
                for arr_arg in arr.bound_arguments.values():
                    if arr_arg is None:
                        continue
                    if argname in arr_arg.shape:
                        extra_dtype_dict[argname] = shape_dtype

        knl = lp.add_and_infer_dtypes(knl, extra_dtype_dict)

        return knl, context

# }}} End compiler
