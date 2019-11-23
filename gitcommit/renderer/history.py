from gitcommit.renderer import BaseRenderer
from gitcommit.utils.git import PygitHelper

from pygit2 import GIT_SORT_TOPOLOGICAL

import logging

logger = logging.getLogger("history")


class HistoryRenderer(BaseRenderer):
    """Search for relevant commits in recent history."""

    def __init__(self, variables, config):
        self.variables = variables
        self.config = config

        self.pygit = PygitHelper()

    def walk_history(self):
        relevant_files = set([f.path for f in self.pygit.get_files()[0]])

        logger.info("Files changed: {}".format(relevant_files))
        commit_list = []

        # If there are no changed files, no commits for them.
        if len(relevant_files) == 0:
            return []

        commits = []
        last_commit = None
        for commit in self.pygit.repo.walk(
            self.pygit.repo.head.target, GIT_SORT_TOPOLOGICAL
        ):
            if not last_commit:
                last_commit = commit
                continue

            # Exclude merge commits
            if len(last_commit.parents) > 1:
                last_commit = commit
                continue

            # get diff objects between two commits
            delta = [
                d.new_file
                for d in self.pygit.repo.diff(
                    a=str(commit.id), b=str(last_commit.id)
                ).deltas
            ]

            change_between = set([x.path for x in delta])

            if len(relevant_files.intersection(change_between)) != 0:
                commits.append(last_commit)
                # Only return the last 5 commits editing the same files as staged
                if len(commits) >= 5:
                    break

            last_commit = commit

        return commits

    def render_template_data(self):
        commits = self.walk_history()
        return {
            "history": [
                {"message": c.message.strip("\n"), "author": c.author.email}
                for c in commits
            ]
        }
