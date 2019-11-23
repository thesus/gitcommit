from gitcommit.renderer import BaseRenderer
from gitcommit.utils.git import PygitHelper

import re
import os
import logging
import gitlab

logger = logging.getLogger("gitlab_bridge")

class GitlabRenderer(BaseRenderer):
    """Searches a merge request for the current branch and proposes commit messages based on them."""

    def __init__(self, variables, config):
        self.variables = variables
        self.config = config

        pygit = PygitHelper()

        remotes = pygit.get_remote()

        # FIXME: Only a remote named origin works atm
        match = re.search("(?<=\@)(.*?)(?=\:)", remotes["origin"])
        self.server = "https://" + match.group(0)

        match = re.search("(?<=\:)(.*?)(?=\.git)", remotes["origin"])
        self.repository = match.group(0)

        self.branch = pygit.get_current_branch()

        if "GITLAB_PRIVATE_TOKEN" in os.environ:
            self.private_token = os.environ["GITLAB_PRIVATE_TOKEN"]
        else:
            self.private_token = None


    def connect(self):
        """Connects to the API and sets the internal connection parameter."""
        logger.info(
            "Connecting to {} with {} as token".format(
                self.server, self.private_token
            )
        )

        self.connection = gitlab.Gitlab(self.server, private_token=self.private_token)

        self.connection.auth()
        logger.info("Connecting succesful")

    def setup_project(self):
        """Returns the id of a given project."""
        return self.connection.projects.get(self.repository)

    def find_mr(self):
        """Returns a list of merge requests for the current branch."""
        return self.project.mergerequests.list(source_branch=self.branch)

    def parse_checklist(checklist):
        """Parses a checklist and returns the last unchecked item and a line number.

        If there's no (unchecked) checklist item, return None and -1
        """
        for i, line in enumerate(checklist.splitlines()):
            if line.startswith("* [ ]"):
                return line[5:].strip(), i

        return None, -1

    def crawl_mergerequest(self):
        logger.info("Searching for merge request")
        mrs = self.find_mr()
        # If there's no merge request to a branch, we can't infer information from the remote
        if len(mrs) == 0:
            logger.info("No Merge Request found.")
            return None
        # For now only work with the first mr in the result
        else:
            mr = mrs[0]
            logger.info("Found Merge Request, using {}".format(mr.title))
            return mr

    def render_template_data(self):
        """Renders data from the Gitlab API

        Returns:
            data: dict containing keys with the `remote` prefix
        """
        # Do not run method if no private token is set via env variable
        if not self.private_token:
            return {}

        self.connect()
        self.project = self.setup_project()
        self.mergerequest = self.crawl_mergerequest()

        logger.info("Write checklist items in the result.")
        if self.mergerequest:
            item, self.line = GitlabRenderer.parse_checklist(
                self.mergerequest.description
            )
        else:
            item = None
            self.line = -1

        data = {"remote": {"next_task": item}}

        return data

    def success(self):
        if self.mergerequest:
            lines = self.mergerequest.description.splitlines()
            lines[self.line] = lines[self.line].replace("* [ ]", "* [x]")

            self.mergerequest.description = "\n".join(lines)

            self.mergerequest.save()
