import os
import logging
from jinja2 import Environment, FileSystemLoader, meta, Template
from gitcommit.renderer import (
    GitlabRenderer,
    HistoryRenderer,
    MessageRenderer,
    CodeAnalysisRenderer,
)
from gitcommit.config.config import get_config

ROOT_DIR = "./"
RENDERERS = [GitlabRenderer, CodeAnalysisRenderer, HistoryRenderer, MessageRenderer]


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


class TemplateLoader:
    def __init__(self, template_name):
        self.env = Environment(trim_blocks=True, lstrip_blocks=True)

        # Load template from local .igitcommit file, otherwise use default template
        # TODO: Traverse to root dirs to find the file even from subdirectories
        if os.path.isfile(".igitcommit"):
            with open(".igitcommit") as f:
                template = f.read()
        else:
            from gitcommit.template import template

        # Load template with the given environment
        self.template = self.env.from_string(template)

        # Preprocess file to find unused variables
        self.variables = meta.find_undeclared_variables(self.env.parse(template))

        # Load config
        # TODO: Use different configs for different projects
        self.config = get_config(ROOT_DIR + "config.ini")

    def run(self):
        data = {}
        renderers = []
        # Join all results and render them in a template
        for renderer_class in RENDERERS:
            renderer = renderer_class(self.variables, self.config)
            renderers.append(renderer)

            data.update(renderer.render_template_data())

        rendered = self.template.render(data)

        print(rendered)

        # Run success methods on rendererers after rendering completed
        for renderer in renderers:
            renderer.success()


if __name__ == "__main__":
    setup_logging()

    instance = TemplateLoader("template")
    instance.run()
