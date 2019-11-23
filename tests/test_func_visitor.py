from gitcommit.renderer import GitlabRenderer
from gitcommit.renderer.code_analysis.func.func_visitor import FuncVisitor
from gitcommit.renderer.code_analysis.language.python_language import PythonLanguage

import pytest

def test_visit_python():
    content = """def test():
    return None

def function():
    return None"""

    visitor = FuncVisitor(content)
    visitor.visit_python(PythonLanguage())
    assert len(visitor.funcs) == 2
    func_test = visitor.funcs[0]
    func_function = visitor.funcs[1];
    assert func_test.name == "test"
    assert func_test.lineno == 1
    assert func_test.end_lineno == 2
    assert func_function.name == "function"
    assert func_function.lineno == 4
    assert func_function.end_lineno == 5