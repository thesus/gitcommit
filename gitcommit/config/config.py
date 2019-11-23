import configparser

def get_config(path):
    """Returns the config. Can be used like a dict."""
    config = configparser.ConfigParser()
    config.read(path)
    return config
