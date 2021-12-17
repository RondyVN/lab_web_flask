import click
from flask.cli import with_appcontext
from flask import current_app as app
from app import db


@app.cli.command()
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
    # print("create_all was maked")


cli.add_command(create_tables)

if __name__ == '__main__':
    cli()

# curl $  python create_tables or create_admin
