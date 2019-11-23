import os
from pygit2 import Repository, GIT_SORT_TIME

class PygitHelper:
    
    def __init__(self):
        """ Initialize repository object to current working directory
    
        """
        self.repo = Repository(os.getcwd()) 


    def get_diff(self, commit_depth = 1):
        """ Get difference of staged files and the commit_depth-commit.

        Returns:
            files: Array of files with all changes denoted by + or - 
            changes: Array of array containing changed lines of the corresponding
                file.
        """
        """
        diff_files = self.repo.diff("HEAD~" + commit_depth, cached=True)

        files = []
        changes = []
        # Iterate over all changed files
        for patch in diff_files:
            files.append(patch)
            # ATTENTION: THIS CLASS IS NOT FINISHED

        return files, changes
        """
        print("Function not implemented!")


    def get_files(self, rev_a = 0, rev_b = 1):
        """ Get all files from commit_depth-commit.

        Args:
            rev_a:
            rev_b:

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