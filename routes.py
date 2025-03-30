from datetime import time
from functools import wraps
from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import db, User, Branch, Subject, Chapter, Quiz, Question, Score
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import func, desc  

# ⪼ Define the Blueprint
routes_bp = Blueprint("routes", __name__)
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# ⪼ Admin authorization decorator (Ensures only admins can access admin routes)
def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Access restricted. Admins only!', 'error')
            return redirect(url_for('routes.index'))
        return func(*args, **kwargs)
    return wrapper

#first page after running the server
@routes_bp.route("/")
def index():
    return render_template('/index.html')  

# ⪼ Register route 
@routes_bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        branch_id = request.form['branch_id']  # Get selected branch

        if not username or not password:
            flash('Username and Password cannot be empty!', 'error')
            return redirect(url_for('routes.register'))

        if User.query.filter_by(username=username).first():
            flash('User already exists!', 'error')
            return redirect(url_for('routes.register'))

        user = User(username=username, name=name, email=email, branch_id=branch_id)
        user.set_password(password)  # Use the hashed password function

        db.session.add(user)
        db.session.commit()

        flash('User registered successfully!', 'success')
        return redirect(url_for('routes.login'))

    # Pass branches to template
    branches = Branch.query.all()  # Fetch all branches from DB
    return render_template('user/register.html', branches=branches)

# ⪼ Login route
@routes_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            flash('Invalid username or password!', 'error')
            return redirect(url_for('routes.login'))

        login_user(user)  #  Flask-Login handles session management
        print(f"User Logged In: {current_user.is_authenticated}, ID: {current_user.id}")

        flash("Login successful!", "success")
        return redirect(url_for('routes.homepage') if not user.is_admin else url_for('admin.admin_home'))

    return render_template('user/login.html')

#test which branch id of the current user
@routes_bp.route("/test_branch")
@login_required
def test_branch():
    return f"Current User Branch ID: {current_user.branch_id}"


#----------------------------------------------- User routes-----------------------------------------------------

#after login, this will be the 1st page
@routes_bp.route("/homepage", methods=["GET", "POST"])
@login_required
def homepage():
    quizzes = Quiz.query.join(Subject).filter(Subject.branch_id == current_user.branch_id).all()

    if request.method == "POST":
        quiz_id = request.form.get("quiz_id")
        if quiz_id:
            return redirect(url_for("routes.start_quiz", quiz_id=quiz_id))

    return render_template('user/homepage.html', username=current_user.username, quizzes=quizzes)


# ⪼ user profile route
@routes_bp.route("/profile", methods=['GET'])
@login_required
def profile():
    # Fetch the top 1 subject with the highest score
    subject_scores = (
        db.session.query(Subject.name.label("subject"), func.sum(Score.score).label("score"))
        .join(Quiz, Quiz.id == Score.quiz_id)
        .join(Subject, Subject.id == Quiz.subject_id)
        .filter(Score.user_id == current_user.id)
        .group_by(Subject.name)
        .order_by(desc("score"))
        .limit(1)  # Fetch top 1 subject
        .all()
    )

    subject_scores = [{"subject": row.subject, "score": row.score} for row in subject_scores]

    # Fetch correct vs wrong questions
    quiz_stats = db.session.query(
        func.count(Score.id).label("attempted"),
        func.coalesce(func.sum(Score.score), 0).label("correct")
    ).filter(Score.user_id == current_user.id).first()

    if quiz_stats:
        correct_wrong_attempts = {
            "correct": quiz_stats.correct or 0,  # Handle None as 0
            "wrong": quiz_stats.attempted - (quiz_stats.correct or 0)
        }
    else:
        correct_wrong_attempts = {"correct": 0, "wrong": 0}  # Ensure it's always defined

    # Fetch the attempted quizzes and their scores
    quiz_attempts = db.session.query(Quiz.name.label("quiz_name"), Score.score).join(Quiz).filter(Score.user_id == current_user.id).all()

    quiz_attempts = [{"quiz_name": row.quiz_name, "score": row.score} for row in quiz_attempts]

    return render_template(
        "user/profile.html",
        subject_scores=subject_scores,
        correct_wrong_attempts=correct_wrong_attempts,
        quiz_attempts=quiz_attempts
    )

# ⪼ Logout route
@routes_bp.route("/logout", methods=['POST'])
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "success")
    return redirect(url_for('routes.index'))

#-----------------------------------------------Admin Blueprint and routes-----------------------------------------------------

# ⪼ Admin Dashboard_______________________________________________
@admin_bp.route("/dashboard")
@login_required
@admin_only
def admin_dashboard():
    users_count = User.query.count()
    quizzes_count = Quiz.query.count()
    
    # Users Count per Branch (Bar Chart)
    branch_users = db.session.query(User.branch, db.func.count(User.id)).group_by(User.branch).all()
    branch_users = [{"branch": row[0], "count": row[1]} for row in branch_users]

    # Total Quizzes Created per Branch (Pie Chart) - FIXED
    branch_quizzes = db.session.query(Branch.name, db.func.count(Quiz.id)) \
        .join(Subject, Quiz.subject_id == Subject.id) \
        .join(Branch, Subject.branch_id == Branch.id) \
        .group_by(Branch.name).all()
    branch_quizzes = [{"branch": row[0], "count": row[1]} for row in branch_quizzes]

    return render_template(
        'admin/admin_dashboard.html',
        users_count=users_count,
        quizzes_count=quizzes_count,
        branch_users=branch_users,
        branch_quizzes=branch_quizzes
    )

# ⪼ Admin Home___________________________________________________
@admin_bp.route("/admin_home")
@login_required
@admin_only
def admin_home():
    return render_template('admin/admin_home.html')

# ⪼ Admin search___________________________________________________
@routes_bp.route("/admin/search", methods=["GET"])
@login_required
def admin_search():
    query = request.args.get("q", "").strip()

    if not query:
        return render_template("admin/search.html", results=[])

    user_results = User.query.filter(User.name.ilike(f"%{query}%") | User.email.ilike(f"%{query}%")).all()
    subject_results = Subject.query.filter(Subject.name.ilike(f"%{query}%")).all()
    quiz_results = Quiz.query.filter(Quiz.name.ilike(f"%{query}%")).all()

    return render_template(
        "admin/search.html",
        query=query,
        user_results=user_results,
        subject_results=subject_results,
        quiz_results=quiz_results
    )


# ⪼ Manage Branches_________________________________________________
from forms import BranchForm  

@admin_bp.route("/manage_branch", methods=['GET', 'POST'])
@login_required
@admin_only
def manage_branch():
    form = BranchForm()
    branches = Branch.query.all()  # Fetch all branches

    # Get the branch_id for editing
    branch_id = request.args.get('branch_id')
    if branch_id:
        branch = Branch.query.get(branch_id)
        if branch:
            form.name.data = branch.name  # Populate the form for editing

    if request.method == 'POST':
        branch_name = request.form.get('name')

        if branch_id:  # Editing an existing branch
            branch = Branch.query.get(branch_id)
            if branch:
                branch.name = branch_name
                db.session.commit()
                flash("Branch details updated successfully!", "success")
        else:  # Adding a new branch
            new_branch = Branch(name=branch_name)
            db.session.add(new_branch)
            db.session.commit()
            flash("New branch added successfully!", "success")

        return redirect(url_for("admin.manage_branch"))

    # Handle deleting a branch
    delete_branch_id = request.args.get('delete_branch_id')
    if delete_branch_id:
        branch = Branch.query.get(delete_branch_id)
        if branch:
            db.session.delete(branch)
            db.session.commit()
            flash(f"Branch {branch.name} deleted successfully!", "success")

        return redirect(url_for("admin.manage_branch"))

    return render_template("admin/manage_branch.html", form=form, branches=branches)


# ⪼ Manage Subjects_________________________________________________
from forms import SubjectForm

@admin_bp.route("/manage_subject", methods=['GET', 'POST'])
@login_required
@admin_only
def manage_subject():
    form = SubjectForm()
    form.branch_id.choices = [(b.id, b.name) for b in Branch.query.all()]
    subjects = [(s, s.branch.name) for s in Subject.query.all()]  # Fetch subjects with branch names

    if form.validate_on_submit():
        if request.args.get("subject_id"):  # Check if updating
            subject = Subject.query.get(int(request.args.get("subject_id")))
            if subject:
                subject.name = form.name.data
                subject.branch_id = form.branch_id.data
        else:  # If adding a new subject
            new_subject = Subject(name=form.name.data, branch_id=form.branch_id.data)
            db.session.add(new_subject)

        db.session.commit()
        flash("Subject saved successfully!", "success")
        return redirect(url_for("admin.manage_subject"))

    return render_template("admin/manage_subject.html", form=form, subjects=subjects)


# ⪼ Manage Chapters_________________________________________________
from forms import ChapterForm  # Import the form
from sqlalchemy.orm import joinedload

@admin_bp.route("/manage_chapter", methods=['GET', 'POST'])
@login_required
def manage_chapter():
    form = ChapterForm()
    form.subject_id.choices = [(s.id, s.name) for s in Subject.query.all()]  # Populate dropdown with subjects

    # Fetch all chapters with their subjects
    chapters = Chapter.query.options(joinedload(Chapter.subject)).all()

    if form.validate_on_submit():
        chapter_id = request.form.get("chapter_id")  # Get chapter_id from form
        if chapter_id:  # Check if updating
            chapter = Chapter.query.get(chapter_id)
            if chapter:
                chapter.name = form.name.data
                chapter.subject_id = form.subject_id.data
                flash("Chapter updated successfully!", "success")
        else:  # If adding a new chapter
            new_chapter = Chapter(name=form.name.data, subject_id=form.subject_id.data)
            db.session.add(new_chapter)
            flash("Chapter added successfully!", "success")

        db.session.commit()
        return redirect(url_for("admin.manage_chapter"))  # Ensure blueprint name is used

    return render_template("admin/manage_chapter.html", form=form, chapters=chapters)


@admin_bp.route("/delete_chapter/<int:chapter_id>", methods=['POST'])
@login_required
def delete_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    flash("Chapter deleted successfully!", "success")
    return redirect(url_for("admin.manage_chapter"))  # Ensure correct blueprint reference


# ⪼ Manage Users___________________________________________________________
from forms import UserForm

@admin_bp.route("/manage_user", methods=['GET', 'POST'])
@login_required
@admin_only
def manage_user():
    form = UserForm()
    form.branch_id.choices = [(b.id, b.name) for b in Branch.query.all()]  # Populate branch dropdown
    users = User.query.all()

    # If we are editing a user
    user_id = request.args.get('user_id')  # Get the user_id for editing
    if user_id:
        user = User.query.get(user_id)
        if user:
            form.username.data = user.username
            form.name.data = user.name
            form.email.data = user.email
            form.branch_id.data = user.branch_id  # Preselect user's branch
            
            # Password should be left blank on edit, only change if new password is provided
            form.password.data = ''
            form.confirm_password.data = ''
            
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        branch_id = request.form.get('branch_id')  # Get branch ID from form
        user_id = request.form.get('user_id')  # user_id is now part of the form

        if user_id:  # If editing an existing user
            user = User.query.get(user_id)
            if user:
                user.username = username
                user.email = email
                user.name = name
                user.branch_id = branch_id  # Update branch ID
                
                if password:  # If a new password is provided, update it
                    user.set_password(password)
                db.session.commit()
                flash("User details updated successfully!", "success")
        else:  # If adding a new user
            if password:
                new_user = User(username=username, email=email, name=name, branch_id=branch_id)  # Assign branch ID
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                flash("New user added successfully!", "success")
        
        return redirect(url_for("admin.manage_user"))

    # Handle deleting a user
    delete_user_id = request.args.get('delete_user_id')  # This will be used to delete the user
    if delete_user_id:
        user = User.query.get(delete_user_id)
        if user and user.id != 1:  # Ensure admin user (ID=1) is not deleted
            db.session.delete(user)
            db.session.commit()
            flash(f"User {user.username} deleted successfully!", "success")
        else:
            flash("Admin user cannot be deleted!", "error")

        return redirect(url_for("admin.manage_user"))

    return render_template("admin/manage_user.html", form=form, users=users)


# ⪼ Manage Quizzes_________________________________________________
from forms import QuizForm

@admin_bp.route("/manage_quiz", methods=['GET', 'POST'])
@login_required
@admin_only
def manage_quiz():
    form = QuizForm()
    chapters = Chapter.query.all()
    form.chapter_id.choices = [(c.id, c.name) for c in chapters]

    quizzes = db.session.query(
    Quiz.id, Quiz.name, Quiz.nos, Quiz.time,
    Chapter.name.label("chapter_name"),
    Quiz.created_at  # Add this field
).join(Chapter, Quiz.chapter_id == Chapter.id).all()


    if request.method == "POST":
        print(request.form)  # Debugging

        # ADD QUIZ
        if "add" in request.form:
            name = request.form.get("new_name")
            chapter_id = request.form.get("new_chapter_id")
            nos = request.form.get("new_nos")
            time = request.form.get("new_time")

            if not name or not chapter_id or not nos or not time:
                flash("All fields are required!", "danger")
            else:
                chapter = Chapter.query.get(chapter_id)
                if chapter and chapter.subject_id:
                    new_quiz = Quiz(
                        name=name,
                        chapter_id=chapter_id,
                        nos=int(nos),
                        time=int(time),
                        subject_id=chapter.subject_id
                    )
                    db.session.add(new_quiz)
                    db.session.commit()
                    flash("Quiz added successfully!", "success")

        # EDIT QUIZ
        elif "edit" in request.form:
            quiz_id = request.form.get("edit")
            quiz = Quiz.query.get(quiz_id)
            if quiz:
                quiz.name = request.form.get(f"name_{quiz_id}")
                quiz.nos = int(request.form.get(f"nos_{quiz_id}"))
                quiz.time = int(request.form.get(f"time_{quiz_id}"))
                db.session.commit()
                flash("Quiz updated successfully!", "success")

        # DELETE QUIZ
        elif "delete" in request.form:
            quiz_id = request.form.get("delete")
            quiz = Quiz.query.get(quiz_id)
            if quiz:
                db.session.delete(quiz)
                db.session.commit()
                flash("Quiz deleted successfully!", "success")

        return redirect(url_for("admin.manage_quiz"))

    return render_template("admin/manage_quiz.html", form=form, quizzes=quizzes, chapters=chapters)



# ⪼ Manage Questions_________________________________________________
from forms import QuestionForm

@admin_bp.route("/manage_question", methods=['GET', 'POST'])
@login_required
@admin_only
def manage_question():
    form = QuestionForm()

    # Populate dropdown with quizzes
    quizzes = Quiz.query.join(Chapter, Quiz.chapter_id == Chapter.id) \
                        .join(Subject, Chapter.subject_id == Subject.id) \
                        .join(Branch, Subject.branch_id == Branch.id) \
                        .add_columns(Quiz.id.label("quiz_id"), Quiz.name.label("quiz_name"),
                                     Subject.name.label("subject_name"), Branch.name.label("branch_name")) \
                        .all()
    form.quiz_id.choices = [(quiz.quiz_id, f"{quiz.quiz_name} - {quiz.subject_name}") for quiz in quizzes]

    # Fetch all questions with related data
    questions = db.session.query(
        Question.id,
        Question.question_text,
        Question.option1,
        Question.option2,
        Question.option3,
        Question.option4,
        Question.ans.label("correct_option"),
        Question.marks,
        Quiz.name.label("quiz_name")
    ).join(Quiz, Question.quiz_id == Quiz.id).all()

    if request.method == "POST":
        action = request.form.get("action")  # 'add', 'edit', or 'delete'
        if action == "add":
            quiz_id = request.form.get("quiz_id")
            question_text = request.form.get("question_text").strip()
            option1 = request.form.get("option1").strip()
            option2 = request.form.get("option2").strip()
            option3 = request.form.get("option3").strip()
            option4 = request.form.get("option4").strip()
            correct_option = request.form.get("correct_option")
            marks = request.form.get("marks")
            if not all([quiz_id, question_text, option1, option2, option3, option4, correct_option, marks]):
                flash("All fields are required!", "error")
            else:
                new_question = Question(
                    quiz_id=int(quiz_id),
                    question_text=question_text,
                    option1=option1,
                    option2=option2,
                    option3=option3,
                    option4=option4,
                    ans=int(correct_option),
                    marks=int(marks)
                )
                try:
                    db.session.add(new_question)
                    db.session.commit()
                    flash("Question added successfully!", "success")
                except Exception as e:
                    db.session.rollback()
                    flash(f"Failed to add question! Error: {e}", "error")
        elif action == "edit":
            question_id = request.form.get("edit_question_id")
            question = Question.query.get(question_id)
            if question:
                question.quiz_id = int(request.form.get("quiz_id"))
                question.question_text = request.form.get("question_text").strip()
                question.option1 = request.form.get("option1").strip()
                question.option2 = request.form.get("option2").strip()
                question.option3 = request.form.get("option3").strip()
                question.option4 = request.form.get("option4").strip()
                question.ans = int(request.form.get("correct_option"))
                question.marks = int(request.form.get("marks"))
                try:
                    db.session.commit()
                    flash("Question updated successfully!", "success")
                except Exception as e:
                    db.session.rollback()
                    flash(f"Failed to update question! Error: {e}", "error")
        elif action == "delete":
            question_id = request.form.get("question_id")
            question = Question.query.get(question_id)
            if question:
                try:
                    db.session.delete(question)
                    db.session.commit()
                    flash("Question deleted successfully!", "success")
                except Exception as e:
                    db.session.rollback()
                    flash(f"Failed to delete question! Error: {e}", "error")
        return redirect(url_for("admin.manage_question"))
    return render_template("admin/manage_question.html", form=form, questions=questions, quizzes=quizzes)


# ⪼ admin logout_________________________________________________
@admin_bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))
 # g0 back to index
 
#-------------------------------------------------Quiz  routes-----------------------------------------------------

# ⪼ Start Quiz Page
@routes_bp.route("/start_quiz/<int:quiz_id>")
@login_required
def start_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template("user/start_quiz.html", quiz=quiz)



# ⪼ Quiz Attempt Page
@routes_bp.route("/quiz/<int:quiz_id>", methods=["GET", "POST"])
@login_required
def quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz.id).all()

    # Debugging: Check if questions exist
    if not questions:
        print(f"❌ No questions found for Quiz ID: {quiz_id}")

    for question in questions:
        print(f"✅ Question: {question.question_text}, Options: [{question.option1}, {question.option2}, {question.option3}, {question.option4}]")

    if request.method == "POST":
        score = 0

        for question in questions:
            selected_option = request.form.get(f"question_{question.id}")
            if selected_option and int(selected_option) == question.ans:
                score += question.marks

        # Store the score in the database
        new_score = Score(user_id=current_user.id, quiz_id=quiz.id, score=score)
        db.session.add(new_score)
        db.session.commit()

        print(f"✅ Score Recorded: {score}")

        return redirect(url_for("routes.end_quiz", quiz_id=quiz.id, score=score))

    return render_template("user/quiz.html", quiz=quiz, questions=questions)


# ⪼ End Quiz Page
@routes_bp.route("/end_quiz/<int:quiz_id>/<int:score>")
@login_required
def end_quiz(quiz_id, score):
    quiz = Quiz.query.get_or_404(quiz_id)  # Ensure quiz exists
    total_questions = len(quiz.questions)  # This is for lists

    return render_template("user/end_quiz.html", quiz_id=quiz_id, score=score or 0, total_questions=total_questions)




