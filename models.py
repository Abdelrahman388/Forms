from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import random
import string

try:
    from app import db
except ImportError:
    db = SQLAlchemy()

def generate_random_id():
    """Generate a random 8-character alphanumeric ID"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.String(8), primary_key=True, default=generate_random_id)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def toJson(self):
        return {
            'id': self.id,
            'username': self.username
        }

class Form(db.Model):
    __tablename__ = "forms"
    id = db.Column(db.String(8), primary_key=True, default=generate_random_id)
    name = db.Column(db.String, default="")
    title = db.Column(db.String, default="")
    description = db.Column(db.String, default="")
    questionCount = db.Column(db.Integer, default=0)
    createdAt = db.Column(db.String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    responsesCount = db.Column(db.Integer, default=0)
    userId = db.Column(db.String(8), db.ForeignKey('users.id'))
    questions = db.relationship('Question', backref='form', cascade="all, delete-orphan", lazy=True)
    options = db.relationship('Option', backref='form', cascade="all, delete-orphan", lazy=True)
    responses = db.relationship('Response', backref='form', cascade="all, delete-orphan", lazy=True)

    def toJson(self):
        return {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'questionCount': self.questionCount,
            'createdAt': self.createdAt,
            'responsesCount': self.responsesCount,
            'userId': self.userId
        }

class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.String(8), primary_key=True, default=generate_random_id)
    text = db.Column(db.String, default="")
    answerType = db.Column(db.String, default="")
    optionCount = db.Column(db.Integer, default=0)
    formId = db.Column(db.String(8), db.ForeignKey('forms.id'))
    saved = db.Column(db.Boolean, default=False)
    options = db.relationship('Option', backref='question', cascade="all, delete-orphan", lazy=True)
    responses = db.relationship('Response', backref='question', cascade="all, delete-orphan", lazy=True)

    def toJson(self):
        return {
            'id': self.id,
            'text': self.text,
            'answerType': self.answerType,
            'optionCount': self.optionCount,
            'formId': self.formId,
            'saved': self.saved
        }

class Option(db.Model):
    __tablename__ = "options"
    id = db.Column(db.String(8), primary_key=True, default=generate_random_id)
    text = db.Column(db.String, default="")
    questionId = db.Column(db.String(8), db.ForeignKey('questions.id'))
    formId = db.Column(db.String(8), db.ForeignKey('forms.id'))

    def toJson(self):
        return {
            'id': self.id,
            'text': self.text,
            'questionId': self.questionId,
            'formId': self.formId
        }

class Responder(db.Model):
    __tablename__ = "responders"
    id = db.Column(db.String(8), primary_key=True, default=generate_random_id)
    name = db.Column(db.String, nullable=False)
    responses = db.relationship('Response', backref='responder', cascade="all, delete-orphan", lazy=True)

    def toJson(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Response(db.Model):
    __tablename__ = "responses"
    id = db.Column(db.String(8), primary_key=True, default=generate_random_id)
    answer = db.Column(db.Text, default="")
    createdAt = db.Column(db.String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    questionId = db.Column(db.String(8), db.ForeignKey('questions.id'))
    formId = db.Column(db.String(8), db.ForeignKey('forms.id'))
    responderId = db.Column(db.String(8), db.ForeignKey('responders.id'))

    def toJson(self):
        return {
            'id': self.id,
            'answer': self.answer,
            'createdAt': self.createdAt,
            'questionId': self.questionId,
            'formId': self.formId,
            'responderId': self.responderId
        }

def init_db():
    db.create_all()
