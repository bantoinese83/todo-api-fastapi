from app.core.cors_config import configure_cors


def configure_middlewares(app):
    configure_cors(app)
