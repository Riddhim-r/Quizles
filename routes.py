from flask import render_template
from app import app

@app.route('/')  # Define route directly
def index():
    return render_template('index.html')

@app.route('/login')  # Define another route for login
def login():
    return render_template('login.html')
