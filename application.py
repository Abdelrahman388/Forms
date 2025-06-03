"""
Main application factory and entry point for the Forms application.
This file replaces the old app.py with a modern Flask structure using blueprints.
"""
from flask import Flask, render_template
from flask_login import LoginManager
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
import os

from models import User
from auth import auth_bp
from main import main_bp
from builder import builder_bp
from respond import respond_bp


def create_app(test_config=None):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configure application
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-key-change-in-production'),
        SESSION_PERMANENT=False,
        SESSION_TYPE='filesystem',
        WTF_CSRF_ENABLED=True,
        WTF_CSRF_TIME_LIMIT=None
    )
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
      # Initialize extensions
    Session(app)
    csrf = CSRFProtect(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(int(user_id))
    
    # Register blueprints
    app.register_blueprint(auth_bp)  # No URL prefix for auth routes
    app.register_blueprint(main_bp)
    app.register_blueprint(builder_bp)
    app.register_blueprint(respond_bp)
      # Add CSRF token to all templates
    @app.context_processor
    def inject_csrf_token():
        from flask_wtf.csrf import generate_csrf
        return dict(csrf_token=generate_csrf)
    
    # Cache control
    @app.after_request
    def after_request(response):
        """Ensure responses aren't cached"""
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response
      # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500
    
    return app


# Create the application instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
