from flask import current_app, Flask, redirect, url_for

def create_app(config):
    """
    Creates and returns app using flask app factory model.
    """
    app = Flask(__name__)
    app.config.from_object(config)

    # Setup the data model.
    with app.app_context():
        model = get_model()

    # Register the Movie Reviews blueprint.
    from .views import views
    app.register_blueprint(views)

    @app.route("/")
    def index():
        language = 'en'
        return redirect(url_for('views.main', language=language))

    return app


def get_model():
    """
    Imports and returns datastore model.
    """
    model_backend = current_app.config['DATA_BACKEND']
    if model_backend == 'datastore':
        from . import model_datastore
        model = model_datastore
    else:
        raise ValueError("No appropriate databackend configured. ")

    return model
