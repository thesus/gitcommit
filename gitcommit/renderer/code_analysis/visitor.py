from gitcommit.renderer.code_analysis.language.language import CodeAnalysisLanguage
from collections import defaultdict
from gitcommit.renderer.code_analysis.language.python_language import PythonLanguage
from gitcommit.utils.file_extension import FileExtension


class Visitor:
    def __init__(self):
        self.extensions = defaultdict(lambda: CodeAnalysisLanguage())
        self.extensions[".py"] = PythonLanguage()

    def visit(self, filepath):
        ext = FileExtension.get_extension(filepath)
        self.extensions[ext].accept(self, filepath)

    def visit_python(self, language):
        pass
