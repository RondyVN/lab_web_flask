web: gunicorn "run:create_app(config_name='dev')"
init: python commands.py create_tables
init2: flask db init