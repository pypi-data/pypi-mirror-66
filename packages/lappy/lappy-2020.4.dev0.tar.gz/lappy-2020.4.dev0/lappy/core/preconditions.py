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
import inspect
from pymbolic import evaluate, var
from pymbolic.primitives import Product


class EvaluationPrecondition(object):
    """Precondition for kernel evaluations.
    Each condition caputures a stack frame to trace back to the place where it is
    imposed.
    """
    def __init__(self, checker, name=None):
        """Captures the stack frame where the condition is constructed for backtrace.
        """
        assert callable(checker)
        self.checker = checker

        if name is None:
            self.name = self._get_checker_name()
        else:
            self.name = name

        self.frame = self._get_frame_obj()

        # if using Py3, call clear()
        if hasattr(self.frame, 'clear'):
            self.frame.clear()

    def _get_frame_obj(self):  # noqa: W0613,R0201
        """Makes an extra frame so that the checker's frame can be
        cleared (to break reference cycles) for better lifetime management.
        """
        return inspect.currentframe()

    def _get_checker_name(self, base_checker=None):
        """Find a name for the checker.
        """
        if base_checker is None:
            base_checker = self.checker

        if hasattr(base_checker, '__name__'):
            # a function declared with def ...
            return base_checker.__name__

        elif hasattr(base_checker, 'func'):
            # a function wrapper, e.g., a partial obj
            return self._get_checker_name(base_checker.func)

        else:
            # the last resort, e.g. unamed lambda
            return 'evaluation_precondition'

    def __str__(self):
        return self.name

    def __call__(self, *args, **kwargs):
        return self.checker(*args, **kwargs)


def logical_or(*checkers):
    """A meta-checker, logical OR for multiple checkers.
    """
    for chkr in checkers:
        assert callable(chkr)

    def meta_checker(*args, **kwargs):
        res_list = []
        for chkr in checkers:
            try:
                res_list.append(chkr(*args, **kwargs))
            except Exception:  # noqa: W0703
                res_list.append(False)
        return any(res_list)

    return EvaluationPrecondition(meta_checker, 'logical_or')


def logical_and(*checkers):
    """A meta-checker, logical AND for multiple checkers.
    """
    for chkr in checkers:
        assert callable(chkr)

    def meta_checker(*args, **kwargs):
        res_list = []
        for chkr in checkers:
            try:
                res_list.append(chkr(*args, **kwargs))
            except Exception:  # noqa: W0703
                res_list.append(False)
        return all(res_list)

    return EvaluationPrecondition(meta_checker, 'logical_and')


def logical_not(checker):
    """A meta-checker, logical NOT for multiple checkers.
    """
    assert callable(checker)

    def meta_checker(*args, **kwargs):
        try:
            res = checker(*args, **kwargs)
        except Exception:  # noqa: W0703
            res = False
        return (not res)

    return EvaluationPrecondition(meta_checker, 'logical_not')


# {{{ some built-in preconditions


def make_size_conservation_condition(array, newshape):
    """Check that the array's size is as specified by the newshape.
    """
    def check_size_conservation(context):
        """
        :param context: a dict of {name: data} to evaluate the expressions in
        """
        old_size = evaluate(array.size, context)
        act_new_shape = tuple(
            var(s.name) if hasattr(s, 'name') else s
            for s in newshape)
        new_size = evaluate(Product(act_new_shape), context)
        if not old_size == new_size:
            raise ValueError("cannot reshape array of size %s into shape %s"
                    % (str(old_size), str(act_new_shape)))
        return old_size == new_size
    return EvaluationPrecondition(check_size_conservation)

# }}} End some built-in preconditions
