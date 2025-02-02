from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config  # Import config settings
from models import db  # Import only db, not the entire models file

app = Flask(__name__)
app.config.from_object(Config)  # Load configuration from config class

db.init_app(app)  # Initialize the database with the app

@app.route('/')
def index():
    return "Flask App is Running!"  # Simple test response

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure tables are created before running
    app.run(debug=True)  # Runs on http://127.0.0.1:5000/
