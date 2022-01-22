import os
from typing import Final


class Config:
    SQLALCHEMY_DATABASE_URI: Final[str] = os.environ.get('DATABASE_URL') or \
                                          'postgresql://tuguzT:tugushev_timur@localhost:5432/simple_blog'
    SQLALCHEMY_TRACK_MODIFICATIONS: Final[bool] = False
