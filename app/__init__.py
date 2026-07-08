from flask import Flask
from flask_cors import CORS
from app.user.routes import user_bp
from app.category.routes import category_bp
from app.movement.routes import movement_bp
from app.dashboard.routes import dashboard_bp
from app.contact.routes import contact_bp
from app.appstats.routes import appstats_bp

def create_app():
    app = Flask(__name__)

    CORS(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(movement_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(appstats_bp)

    return app