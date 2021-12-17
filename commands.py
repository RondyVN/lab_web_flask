import click
from flask.cli import with_appcontext
from app import db

from flask import Blueprint

command_blueprint = Blueprint('cli', __name__, )


@command_blueprint.cli.command()
def initdb():
    """Initialize the database."""
    click.echo('Init the db')


@click.group()
def cli():
    pass


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()
    click.echo("tables created!!!")
    print("create_all was maked")


@click.command(name='drop_tables')
@with_appcontext
def drop_tables():
    db.drop_all()
    click.echo("tables drop!!!")
    print("drop_all was maked")


cli.add_command(create_tables)
cli.add_command(drop_tables)

if __name__ == '__main__':
    cli()

# curl $  python create_tables or create_admin
