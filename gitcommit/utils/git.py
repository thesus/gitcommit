import os
from pygit2 import Repository, GIT_SORT_TIME

class PygitHelper:
    
    def __init__(self):
        """ Initialize repository object to current working directory
    
        """
        self.repo = Repository(os.getcwd()) 


    def get_diff(self, filepath, commit_depth = 1):
        """ Get different lines of a staged file and the its commit_depth-commit version.

        Returns:
            files: Mapping from old lines numbers to new line numbers
        """
        for patch in self.repo.diff():
            for hunk in patch.hunks:
                for line in hunk.lines:
                    yield line.new_lineno, line.old_lineno

    def get_files(self, rev_a = 0, rev_b = 1):
        """ Get all files from commit_depth-commit.

        Args:
            rev_a: Index to start from
            rev_b: Index to go to

        Returns:
            new_files: Files from new commit specified above.
            old_files: Files from old commit specified above.
        """
        # Iterate over all commits 
        deltas = self.repo.diff("HEAD~" + str(rev_a), "HEAD~" + str(rev_b)).deltas

        o_files = []
        n_files = []
        for delta in deltas:
            n_files.append(delta.new_file.id)
            o_files.append(delta.old_file.id)

        return n_files, o_files


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