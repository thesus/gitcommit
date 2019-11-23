from .language import CodeAnalysisLanguage


class PythonLanguage(CodeAnalysisLanguage):
    def accept(self, visitor, filepath):
        visitor.visit_python(self, filepath)
