from .auth import *
from .basic import *
from .rest import *


# noinspection PyUnusedLocal
@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html', title='404 Not Found'), 404
