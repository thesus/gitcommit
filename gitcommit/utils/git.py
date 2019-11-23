import os
from pygit2 import Repository, GIT_SORT_TIME


class PygitHelper:
    def __init__(self):
        """ Initialize repository object to current working directory
    
        """
        self.repo = Repository(os.getcwd())

    def get_diff(self, id_a, id_b):
        """ Get different lines of a staged file and the its commit_depth-commit version.

        Returns:
            files: Mapping from old lines numbers to new line numbers
        """
        patch = self.repo[id_b].diff(self.repo[id_a])
        for hunk in patch.hunks:
            for line in hunk.lines:
                yield line.new_lineno, line.old_lineno

    def get_files(self, rev_a=0, rev_b=None):
        """ Get all files from commit_depth-commit.

        Args:
            rev_a: Index to start from
            rev_b: Index to go to

        Returns:
            new_files: Files from new commit specified above.
            old_files: Files from old commit specified above.
        """
        if not rev_b:
            deltas = self.repo.diff("HEAD~" + str(rev_a), cached=True).deltas
        else:
            # Iterate over all commits
            deltas = self.repo.diff("HEAD~" + str(rev_a), "HEAD~" + str(rev_b)).deltas

        o_files = []
        n_files = []
        for delta in deltas:
            n_files.append(delta.new_file)
            o_files.append(delta.old_file)

        return n_files, o_files

    def get_files_tuple(self, rev_a=0, rev_b=None):
        """ Get all files from commit_depth-commit.

        Args:
            rev_a: Index to start from
            rev_b: Index to go to

        Returns:
            files: List of tuple containing new and old files
        """
        if not rev_b:
            deltas = self.repo.diff("HEAD~" + str(rev_a), cached=True).deltas
        else:
            # Iterate over all commits
            deltas = self.repo.diff("HEAD~" + str(rev_a), "HEAD~" + str(rev_b)).deltas

        files = []
        for delta in deltas:
            files.append((delta.new_file, delta.old_file))

        return files

    def get_remote(self):
        """ Get configured remotes

        Returns:
            remotes: All configured remotes as dictionary containing name and
                url
        """

        remotes = {}

        for rep in self.repo.remotes:
            remotes[rep.name] = rep.url

        return remotes

    def get_branches(self):
        """ Get all branches of the current repository

        Returns: 
            branches_local: All local branches
            branches_remote: All remote branches
        """

        branches_local = list(self.repo.branches.local)
        branches_remote = list(self.repo.branches.remote)

        return branches_local, branches_remote

    def get_current_branch(self):
        """ Get current branch

        Returns:
            current_branch: Name of the branch currently checked out
        """
        current_branch = (self.repo.head.name).rsplit("/", 1)[1]

        return current_branch

    def get_commit_history(self, length=10):
        """ Get commit history

        Returns:
            commits: List of pygit2.Commit objects containing information about
                the commit
        """
        commits = []

        for commit in self.repo.walk(self.repo.head.target, GIT_SORT_TIME):
            if length == 0:
                return commits

            commits.append(commit)
            length -= 1

        return commits
