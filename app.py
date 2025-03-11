import os
from flask import Flask
from datetime import datetime
from config import Config
from models import db, User

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def ensure_admin_user():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin_email = os.getenv("ADMIN_EMAIL", "admin@quizles.app")
        admin_dob_str = os.getenv("ADMIN_DOB", "2000-01-01")
        admin_dob = datetime.strptime(admin_dob_str, '%Y-%m-%d')

        admin = User(
            username='admin',
            name='Admin',
            email=admin_email,
            dob=admin_dob,
            is_admin=True
        )
        admin.password = 'admin123'
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created.")

# 🔥 Now import routes after app is fully defined (no circular crash)
from routes import *

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        ensure_admin_user()
    app.run(debug=True)

from commands import seed_branches
app.cli.add_command(seed_branches)
