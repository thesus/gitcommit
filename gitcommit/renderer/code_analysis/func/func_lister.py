import ast


class FuncLister(ast.NodeVisitor):
    def __init__(self):
        self.funcs = []

    def visit_FunctionDef(self, node):
        self.funcs.append(node)
        self.generic_visit(node)
