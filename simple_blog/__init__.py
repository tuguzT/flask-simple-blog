from flask import Flask

from simple_blog.config import Config

app = Flask(__name__)
app.config.from_object(Config)

from simple_blog import routes  # noqa: E402
