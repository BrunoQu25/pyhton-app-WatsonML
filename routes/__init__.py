from .watson import watson_routes

def init_app(app):
    app.register_blueprint(watson_routes)