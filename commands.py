import click
from flask.cli import with_appcontext
from models import db, Branch

@click.command("seed-branches")
@with_appcontext
def seed_branches():
    """Seeds default branches into the database."""
    default_branches = [
        "Electronics and Telecommunication",
        "Information Technology",
        "Data Science"
    ]

    for name in default_branches:
        if not Branch.query.filter_by(name=name).first():
            db.session.add(Branch(name=name, desc=f"{name} Branch"))
    
    db.session.commit()
    print("Default branches seeded successfully.")
