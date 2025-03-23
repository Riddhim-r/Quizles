from datetime import datetime
from functools import wraps
from flask import render_template, request, flash, redirect, url_for, session 
from app import app
from models import db, User

def authenticate(func):   
    @wraps(func)
    def wrapper(*args, **kwargs): 
        if 'user_id' not in session: 
            flash('You must be logged in to view this page!', 'error')
            return redirect(url_for('login'))   
        return func(*args, **kwargs)    
    return wrapper

@app.route('/')  # this is a decorator(wrap a function and modify its behavior)
@authenticate
def index():
    return render_template('index.html', user=User.query.get(session['user_id'])) # <-- pass the user object to the template and show the user name on the page

@app.route('/profile')
@authenticate
def profile():
    return render_template('profile.html', user=User.query.get(session['user_id']))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if not user:
            flash('User not found!', 'error')
            return redirect(url_for('login'))
        if not user.check_password(password):
            flash('Incorrect password!', 'error')
            return redirect(url_for('login'))
        session['user_id'] = user.id  # <-- move inside POST block
        flash('Login successful!', 'success')
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    from models import Branch  # Ensure Branch model is accessible

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        dob = request.form['dob']
        branch_id = request.form['branch_id']

        if not username.strip() or not password.strip():
            flash('Username and Password cannot be empty!', 'error')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash('User already exists!', 'error')
            return redirect(url_for('register'))

        user = User(
            username=username,
            name=name,
            email=email,
            dob=datetime.strptime(dob, '%Y-%m-%d'),
            branch_id=branch_id
        )
        user.password = password
        db.session.add(user)
        db.session.commit()
        flash('User registered successfully!', 'success')
        return redirect(url_for('login'))

    branches = Branch.query.all()
    return render_template('register.html', branches=branches)



@app.route('/logout')
def logout():
    session.pop('user_id', None) # remove the user_id from the session, effectively logging them out
    return redirect(url_for('index')) # redirecting them to the home page