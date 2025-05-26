# -*- coding: utf-8 -*-
from flask_migrate import Migrate
from app import create_app
from app.models import db

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    from flask.cli import FlaskGroup
    cli = FlaskGroup(app)
    cli() 