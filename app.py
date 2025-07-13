from flask import Flask
from src.config.database import config_db
from src.routes import register_blueprints


def create_app():
    app = Flask(__name__)

    config_db(app)

    register_blueprints(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
