from simple_blog.login import login_manager
from simple_blog.repository.model.session import Session
from simple_blog.repository.model.user import User


@login_manager.user_loader
def load_user(session_id: str) -> User | None:
    return Session.query.get(session_id).user
