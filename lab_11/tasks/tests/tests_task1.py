#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 20:23:55 2020

@author: zofiadomanowska
"""


import pytest

from lab_11.tasks.tools.calculator import (
    Calculator,
    CalculatorError,
    EmptyMemory,
    NotNumberArgument,
    WrongOperation,
)

@pytest.fixture
def open_calculator():
    return Calculator()

@pytest.fixture
def clc():
    return Calculator().run("+",2,10)

@pytest.mark.parametrize(
    'operator, param_1, param_2, expected',
    [
        ('+', 1, 3, 4),
        ('+', 1, 10, 11),
        ('-', 10, 3, 7),
        ('-', 12, 4, 8),
        ('/', 3, 3, 1),
        ('/', 16, 4, 4),
        ('*', 3, 10, 30),
        ('*', 12, 4, 48)
    ]
)
def test_calculation(op_clc, operator, param_1, param_2, expected):
    assert op_clc.run(operator, param_1, param_2) == expected

def test_zero_division(op_clc):
    try:
        op_clc.run('/', 1, 0)
    except CalculatorError as exc:
        assert type(exc.__cause__) == ZeroDivisionError
    else:
        raise AssertionError

def test_memorisation(op_clc):
    op_clc.run('+', 2, 20)
    op_clc.memorize()
    assert op_clc.memory == 22

@pytest.mark.parametrize(
    'operate, param_1, expected',
    [
        ('+', 3, 6),
        ('+', 12, 15),
        ('-', 3, 0),
        ('-', 12, 9),
        ('/', 3, 1),
        ('/', 12, 4),
        ('*', 3, 9),
        ('*', 12, 36)
    ]
)
def test_recall(op_clc, operate, param_1, expected):
    op_clc.run('+', 2, 1)
    op_clc.memorize()
    assert op_clc.run(operate, param_1) == expected

def test_missing_memory(op_clc):
    try:
        op_clc.in_memory()
    except CalculatorError as exc:
        assert type(exc) is EmptyMemory
    else:
        raise AssertionError

def test_missing_memory2(op_clc):
    try:
        op_clc.run("-", 2)
    except CalculatorError as exc:
        assert type(exc) is EmptyMemory
    else:
        raise AssertionError

def test_wrong_operator(op_clc):
    try:
        op_clc.run('^', 2, 3)
    except CalculatorError as exc:
        assert type(exc) == WrongOperation
    else:
        raise AssertionError

def test_wrong_type(op_clc, param_1, param_2):
    try:
        op_clc.run('+', param_1, param_2)
    except CalculatorError as exc:
        assert type(exc) == NotNumberArgument
    else:
        raise AssertionError
        
        