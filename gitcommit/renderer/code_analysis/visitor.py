from gitcommit.renderer.code_analysis.language.language import CodeAnalysisLanguage
from collections import defaultdict
from gitcommit.renderer.code_analysis.language.python_language import PythonLanguage


class Visitor:
    def __init__(self):
        self.extensions = defaultdict(lambda: CodeAnalysisLanguage())
        self.extensions[".py"] = PythonLanguage()

    def visit(self, ext):
        self.extensions[ext].accept(self)

    def visit_python(self, language):
        pass
