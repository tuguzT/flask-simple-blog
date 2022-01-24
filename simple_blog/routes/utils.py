from urllib.parse import urljoin, urlparse

from flask import request

from ..repository.model import Post, DeletedPosts


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def posts_not_deleted():
    return Post.query.join(DeletedPosts, isouter=True).filter(DeletedPosts.soft_deleted_at == None)


def posts_deleted():
    return Post.query.join(DeletedPosts)
