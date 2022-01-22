from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from simple_blog import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)
