from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import User, db
from forms import LoginForm, RegisterForm, ChangePasswordForm
from werkzeug.security import generate_password_hash


auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/register" ,methods = ["GET","POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if User.query.filter_by(username=form.username.data).first():
                flash('Username already exists.', 'danger')
                return redirect(url_for('auth.register'))
            
            # Generate unique ID for new user
            from models import generate_random_id
            user_id = generate_random_id()
            while User.query.get(user_id):  # Ensure uniqueness
                user_id = generate_random_id()
                
            user = User(id=user_id, username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Registration successful!', 'success')
            return redirect(url_for('auth.login'))
        else:
            # Validation failed, fall through to render template
            pass
    return render_template("register.html", form=form)
        

@auth_bp.route("/login" ,methods = ["GET","POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Login successful!', 'success')
                return redirect('/')
            else:
                flash('Invalid username or password', 'error')
        # If validation fails or login fails, fall through to render template
    return render_template("login.html", form=form)



@auth_bp.route("/logout" ,methods = ["GET"])
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login'))



@auth_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password"""
    form = ChangePasswordForm()
    
    if request.method == 'GET':
        return render_template('change_password.html', form=form)
    
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data): 
            current_user.password_hash = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect('/') 
        else:
            flash('Current password is incorrect', 'error')
    
    return render_template('change_password.html', form=form)
