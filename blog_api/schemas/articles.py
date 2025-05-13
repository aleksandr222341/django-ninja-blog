from datetime import datetime
from typing import Optional

from ninja import Schema
from blog_app.models import Article
from .comments import CommentSchema
from .auth import UserSchema
from .categories import CategorySchema




class ArticleListSchema(Schema):
    id: int
    title: str
    slug: str
    short_description: str
    preview: Optional[str]
    views: int
    category: CategorySchema
    author: UserSchema
    created_at: datetime

class ArticleLikesSchema(Schema):
    id: int


class ArticleDislikesSchema(Schema):
    id: int


class ArticleImageSchema(Schema):
    id: int
    photo: str
    

class ArticleDetailSchema(Schema):
    id: int
    title: str
    slug: str
    short_description: str
    full_description: Optional[str]
    preview: Optional[str]
    views: int
    category: CategorySchema
    author: UserSchema
    comments: Optional[list[CommentSchema]]
    gallery: Optional[list[ArticleImageSchema]]
    total_likes: int = 0
    total_dislikes: int = 0
    total_comments: int = 0
    created_at: datetime
    updated_at: datetime
    
    @staticmethod
    def resolve_total_likes(obj: Article):
        return obj.likes.user.all().count()
        
    @staticmethod
    def resolve_total_dislikes(obj: Article):
        return obj.dislikes.user.all().count()
        
    @staticmethod
    def resolve_total_comments(obj: Article):
        return obj.comments.all().count()
        

    
class ArticlesPaginatedSchema(Schema):
    total: int
    limit: int = 0
    offset: int = 2
    articles: list[ArticleListSchema]
    

class ArticleCreateSchema(Schema):
    title: str
    short_description: str
    full_description: Optional[str] = None
    category: int
    author: int


class ArticleUpdateSchema(Schema):
    title: Optional[str] = None
    short_description: Optional[str] = None
    full_description: Optional[str] = None
    category: Optional[int] = None