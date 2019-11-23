from .language import CodeAnalysisLanguage


class PythonLanguage(CodeAnalysisLanguage):
    def accept(self, visitor):
        visitor.visit_python(self)
