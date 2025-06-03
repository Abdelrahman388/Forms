"""
Authentication blueprint for login, registration, logout, and theme toggling.
"""
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from models import User
from forms import LoginForm, RegisterForm, ChangePasswordForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user"""
    form = RegisterForm()
    
    if request.method == 'GET':
        return render_template('register.html', form=form)
    
    if form.validate_on_submit():
        try:
            user = User.create(form.username.data, form.password.data)
            login_user(user)
            flash('Registration successful!', 'success')
            return redirect(url_for('main.index'))
        except ValueError as e:
            flash(str(e), 'error')
    
    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login user"""
    form = LoginForm()
    
    if request.method == 'GET':
        return render_template('login.html', form=form)
    
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """Logout user"""
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
        from flask_login import current_user
        if current_user.check_password(form.current_password.data):
            # Update password in database
            from models import db
            from werkzeug.security import generate_password_hash
            db.execute("UPDATE users SET hash = ? WHERE id = ?", 
                      generate_password_hash(form.new_password.data), current_user.id)
            flash('Password changed successfully!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Current password is incorrect', 'error')
    
    return render_template('change_password.html', form=form)


@auth_bp.route('/toggle_theme', methods=['POST'])
def toggle_theme():
    """Toggle night mode theme"""
    current_mode = session.get('night_mode', False)
    session['night_mode'] = not current_mode
    new_mode = 'dark' if session['night_mode'] else 'light'
    
    if request.is_json or request.headers.get('Content-Type') == 'application/json':
        return jsonify({'success': True, 'mode': new_mode})
    
    return redirect(request.referrer or url_for('main.index'))
