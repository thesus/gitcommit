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


    def get_files(self, commit_depth = 1):
        """ Get all files from commit_depth-commit.

        Args:
            commit_depth: Specify from which commit to get the files from.
                          e.g. 1 means last, 2 means second last, ... .

        Returns:
            files: Files from commit specified above.
        """
        #commit = self.repo.walk(self.repo.head.target, GIT_SORT_TIME)[1 - commit_depth]
        # Iterate over all commits 
        for cw in self.repo.walk(self.repo.head.target, GIT_SORT_TIME):
            if (commit_depth == 1):
                commit = cw
                pass
            commit_depth -= 1

        commit_files = self.repo.revparse_single(str(commit.id))
        files = []
        # Iterate over tree entries of before mentioned commit
        for entry in commit.tree:
            files.append(entry.name)
            #files.append(self.repo[entry.id])
            
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