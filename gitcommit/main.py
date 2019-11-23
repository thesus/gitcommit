import logging

from jinja2 import Environment, FileSystemLoader, meta, Template

# from renderer.base import BaseRenderer
from config.config import get_config


ROOT_DIR = "./"


def setup_logging():
    """Sets up logging facilities.

    You can use the logger via logger.debug('my message') in each module.
    See https://docs.python.org/3/library/logging.html#logging.debug
    """
    # Create root logger
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    # Add handler to pump data to stdout in the specified format
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    root.addHandler(handler)

    return root


setup_logging()

RENDERERS = []
# RENDERES = [BaseRenderer]


class TemplateLoader:
    def __init__(self, template_name):
        self.env = Environment(loader=FileSystemLoader(ROOT_DIR + "templates"))
        # Load source of the template
        source = self.env.loader.get_source(self.env, template_name)

        # Preprocess file to find unused variables
        self.variables = meta.find_undeclared_variables(self.env.parse(source))
        # Load template
        self.template = self.env.get_template(template_name)

        # Load config
        # TODO: Use different configs for different projects
        self.config = get_config(ROOT_DIR + "config.ini")


    def run(self):
        for renderer in RENDERERS:
            instance = renderer(self.template, self.variables, self.config)

            # TODO: is a template renderable multiple times?
            self.template = instance.render_template()


if __name__ == "__main__":
    instance = TemplateLoader("template")
    instance.run()
