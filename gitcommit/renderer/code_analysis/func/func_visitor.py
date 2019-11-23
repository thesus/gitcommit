from .visitor import Visitor
from .func_lister import FuncLister
from .func import Func
import ast


class FuncVisitor(Visitor):
    filepath = ""
    funcs = []

    def __init__(self, filepath):
        self.filepath = filepath

    def visit_python(self, language):
        with open(self.filepath, "r") as file:
            source = file.read()
            tree = ast.parse(source)
        lister = FuncLister()
        lister.visit(tree)

        self.funcs = map(
            lambda x: Func(
                x.name,
                x.lineno,
                x.end_lineno,
                ast.get_source_segment(source, x),
                ast.get_docstring(x),
            ),
            lister.funcs,
        )
