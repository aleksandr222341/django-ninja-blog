from ninja import Router
from typing import Optional

from blog_api.schemas.comments import CommentShortSchema, CommentPaginatedSchema, CommentUpdateCreateSchema
from blog_api.services.comment import comments_servise
from django.shortcuts import get_object_or_404

router = Router(tags=['Comments'])

# добавить роуты для получения 
# Детальной информации о комментарии
# удаление комментария
# создание комментария


@router.get('/comments/', response=CommentPaginatedSchema)
def get_comments(request, limit: int = 5, offset: int = 0):
    return comments_servise.get_comments(limit=limit, offset=offset)


@router.get('/comments/{id}/', response=CommentShortSchema)
def get_comment_detail(request, id: int):
    return comments_servise.get_comment_detail(id=id)


@router.post('/comments/', response=CommentShortSchema)
def create_comment(request, comment_data: CommentUpdateCreateSchema):
    return comments_servise.create_comment(comment_data=comment_data)


@router.put('/comments/{id}/update/', response=CommentShortSchema)
def update_comment(request, id: int, comment_data: CommentUpdateCreateSchema):
    return comments_servise.update_comment(id=id, comment_data=comment_data)


@router.delete('/comments/{id}/delete/')
def delete_comment(request, id: int):
    return comments_servise.delete_comment(id=id)