from datetime import datetime
from functools import wraps
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models import db, User, Branch
from werkzeug.security import generate_password_hash, check_password_hash

# ✅ Define the Blueprint properly
routes_bp = Blueprint("routes", __name__)

# Authentication decorator
def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('You must be logged in to view this page!', 'error')
            return redirect(url_for('routes.login'))  
        return func(*args, **kwargs)
    return wrapper

@routes_bp.route("/")
def index():
    return redirect(url_for('routes.login'))  

# ✅ Login route
@routes_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if not user:
            flash('User not found!', 'error')
            return redirect(url_for('routes.login'))

        # ✅ Use check_password() method instead of directly accessing `passhash`
        if not user.check_password(password):
            flash('Incorrect password!', 'error')
            return redirect(url_for('routes.login'))
        
         # If the user is an admin, redirect to the admin homepage
        if user.is_admin:
            session['user_id'] = user.id
            flash('Admin login successful!', 'success')
            return redirect(url_for('routes.admin_home'))

        #otherwise, redirect to the user homepage
        session['user_id'] = user.id
        flash('Login successful!', 'success')
        return redirect(url_for('routes.index'))

    return render_template('login.html')

# ✅ Admin homepage route (accessible only after successful admin login)
@routes_bp.route('/admin-home')
def admin_home():
    # Check if the logged-in user is an admin
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in to access the admin dashboard!', 'error')
        return redirect(url_for('routes.login'))

    user = User.query.get(user_id)
    if not user or not user.is_admin:
        flash('Access restricted. Admins only!', 'error')
        return redirect(url_for('routes.index'))

    return render_template('admin/admin_home.html')  # Render the admin homepage (from templates/admin)

# ✅ Register route (with debugging)
@routes_bp.route("/register", methods=['GET', 'POST'])
def register():
    branches = Branch.query.all()

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        dob = request.form['dob'].strip()
        branch_id = request.form.get('branch_id')

        if not username or not password:
            flash('Username and Password cannot be empty!', 'error')
            return redirect(url_for('routes.register'))

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
        
        user.password = password  # ✅ This will trigger the setter method

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
