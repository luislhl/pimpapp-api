from flask import Flask
from app import config


def create_app(config_name):
    """TODO: Docstring for create_app.

    :config_name: TODO
    :returns: TODO

    """

    app = Flask(__name__)
    config.config[config_name](app)

    return app