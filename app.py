from cs50 import SQL
from flask import Flask, render_template
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

from decouple import config

from index import home_bp 
from auth import auth_bp
from builder import builder_bp
from respond import respond_bp
from models import db,User

app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config.from_mapping(
    SECRET_KEY='SECRET_KEY',
    SESSION_PERMANENT=False,
    SESSION_TYPE='filesystem',
    WTF_CSRF_ENABLED=True,
    WTF_CSRF_TIME_LIMIT=None
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# app.config["SECRET_KEY"] = "your_secret_key_change_this_in_production"  # Make sure this is set
# app.config['WTF_CSRF_ENABLED'] = True

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
    return User.query.get(str(user_id)) 

# Register blueprints
app.register_blueprint(auth_bp) 
app.register_blueprint(home_bp, url_prefix='/') 
app.register_blueprint(builder_bp)
app.register_blueprint(respond_bp)



db.init_app(app) 

with app.app_context():
    db.create_all()
    db.session.execute(text("PRAGMA foreign_keys = ON;"))  # Wrap with text()
    db.session.commit()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Add CSRF token to all templates
@app.context_processor
def inject_csrf_token():
    from flask_wtf.csrf import generate_csrf
    return dict(csrf_token=generate_csrf)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    try:
        return render_template('404.html'), 404
    except Exception as e:
        # Fallback if template rendering fails
        return '''
        <html>
        <head><title>404 - Page Not Found</title></head>
        <body>
            <h1>404 - Page Not Found</h1>
            <p>The page you're looking for doesn't exist.</p>
            <a href="/">Go Home</a>
        </body>
        </html>
        ''', 404

@app.errorhandler(500)
def internal_error(error):
    try:
        return render_template('500.html'), 500
    except Exception as e:
        # Fallback if template rendering fails
        return '''
        <html>
        <head><title>500 - Internal Server Error</title></head>
        <body>
            <h1>500 - Internal Server Error</h1>
            <p>Something went wrong on our end. We're working to fix this issue.</p>
            <a href="/">Go Home</a>
        </body>
        </html>
        ''', 500


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host=config('HOST'), port=config('PORT'))