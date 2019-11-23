class Func:
    def __init__(self, name, lineno, end_lineno, segment, docstring):
        self.name = name
        self.lineno = lineno
        self.end_lineno = end_lineno
        self.segment = segment
        self.docstring = docstring
