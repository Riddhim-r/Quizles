import os
from flask import Flask
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# 🔥 Import routes AFTER initializing the app
import routes  

with app.app_context():  # ✅ Ensure app context is set up
    db.create_all()  


if __name__ == "__main__":
    app.run(debug=True)

# ✅ Register CLI commands properly
from commands import register_commands
register_commands(app)
