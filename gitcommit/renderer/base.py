import logging

logger = logging.getLogger("base_renderer")


class BaseRenderer:
    def __init__(self, variables, config):
        """Initializes with undefined variables and a config.

        This may be subject to change...
        """

    def render_template_data(self):
        """Returns a dictionary containing the template values."""
        pass

    def success(self):
        """Runs after the template rendering has finished.

        Usefull for propagating changes to a remote.
        """
