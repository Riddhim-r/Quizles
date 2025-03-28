from functools import wraps
from flask import Blueprint, render_template, redirect, flash, request, url_for
from flask_login import current_user, login_required
from app import db
from forms import BranchForm, SubjectForm, ChapterForm, QuizForm, QuestionForm
from models import Branch, Subject, Chapter, Quiz, Question


admin_bp = Blueprint('admin', __name__)

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
