class Func:
    def __init__(self, name, lineno, end_lineno, docstring, filename):
        self.name = name
        self.lineno = lineno
        self.end_lineno = end_lineno
        self.docstring = docstring
        self.filename = filename
