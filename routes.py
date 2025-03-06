from flask import render_template, request, flash, redirect, url_for
from app import app
from models import User

@app.route('/')  # Define route directly
def index():
    return render_template('index.html')

@app.route('/login')  # Define another route for login
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])  # Define route for login with POST method
def login_post():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User not found!')
        return redirect(url_for('login'))
    if not user.check_password(password):
        flash('Incorrect password!')
        return redirect(url_for('login'))
    #if the user is found and password is correct
    return redirect(url_for('index'))

@app.route('/register')  # Define another route for register
def register():
    return render_template('register.html')