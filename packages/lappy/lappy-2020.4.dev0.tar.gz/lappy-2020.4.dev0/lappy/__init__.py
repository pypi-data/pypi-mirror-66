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

__all__ = []

from lappy.version import GIT_REVISION as __git_revision__  # noqa: N811
from lappy.version import VERSION_TEXT as __version__  # noqa: N811
__all__ += ['__git_revision__', '__version__']

from lappy.exceptions import AxisError, ComplexWarning, RankWarning
__all__ += ['AxisError', 'ComplexWarning', 'RankWarning']

from lappy.core import to_lappy_array
from lappy.core.tools import ScalarType
__all__ += ['to_lappy_array', 'ScalarType']

from lappy.core.ufuncs import sin, cos, exp
__all__ += ['sin', 'cos', 'exp']

from lappy.core.array import Array
from lappy.eval import Compiler, Executor


class ndarray(Array):  # noqa: N801
    def eval(self, queue, check_preconditions=False):
        if self.value is None:
            if hasattr(self, '_closure'):
                pass
            else:
                compiler = Compiler(check_preconditions)
                self._closure = compiler(self)

            print(self._closure.kernel)
            print(self._closure.data_map)

            evaluator = Executor(self._closure)
            res = evaluator(queue)
            self.value = res[self.name]
        return self.value


__all__ += ["ndarray", ]
