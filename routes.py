from datetime import datetime
from functools import wraps
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models import db, User, Branch
from werkzeug.security import generate_password_hash, check_password_hash

# ✅ Define the Blueprint properly
routes_bp = Blueprint("routes", __name__)

# ✅ Debugging: Log when routes.py loads
print("🔹 routes.py loaded successfully")

# Authentication decorator
def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('You must be logged in to view this page!', 'error')
            return redirect(url_for('routes.login'))  # ✅ Blueprint reference fixed
        return func(*args, **kwargs)
    return wrapper

# ✅ Debugging: Ensure this route works
@routes_bp.route("/")
def index():
    print("🔹 index() route called")
    return redirect(url_for('routes.login'))  # ✅ Fixed Blueprint reference

# ✅ Login route
@routes_bp.route("/login", methods=['GET', 'POST'])
def login():
    print("🔹 login() route called")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if not user:
            flash('User not found!', 'error')
            return redirect(url_for('routes.login'))

        if not check_password_hash(user.password, password):
            flash('Incorrect password!', 'error')
            return redirect(url_for('routes.login'))

        session['user_id'] = user.id
        flash('Login successful!', 'success')
        return redirect(url_for('routes.index'))

    return render_template('login.html')

# ✅ Register route (with debugging)
@routes_bp.route("/register", methods=['GET', 'POST'])
def register():
    print("🔹 register() route called")  # Debugging

    try:
        branches = Branch.query.all()
    except Exception as e:
        print(f"⚠️ Database error fetching branches: {e}")
        branches = []  # Prevent crashing if database query fails

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        dob = request.form['dob'].strip()
        branch_id = request.form.get('branch_id')

        if not username or not password:
            flash('Username and Password cannot be empty!', 'error')
            return redirect(url_for('routes.register'))  # ✅ Fixed reference

        if User.query.filter_by(username=username).first():
            flash('User already exists!', 'error')
            return redirect(url_for('routes.register'))

        user = User(
            username=username,
            name=name,
            email=email,
            dob=datetime.strptime(dob, '%Y-%m-%d'),
            branch_id=int(branch_id) if branch_id else None  
        )
        user.password = generate_password_hash(password)

        db.session.add(user)
        db.session.commit()

        flash('User registered successfully!', 'success')
        return redirect(url_for('routes.login'))

    return render_template('register.html', branches=branches)

# ✅ Logout route
@routes_bp.route("/logout")
def logout():
    session.pop('user_id', None)
    flash("Logged out successfully!", "success")
    return redirect(url_for('routes.index'))
