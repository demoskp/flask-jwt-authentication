import click
from flask.cli import with_appcontext, AppGroup

from extensions import db
from models import User

user_cli = AppGroup("user", help="Run commands for users")


@user_cli.command("create", )
@click.argument("name")
@click.argument("email")
@click.option("--extras", default=None)
@with_appcontext
def create_user(name: str, email: str, extras):
    """Create a user by passing the name and email"""
    click.echo(f"extras passed are: {extras}")
    click.echo("Creating user")
    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    click.echo(f"User {name} created")
