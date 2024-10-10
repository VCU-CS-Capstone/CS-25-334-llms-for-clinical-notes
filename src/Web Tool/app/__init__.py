from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Load configurations

    # Import and register blueprints/routes here
    from .routes import main
    app.register_blueprint(main)

    return app