from flask import Flask
from common.middleware import middleware
from settings.config.database import connect_to_db
from settings.register_blueprint import register_blueprint
from .views import global_errorhandler, homepage


def create_app():
    app = Flask(__name__)
    app = connect_to_db(app)
    app = register_blueprint(app)
    homepage(app)
    middleware(app)
    global_errorhandler(app)
    # app = connect_to_mongodb(app)

    return app
