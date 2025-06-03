"""
Flask-WTF forms for the Forms application.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from models import User


class LoginForm(FlaskForm):
    """Login form"""
    username = StringField('Username', validators=[DataRequired()], 
                          render_kw={"class": "form-control mx-auto w-auto", 
                                   "placeholder": "Username", "autofocus": True})
    password = PasswordField('Password', validators=[DataRequired()],
                           render_kw={"class": "form-control mx-auto w-auto", 
                                    "placeholder": "Password"})


class RegisterForm(FlaskForm):
    """Registration form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)],
                          render_kw={"class": "form-control mx-auto w-auto", 
                                   "placeholder": "Username", "autofocus": True})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)],
                           render_kw={"class": "form-control mx-auto w-auto", 
                                    "placeholder": "Password"})
    confirmation = PasswordField('Confirm Password', 
                                validators=[DataRequired(), EqualTo('password', message='Passwords must match')],
                                render_kw={"class": "form-control mx-auto w-auto", 
                                         "placeholder": "Confirm Password"})

    def validate_username(self, username):
        """Check if username already exists"""
        user = User.get_by_username(username.data)
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')


class FormDetailsForm(FlaskForm):
    """Form for creating/editing form details"""
    name = StringField('Form Name', validators=[DataRequired()],
                      render_kw={"class": "form-control mx-auto w-auto d-inline-block", 
                               "placeholder": "Enter form name"})
    title = StringField('Form Title', validators=[DataRequired()],
                       render_kw={"class": "form-control mx-auto w-auto d-inline-block", 
                                "placeholder": "Enter form title"})


class QuestionForm(FlaskForm):
    """Form for creating/editing questions"""
    question = StringField('Question', validators=[DataRequired()],
                          render_kw={"class": "form-control mx-auto w-75 d-inline-block", 
                                   "placeholder": "Write a Question"})
    answer_type = SelectField('Answer Type', 
                             choices=[('', 'Answer type'), ('text', 'Text'), 
                                    ('radio', 'Radio'), ('checkbox', 'Checkbox')],
                             validators=[DataRequired()],
                             render_kw={"class": "form-select form-select-sm"})


class OptionForm(FlaskForm):
    """Form for creating/editing options"""
    option = StringField('Option', validators=[DataRequired()],
                        render_kw={"class": "form-control mx-auto w-25", 
                                 "placeholder": "Write Option"})


class ChangePasswordForm(FlaskForm):
    """Form for changing password"""
    current_password = PasswordField('Current Password', validators=[DataRequired()],
                                   render_kw={"class": "form-control mx-auto w-auto", 
                                            "placeholder": "Current Password"})
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)],
                               render_kw={"class": "form-control mx-auto w-auto", 
                                        "placeholder": "New Password"})
    confirm_password = PasswordField('Confirm New Password', 
                                   validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')],
                                   render_kw={"class": "form-control mx-auto w-auto", 
                                            "placeholder": "Confirm New Password"})
    submit = SubmitField('Change Password', render_kw={"class": "btn btn-primary"})
