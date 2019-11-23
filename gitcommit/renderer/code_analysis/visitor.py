class Visitor:
    def visit(self, language):
        language.accept(self)

    def visit_python(self, language):
        pass
