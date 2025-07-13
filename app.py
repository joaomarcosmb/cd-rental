from flask import Flask
from src.config.database import config_db
from src.config.api import api
from src.routes import register_namespaces


def create_app():
    app = Flask(__name__)

    config_db(app)

    api.init_app(app)

    register_namespaces(api)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)
