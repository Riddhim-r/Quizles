from functools import wraps
from flask import Blueprint, render_template, redirect, flash, request, url_for
from flask_login import current_user, login_required
from app import db
from forms import BranchForm, SubjectForm, ChapterForm, QuizForm, QuestionForm, UserForm
from models import Branch, Subject, Chapter, Quiz, Question, User


admin_bp = Blueprint('admin', __name__)
users_bp = Blueprint('users', __name__)

# Middleware to check admin access
def admin_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return login_required(func)(*args, **kwargs)
        if not current_user.is_admin:
            flash("You don't have permission to access this page", category="error")
            return redirect(url_for("home"))
        return func(*args, **kwargs)
    return decorated_view

# Generic CRUD handler
@admin_bp.route("/admin/manage/<string:model>", methods=['GET', 'POST'])
@admin_login_required
def handle_crud(model):
    # Model mapping dictionary
    model_map = {
        "branches": Branch,
        "subjects": Subject,
        "chapters": Chapter,
        "quizzes": Quiz,
        "questions": Question
    }
    
    form_map = {
        "branches": BranchForm,
        "subjects": SubjectForm,
        "chapters": ChapterForm,
        "quizzes": QuizForm,
        "questions": QuestionForm
    }

    if model not in model_map:
        flash("Invalid model!", category="error")
        return redirect(url_for("admin.dashboard"))

    ModelClass = model_map[model]  # Get the model class
    FormClass = form_map[model]    # Get the form class
    items = ModelClass.query.all()  # Fetch all records
    query = request.form.get('query', '')

    # Search functionality
    if request.method == 'POST':
        items = ModelClass.query.filter(ModelClass.name.ilike(f"%{query}%")).all()

    return render_template(f"admin/{model}/manage.html", items=items, query=query, model=model)

# Generic Add/Edit Function
@admin_bp.route("/admin/<string:model>/edit/<int:id>", methods=['GET', 'POST'])
@admin_bp.route("/admin/<string:model>/add", methods=['GET', 'POST'])
@admin_login_required
def add_edit_item(model, id=None):
    model_map = {
        "branches": Branch,
        "subjects": Subject,
        "chapters": Chapter,
        "quizzes": Quiz,
        "questions": Question
    }
    
    form_map = {
        "branches": BranchForm,
        "subjects": SubjectForm,
        "chapters": ChapterForm,
        "quizzes": QuizForm,
        "questions": QuestionForm
    }

    if model not in model_map:
        flash("Invalid model!", category="error")
        return redirect(url_for("admin.dashboard"))

    ModelClass = model_map[model]
    FormClass = form_map[model]

    item = ModelClass.query.get(id) if id else None
    form = FormClass(obj=item)

    if form.validate_on_submit():
        if not item:
            item = ModelClass()
            db.session.add(item)
        
        for field in form.data:
            if field != 'csrf_token':  # Ignore CSRF field
                setattr(item, field, form.data[field])

        db.session.commit()
        flash(f"{model.capitalize()} {'updated' if id else 'added'} successfully!", category="success")
        return redirect(url_for("admin.handle_crud", model=model))

    return render_template(f"admin/{model}/edit.html", form=form, model=model)


#Inline Editing Support
@admin_bp.route("/admin/<string:model>/edit/<int:id>", methods=['POST'])
@admin_login_required
def edit_item_inline(model, id):
    model_map = {
        "branches": Branch,
        "subjects": Subject,
        "chapters": Chapter,
        "quizzes": Quiz,
        "questions": Question
    }

    if model not in model_map:
        return "Invalid model!", 400

    ModelClass = model_map[model]
    item = ModelClass.query.get_or_404(id)

    for field in request.form:
        setattr(item, field, request.form[field])  # Dynamically update fields

    db.session.commit()
    return "", 204  # Return empty response for inline edit


# Generic Delete Function
@admin_bp.route("/admin/<string:model>/delete/<int:id>", methods=['POST'])
@admin_login_required
def delete_item(model, id):
    model_map = {
        "branches": Branch,
        "subjects": Subject,
        "chapters": Chapter,
        "quizzes": Quiz,
        "questions": Question
    }

    if model not in model_map:
        flash("Invalid model!", category="error")
        return redirect(url_for("admin.dashboard"))

    ModelClass = model_map[model]
    item = ModelClass.query.get_or_404(id)
    
    db.session.delete(item)
    db.session.commit()
    flash(f"{model.capitalize()} deleted successfully!", category="success")
    return redirect(url_for("admin.handle_crud", model=model))

# Manage Users Page
@users_bp.route("/admin/manage/users", methods=['GET', 'POST'])
@admin_login_required
def manage_users():
    users = User.query.all()
    query = request.form.get('query', '')

    # Search Functionality
    if request.method == 'POST':
        users = User.query.filter(User.username.ilike(f"%{query}%")).all()

    return render_template("admin/users/manage.html", users=users, query=query)

# Add or Edit User
@users_bp.route("/admin/users/edit/<int:id>", methods=['GET', 'POST'])
@users_bp.route("/admin/users/add", methods=['GET', 'POST'])
@admin_login_required
def add_edit_user(id=None):
    user = User.query.get(id) if id else None
    form = UserForm(obj=user)

    if form.validate_on_submit():
        if not user:
            user = User()
            db.session.add(user)
        
        for field in form.data:
            if field != 'csrf_token':
                setattr(user, field, form.data[field])

        db.session.commit()
        flash(f"User {'updated' if id else 'added'} successfully!", category="success")
        return redirect(url_for("users.manage_users"))

    return render_template("admin/users/edit.html", form=form)

# Inline Editing for Users
@users_bp.route("/admin/users/edit/<int:id>", methods=['POST'])
@admin_login_required
def edit_user_inline(id):
    user = User.query.get_or_404(id)

    for field in request.form:
        setattr(user, field, request.form[field])

    db.session.commit()
    return "", 204  # Empty response for inline edit

# Delete User
@users_bp.route("/admin/users/delete/<int:id>", methods=['POST'])
@admin_login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully!", category="success")
    return redirect(url_for("users.manage_users"))









