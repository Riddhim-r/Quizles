from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, TextAreaField, SelectField, IntegerField, DateTimeLocalField
from wtforms.validators import Email, Length, EqualTo, DataRequired

# -------------------- User Forms --------------------

class RegisterForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    name = StringField('Full Name', validators=[DataRequired()])
    branch_id = SelectField('Branch', validators=[DataRequired()])  # Dropdown for branches
    submit = SubmitField('Submit')


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    branch_id = SelectField('Branch', validators=[DataRequired()])
    
    submit = SubmitField('Submit')

class UserDetailsForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name')
    qualification = StringField('Qualification')
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
    branch_id = SelectField('Branch', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')


class ChapterForm(FlaskForm):
    name = StringField('Chapter Name', validators=[DataRequired()])
    subject_id = SelectField('Subject', coerce=int, validators=[DataRequired()])  # Dropdown for subject selection
    submit = SubmitField('Submit')


class QuizForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])  # Standardized field name
    chapter_id = SelectField('Chapter', coerce=int, validators=[DataRequired()])
    nos = IntegerField('Number of Questions', validators=[DataRequired()])
    time_duration = IntegerField('Time Duration (In seconds)')
    submit = SubmitField('Submit')

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

class QuestionForm(FlaskForm):
    quiz_id = SelectField('Quiz', coerce=int, validators=[DataRequired()])
    question_text = StringField('Question Text', validators=[DataRequired()])
    option1 = StringField('Option 1', validators=[DataRequired()])
    option2 = StringField('Option 2', validators=[DataRequired()])
    option3 = StringField('Option 3', validators=[DataRequired()])
    option4 = StringField('Option 4', validators=[DataRequired()])
    correct_option = IntegerField('Correct Option', validators=[DataRequired()])
    marks = IntegerField('Marks', default=1, validators=[DataRequired()])
    submit = SubmitField('Save')

