import ast


class FuncLister(ast.NodeVisitor):
    funcs = []

    def visit_FunctionDef(self, node):
        self.funcs.append(node)
        self.generic_visit(node)
