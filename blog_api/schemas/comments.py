# сделать получение всех комментариев

from datetime import datetime
from ninja import Schema

from .auth import UserSchema


class CommentSchema(Schema):
    id: int
    text: str
    # article: int
    author: UserSchema
    created_at: datetime

class CommentShortSchema(Schema):
    id: int
    text: str
    article_id: int
    author_id: int
    created_at: datetime

class CommentPaginatedSchema(Schema):
    total: int
    limit: int
    offset: int
    comments: list[CommentShortSchema]

class CommentUpdateCreateSchema(Schema):
    text: str
    article_id: int
    author_id: int
    