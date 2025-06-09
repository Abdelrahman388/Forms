from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], 
                          render_kw={"class": "form-control mx-auto w-auto", 
                                   "placeholder": "", "autofocus": True})
    password = PasswordField('Password', validators=[DataRequired()],
                           render_kw={"class": "form-control mx-auto w-auto", 
                                    "placeholder": ""})


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)],
                          render_kw={"class": "form-control mx-auto w-auto", 
                                   "placeholder": "", "autofocus": True})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)],
                           render_kw={"class": "form-control mx-auto w-auto", 
                                    "placeholder": ""})
    confirmation = PasswordField('Confirm Password', 
                                validators=[DataRequired(), EqualTo('password', message='Passwords must match')],
                                render_kw={"class": "form-control mx-auto w-auto", 
                                         "placeholder": ""})

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()],
                                   render_kw={"class": "form-control mx-auto w-auto", 
                                            "placeholder": ""})
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)],
                               render_kw={"class": "form-control mx-auto w-auto", 
                                        "placeholder": ""})
    confirm_password = PasswordField('Confirm New Password', 
                                   validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')],
                                   render_kw={"class": "form-control mx-auto w-auto", 
                                            "placeholder": ""})
    submit = SubmitField('Change Password', render_kw={"class": "btn btn-primary"})
