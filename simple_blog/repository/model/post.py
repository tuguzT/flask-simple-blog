from datetime import datetime
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from .user import User
from .. import db


class Post(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    create_datetime = db.Column(db.DateTime, index=True, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(100), index=True, nullable=False)
    text_content = db.Column(db.Text, nullable=False)
    author_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    author: User = db.relationship('User', backref=db.backref('posts', lazy=True))
