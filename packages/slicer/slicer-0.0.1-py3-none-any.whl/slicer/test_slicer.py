from . import Slicer
import pytest

def test_slicer():
    o = [1,2,3]
    s = Slicer(o)

    assert o[0] == s[0]