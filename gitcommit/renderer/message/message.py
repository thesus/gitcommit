import logging, requests
from gitcommit.renderer import BaseRenderer

logger = logging.getLogger("base_renderer")

class MessageRenderer(BaseRenderer):
    def __self__(self, variables, config):
        self.variables = variables
        self.config = config

    def render_template_data(self):
        """ Generate random message

        Returns: 
            data: dict containig random message
        """
        try:
            response = requests.get('http://whatthecommit.com/index.txt')
            content = response.content.decode('utf-8')
        except requests.exceptions.RequestException as e:
            content = None

        data = {"message": content}

        return data

    def success(self):
        """ Runs after the template rendering has finished """
        pass