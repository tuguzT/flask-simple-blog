from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from simple_blog.repository import db


class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f'<User id={self.id} name="{self.name}">'
