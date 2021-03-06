from gitcommit.renderer.code_analysis.visitor import Visitor
from gitcommit.renderer.code_analysis.func.func_lister import FuncLister
from gitcommit.renderer.code_analysis.func.func import Func
from gitcommit.utils.file_extension import FileExtension
import ast


class FuncVisitor(Visitor):
    content = ""
    funcs = []

    def __init__(self, content):
        Visitor.__init__(self)
        self.content = content

    def visit_python(self, language, filepath):
        tree = ast.parse(self.content)
        lister = FuncLister()
        lister.visit(tree)

        filename = FileExtension.get_filename(filepath)
        self.funcs = [
            Func(x.name, x.lineno, x.end_lineno, ast.get_docstring(x), filename)
            for x in lister.funcs
        ]
