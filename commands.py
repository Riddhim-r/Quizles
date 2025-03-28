import click
from flask import Flask
from flask.cli import with_appcontext
from models import db, Branch

app = Flask(__name__)

@click.command('seed_branches')
@with_appcontext
def seed_branches():
    """Seed the database with default branches."""
    branches = [
        {"name": "Electronics and Telecommunication", "desc": "ETC Branch"},
        {"name": "Information Technology", "desc": "IT Branch"},
        {"name": "Data Science", "desc": "DS Branch"},
    ]
    
    for branch in branches:
        if not Branch.query.filter_by(name=branch["name"]).first():
            new_branch = Branch(name=branch["name"], desc=branch["desc"])
            db.session.add(new_branch)

    db.session.commit()
    print("⪼ Branches seeded successfully!")

# Make sure this script can be found by Flask
def register_commands(app):
    app.cli.add_command(seed_branches)
