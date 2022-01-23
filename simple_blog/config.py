import os
from typing import Final


class Config:
    SECRET_KEY: Final[str] = os.environ.get('SECRET_KEY') or 'JKUBT(*@^i9nfr4hjtv,-4ihbjjgk,-3lw4i4'

    SQLALCHEMY_DATABASE_URI: Final[str] = \
        os.environ.get('DATABASE_URL') or 'postgresql://tuguzT:tugushev_timur@localhost:5432/simple_blog'
    SQLALCHEMY_TRACK_MODIFICATIONS: Final[bool] = False
