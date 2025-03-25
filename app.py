import os
from flask import Flask
from config import Config
from models import db, User
import datetime  

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# ✅ Import routes and register Blueprint after app is initialized
from routes import routes_bp
app.register_blueprint(routes_bp, url_prefix="")  # No prefix ensures root-level routes

# ✅ Create tables and admin user if not exists
with app.app_context():
    db.create_all()

    if not User.query.filter_by(username='admin').first():
        admin_user = User(
            username='admin',
            email='admin@example.com',
            name='Admin',
            is_admin=True,
            dob=datetime.date(2000, 1, 1)
        )
        admin_user.password = "admin123"
        db.session.add(admin_user)
        db.session.commit()
        print("✅ Admin user created successfully!")

# ✅ Register CLI commands
from commands import register_commands
register_commands(app)

if __name__ == "__main__":
    app.run(debug=True)
