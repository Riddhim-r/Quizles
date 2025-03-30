from flask import Flask
from config import Config
from models import db, User, setup_database
from routes import routes_bp, admin_bp
from commands import register_commands
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

#a debug test to see if the app is running 
#print("DEBUG:", app.config["DEBUG"])
#print("DB URI:", app.config["SQLALCHEMY_DATABASE_URI"])
#print("SECRET_KEY:", app.config["SECRET_KEY"])

# ⪼ Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "routes.login"  # Redirect unauthorized users

# ⪼ User loader function (Required for Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ⪼ Import routes and register Blueprint after app is initialized
app.register_blueprint(routes_bp, url_prefix="")  # No prefix ensures root-level routes
app.register_blueprint(admin_bp)

# Initialize Database & Create Admin
setup_database(app)

# ⪼ Register CLI commands
register_commands(app)

if __name__ == "__main__":
    app.run(debug=True)
