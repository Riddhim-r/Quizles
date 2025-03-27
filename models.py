from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    passhash = db.Column(db.String(200), nullable=False)  # ⪼ Keep only this for passwords
    name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=True)
    scores = db.relationship('Scores', backref='user', lazy=True)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        """Hash the password before storing it."""
        self.passhash = generate_password_hash(password)  # ⪼ Save hash in passhash

    def check_password(self, password):
        """Verify the password."""
        return check_password_hash(self.passhash, password)  # ⪼ Use passhash



class Branch(db.Model):
    __tablename__ = 'branch'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    desc = db.Column(db.String(500), nullable=False)

    users = db.relationship('User', backref='branch', lazy=True)
    subjects = db.relationship('Subject', backref='branch', lazy=True)


class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=True)

    chapters = db.relationship('Chapters', backref='subject', lazy=True)
    quizzes = db.relationship('Quiz', backref='subject', lazy=True)


class Chapters(db.Model):
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True)
    sub_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    desc = db.Column(db.String(500), nullable=False)

    quiz = db.relationship('Quiz', backref='chapter', lazy=True)


class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key=True)
    chap_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    nos = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False)

    questions = db.relationship('Questions', backref='quiz', lazy=True)
    scores = db.relationship('Scores', backref='quiz', lazy=True)


class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question = db.Column(db.String(500), nullable=False)
    option1 = db.Column(db.String(100), nullable=False)
    option2 = db.Column(db.String(100), nullable=False)
    option3 = db.Column(db.String(100), nullable=False)
    option4 = db.Column(db.String(100), nullable=False)
    ans = db.Column(db.String(100), nullable=False)
    marks = db.Column(db.Integer, nullable=False)


class Scores(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
