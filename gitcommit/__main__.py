import logging
from jinja2 import Environment, FileSystemLoader, meta, Template
from gitcommit.renderer import GitlabRenderer, HistoryRenderer, MessageRenderer, CodeAnalysisRenderer
from gitcommit.config.config import get_config

ROOT_DIR = "./"
RENDERERS = [CodeAnalysisRenderer, HistoryRenderer]


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
        data = {}
        renderers = []
        for renderer_class in RENDERERS:
            renderer = renderer_class(self.variables, self.config)
            renderers.append(renderer)

            data.update(renderer.render_template_data())

        rendered = self.template.render(data)

        print(rendered)

        # Run succes methods on rendererers
        for renderer in renderers:
            renderer.success()


if __name__ == "__main__":
    setup_logging()

    instance = TemplateLoader("template")
    instance.run()
