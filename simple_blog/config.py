import os
from typing import Final


class Config:
    SECRET_KEY: Final[str] = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI: Final[str] = os.environ.get('DATABASE_URL').replace('postgres', 'postgresql')
    SQLALCHEMY_TRACK_MODIFICATIONS: Final[bool] = False
