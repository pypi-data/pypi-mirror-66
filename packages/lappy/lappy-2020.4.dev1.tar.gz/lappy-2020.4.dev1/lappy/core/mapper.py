# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, print_function

copyright__ = "Copyright (C) 2017 Sophia Lin and Andreas Kloeckner"

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
from pymbolic.mapper import Collector
from pymbolic.mapper.stringifier import (
        StringifyMapper,
        PREC_SUM, PREC_COMPARISON, PREC_NONE, PREC_PRODUCT)


class SetVariableCollector(Collector):
    """Traverse a loop domain expression and collect the set variables.
    """
    def map_set_variable(self, expr):
        return {expr.name, }

    map_set_zero = Collector.map_constant
    map_set_parameter = Collector.map_constant
    map_pwaff_comparison = Collector.map_comparison
    map_pwaff_sum = Collector.map_sum
    map_pwaff_product = Collector.map_sum
    map_set_union = Collector.map_sum
    map_set_intersection = Collector.map_sum
    map_pwaff_floor_div = Collector.map_quotient
    map_pwaff_remainder = Collector.map_quotient


class SetParameterCollector(Collector):
    """Traverse a loop domain expression and collect the set parameters.
    """
    def map_set_parameter(self, expr):
        return {expr.name, }

    map_set_zero = Collector.map_constant
    map_set_variable = Collector.map_constant
    map_pwaff_comparison = Collector.map_comparison
    map_pwaff_sum = Collector.map_sum
    map_pwaff_product = Collector.map_sum
    map_set_union = Collector.map_sum
    map_set_intersection = Collector.map_sum
    map_pwaff_floor_div = Collector.map_quotient
    map_pwaff_remainder = Collector.map_quotient


class SetExpressionStringifyMapper(StringifyMapper):
    def map_set_variable(self, expr, *args, **kwargs):
        return expr.name

    def map_set_parameter(self, expr, *args, **kwargs):
        return expr.name

    def map_set_zero(self, expr, *args, **kwargs):
        return expr.name

    def map_set_union(self, expr, enclosing_prec, *args, **kwargs):
        return self.parenthesize_if_needed(
                self.join_rec(u" ∪ ", expr.children, PREC_SUM, *args, **kwargs),
                enclosing_prec, PREC_SUM)

    def map_set_intersection(self, expr, enclosing_prec, *args, **kwargs):
        return self.parenthesize_if_needed(
                self.join_rec(u" ∩ ", expr.children, PREC_SUM, *args, **kwargs),
                enclosing_prec, PREC_SUM)

    def map_pwaff_comparison(self, expr, enclosing_prec, *args, **kwargs):
        return self.format("{%s %s %s}",
                    self.rec(expr.left, PREC_COMPARISON, *args, **kwargs),
                    expr.operator,
                    self.rec(expr.right, PREC_COMPARISON, *args, **kwargs))

    def map_pwaff_floor_div(self, expr, enclosing_prec, *args, **kwargs):
        return self.format("%s // %s",
                    self.rec(expr.numerator, PREC_NONE, *args, **kwargs),
                    self.rec(expr.denominator, PREC_NONE, *args, **kwargs))

    def map_pwaff_sum(self, expr, enclosing_prec, *args, **kwargs):
        return self.parenthesize_if_needed(
                self.join_rec(" + ", expr.children, PREC_SUM, *args, **kwargs),
                enclosing_prec, PREC_SUM)

    def map_pwaff_product(self, expr, enclosing_prec, *args, **kwargs):
        return self.parenthesize_if_needed(
                self.join_rec("*", expr.children, PREC_PRODUCT, *args, **kwargs),
                enclosing_prec, PREC_PRODUCT)
