# -*- coding: utf-8 -*-
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

import pytest
import islpy as isl
from lappy.core.primitives import SetVar, SetParam
from lappy.core.mapper import SetVariableCollector, SetParameterCollector
from lappy.eval.compiler import LoopDomainCompiler


@pytest.mark.parametrize('expr, var', [
    (SetVar('i') + SetParam('j'), {'i', }),
    (SetVar('i') + SetVar('j'), {'i', 'j'}),
    (SetVar('i').le(SetParam('n')).and_(SetVar('j').ge(1)), {'i', 'j'}),
    ])
def test_variable_collector(expr, var):
    collector = SetVariableCollector()
    assert collector(expr) == var


@pytest.mark.parametrize('expr, var', [
    (SetVar('i') + SetParam('j'), {'j', }),
    (SetVar('i') + SetVar('j'), set()),
    (SetVar('i').le(SetParam('n')).and_(SetVar('j').ge(1)), {'n', }),
    ])
def test_parameter_collector(expr, var):
    collector = SetParameterCollector()
    assert collector(expr) == var


@pytest.mark.parametrize('expr,expected_set', [
    ((SetVar('i') + SetVar('j')).ge(10).and_(
        SetVar('i').le(SetParam('m'))).and_(
            SetVar('j').lt(SetParam('n'))),
        ["[m, n] -> { [i, j]: i <= m and j < n and i + j >= 10}"]),
    (SetVar('i').lt(SetParam('n')).and_(SetVar('i').ge(0)),
        ["[n] -> { [i]: i < n and i >= 0 }"]),
    (SetVar('i').lt(SetParam('n')).and_((SetVar('i') * 12 + 3).ge(-2)),
        ["[n] -> { [i]: i < n and i * 12 + 3 >= -2 }"]),
    (SetVar('i').lt(SetParam('n')).and_(
        (SetVar('i') - 9).ge(8)),
        ["[n] -> { [i]: i < n and i - 9 >= 8 }"]),
    (SetVar('i').lt(SetParam('n')).and_(
        (SetVar('i') // 9).ge(8)),
        ["[n] -> { [i]: i < n and i / 9 >= 8 }"]),
    ])
def test_loop_domain_compiler(expr, expected_set):

    compiler = LoopDomainCompiler()
    domain = compiler(expr)

    print(domain)
    expected_domain = [
            isl.BasicSet.read_from_str(isl.DEFAULT_CONTEXT, es)
            for es in expected_set]

    assert domain == expected_domain


@pytest.mark.parametrize('expr,expected_str', [
    ((SetVar('i') + SetVar('j')).ge(10).and_(
        SetVar('i').le(SetParam('m'))).and_(
            SetVar('j').lt(SetParam('n'))),
        u"{i + j >= 10} ∩ {i <= m} ∩ {j < n}"),
    (SetVar('i').lt(SetParam('n')).and_(SetVar('i').ge(0)),
        u"{i < n} ∩ {i >= 0}"),
    (SetVar('i').lt(SetParam('n')).and_((SetVar('i') * 12 + 3).ge(-2)),
        u"{i < n} ∩ {i*12 + 3 >= -2}"),
    (SetVar('i').lt(SetParam('n')).and_(
        (SetVar('i') - 9).ge(8)),
        u"{i < n} ∩ {i + -9 >= 8}"),
    (SetVar('i').lt(SetParam('n')).and_(
        (SetVar('i') // 9).ge(8)),
        u"{i < n} ∩ {i // 9 >= 8}"),
    ])
def test_loop_domain_expr_stringifier(expr, expected_str):
    stringified = expr.make_stringifier()(expr)
    assert stringified == expected_str
