from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, TextAreaField, SelectField, IntegerField, DateTimeLocalField
from wtforms.validators import Email, Length, EqualTo, DataRequired

# -------------------- User Forms --------------------

class RegisterForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    fullname = StringField('Full Name')
    qualification = StringField('Qualification')
    dob = DateField('Date of Birth', format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField('Submit')

class UserDetailsForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired(), Email()])
    fullname = StringField('Full Name')
    qualification = StringField('Qualification')
    dob = DateField('Date of Birth', format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField('Submit')

class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Submit')

# -------------------- Admin CRUD Forms --------------------

class BranchForm(FlaskForm):
    name = StringField('Branch Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SubjectForm(FlaskForm):
    name = StringField('Subject Name', validators=[DataRequired()])
    branch_id = SelectField('Branch', coerce=int, validators=[DataRequired()])  # Fix
    submit = SubmitField('Submit')

class ChapterForm(FlaskForm):
    name = StringField('Chapter Name', validators=[DataRequired()])
    subject_id = SelectField('Subject', coerce=int, validators=[DataRequired()])  # Fix
    submit = SubmitField('Submit')

class QuizForm(FlaskForm):
    name = StringField('Quiz Name', validators=[DataRequired()])
    chap_id = SelectField('Chapter', coerce=int, validators=[DataRequired()])  # Fix
    subject_id = SelectField('Subject', coerce=int, validators=[DataRequired()])  # Fix
    nos = IntegerField('Number of Questions', validators=[DataRequired()])  # Fix
    time_duration = IntegerField('Time Duration (In seconds)')
    submit = SubmitField('Submit')

class QuestionForm(FlaskForm):
    question = TextAreaField('Question', validators=[DataRequired()])  # Fix name
    option1 = StringField('Option 1', validators=[DataRequired()])
    option2 = StringField('Option 2', validators=[DataRequired()])
    option3 = StringField('Option 3', validators=[DataRequired()])
    option4 = StringField('Option 4', validators=[DataRequired()])
    ans = StringField('Correct Answer', validators=[DataRequired()])  # Fix type
    marks = IntegerField('Marks', validators=[DataRequired()])
    submit = SubmitField('Save')
