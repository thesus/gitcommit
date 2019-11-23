from gitcommit.renderer import BaseRenderer
from gitcommit.utils.file_extension import FileExtension
from gitcommit.utils.git import PygitHelper
from gitcommit.renderer.code_analysis.func.func_visitor import FuncVisitor
from pygit2 import GIT_OID_HEX_ZERO


class CodeAnalysisRenderer(BaseRenderer):
    def __init__(self, variables, config):
        self.variables = variables
        self.config = config
        self.pygit = PygitHelper()

    def render_template_data(self):
        # get new and old version of changed files from
        changes = self.pygit.get_files_tuple()
        # find newly added files
        added_files = [
            FileExtension.get_filename(n.path)
            for (n, o) in changes
            if str(o.id) == GIT_OID_HEX_ZERO
        ]
        removed_files = [
            FileExtension.get_filename(n.path)
            for (n, o) in changes
            if str(n.id) == GIT_OID_HEX_ZERO
        ]
        result = {"added_files": added_files, "removed_files": removed_files}
        # only look for function changes in existing files
        result.update(
            self.func_changes(
                [
                    (n, o)
                    for (n, o) in changes
                    if str(o.id) != GIT_OID_HEX_ZERO and str(n.id) != GIT_OID_HEX_ZERO
                ]
            )
        )
        return result

    def func_changes(self, changes):
        added = []
        removed = []
        changed = []
        for new, old in changes:
            ext = FileExtension.get_extension(new.path)
            # get funcs in new version
            visitor = FuncVisitor(self.pygit.repo[new.id].data)
            visitor.visit(ext)
            new_funcs = visitor.funcs

            # get funcs in old version
            visitor.content = self.pygit.repo[old.id].data
            visitor.visit(ext)
            old_funcs = visitor.funcs

            # find added, removed and already existing functions
            existing_funcs = [
                (n, o) for n in new_funcs for o in old_funcs if n.name == o.name
            ]
            added.extend(
                [
                    n.name
                    for n in new_funcs
                    if not any([o for o in old_funcs if n.name == o.name])
                ]
            )
            removed.extend(
                [
                    o.name
                    for o in old_funcs
                    if not any([n for n in new_funcs if o.name == n.name])
                ]
            )

            # look for changes in existing functions
            # find -1 entries in file diff
            diff = [
                (n, o)
                for (n, o) in self.pygit.get_diff(new.id, old.id)
                if n == -1 or o == -1
            ]

            for existing_func in existing_funcs:
                # check if line of function has been added or removed
                if any(
                    [
                        n
                        for (n, o) in diff
                        if n >= existing_func[0].lineno
                        and n <= existing_func[0].end_lineno
                    ]
                ) or any(
                    [
                        o
                        for (n, o) in diff
                        if o >= existing_func[1].lineno
                        and o <= existing_func[1].end_lineno
                    ]
                ):
                    changed.append(existing_func[0].name)

        return {
            "added_functions": added,
            "removed_functions": removed,
            "changed_functions": changed,
        }
