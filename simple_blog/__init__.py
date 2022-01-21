from flask import Flask

app = Flask(__name__)

from simple_blog import routes  # noqa: E402
