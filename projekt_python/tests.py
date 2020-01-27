# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 17:03:16 2020

@author: zdomanowsk001
"""

import pytest
from wybory_euro import przelicz_jednostke
from unittest import mock
from wybory_euro import read_data
from collections import Counter



def test_przelicz_jednostke():
    mandaty_partii = Counter({'a':49, 'b':37, 'c':1})
    assert przelicz_jednostke(mandaty_partii) == Counter({'a': 1.0, 'b': 0.0, 'c': 0.0})
 
@mock.patch('data.os.path.isfile', return_value=False) 
def test_read_data():
    with pytest.raises(ValueError):
        read_data('filetestowy.csv')
