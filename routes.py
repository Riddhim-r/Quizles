from datetime import datetime
from functools import wraps
from flask import render_template, request, flash, redirect, url_for, session
from models import db, User, Branch
from werkzeug.security import generate_password_hash, check_password_hash 
from app import app # Ensure correct password handling

with app.app_context():
    branches = Branch.query.all()  
    
# Authentication decorator
def authenticate(func):   
    @wraps(func)
    def wrapper(*args, **kwargs): 
        if 'user_id' not in session: 
            flash('You must be logged in to view this page!', 'error')
            return redirect(url_for('login'))   
        return func(*args, **kwargs)    
    return wrapper

# Homepage route (Protected)
@app.route('/')  
@authenticate
def index():
    return render_template('index.html', user=User.query.get(session['user_id']))  


# Login route
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
        
        session['user_id'] = user.id  # Store user ID in session
        flash('Login successful!', 'success')
        return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        dob = request.form['dob'].strip()
        branch_id = request.form.get('branch_id')

        if not username or not password:
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
            branch_id=int(branch_id) if branch_id else None  
        )
        user.password = generate_password_hash(password)  

        with app.app_context():
            db.session.add(user)
            db.session.commit()

        flash('User registered successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', branches=branches)


# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)  
    flash("Logged out successfully!", "success")
    return redirect(url_for('index'))
