
import modelx as mx
from modelx.core.errors import (
    FormulaError,
    DeepReferenceError,
    NoneReturnedError)
import pytest
from textwrap import dedent


@pytest.fixture(scope="module")
def errormodel():

    m = mx.new_model("ErrorModel")
    s = m.new_space("ErrorSpace")

    @mx.defcells
    def foo(x):
        if x > 0:
            return foo(x-1) + 1
        else:
            raise ValueError

    @mx.defcells
    def bar(x):
        if x > 0:
            return bar(x-1)
        else:
            return None

    @mx.defcells
    def infinite(x):
        return infinite(x-1)

    return m


def test_value_error(errormodel):

    cells = errormodel.ErrorSpace.foo
    with pytest.raises(FormulaError) as errinfo:
        cells(1)

    errmsg = dedent("""\
        Error raised during formula execution
        ValueError
        Formula traceback:
        0: ErrorModel.ErrorSpace.foo(x=1), line 3
        1: ErrorModel.ErrorSpace.foo(x=0), line 5
        Formula source:
        def foo(x):
            if x > 0:
                return foo(x-1) + 1
            else:
                raise ValueError
        """)

    assert errinfo.value.args[0] == errmsg
    assert isinstance(mx.get_error(), ValueError)
    assert mx.get_traceback() == [(cells.node(1), 3),
                                  (cells.node(0), 5)]


def test_none_returned_error(errormodel):

    cells = errormodel.ErrorSpace.bar
    with pytest.raises(FormulaError) as errinfo:
        cells(1)

    errmsg = dedent("""\
        Error raised during formula execution
        modelx.core.errors.NoneReturnedError: ErrorModel.ErrorSpace.bar(x=0)
        Formula traceback:
        0: ErrorModel.ErrorSpace.bar(x=1), line 3
        1: ErrorModel.ErrorSpace.bar(x=0)
        Formula source:
        def bar(x):
            if x > 0:
                return bar(x-1)
            else:
                return None
        """)

    assert errinfo.value.args[0] == errmsg
    assert isinstance(mx.get_error(), NoneReturnedError)
    assert mx.get_traceback() == [(cells.node(1), 3),
                                  (cells.node(0), 0)]


def test_deep_reference_error(errormodel):

    cells = errormodel.ErrorSpace.infinite
    saved = mx.get_recursion()
    try:
        mx.set_recursion(3)
        with pytest.raises(FormulaError) as errinfo:
            cells(3)
    finally:
        mx.set_recursion(saved)

    errmsg = dedent("""\
        Error raised during formula execution
        modelx.core.errors.DeepReferenceError: Formula chain exceeded the 3 limit
        Formula traceback:
        0: ErrorModel.ErrorSpace.infinite(x=3), line 2
        1: ErrorModel.ErrorSpace.infinite(x=2), line 2
        2: ErrorModel.ErrorSpace.infinite(x=1), line 2
        3: ErrorModel.ErrorSpace.infinite(x=0), line 2
        Formula source:
        def infinite(x):
            return infinite(x-1)
        """)

    assert errinfo.value.args[0] == errmsg
    assert isinstance(mx.get_error(), DeepReferenceError)
    assert mx.get_traceback() == [(cells.node(3), 2),
                                  (cells.node(2), 2),
                                  (cells.node(1), 2),
                                  (cells.node(0), 2)]



