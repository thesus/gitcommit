import logging

logger = logging.getLogger("base_renderer")


class BaseRenderer:
    def __init__(self, template, variables, config):
        """Initializes with a template, undefined variables and a config.

        This may be subject to change...
        """

    def render_template(self):
        """Returns the rendered jinja2 template."""
        pass
