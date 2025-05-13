from typing import Optional
from ninja import Router, File, Form
from ninja.files import UploadedFile
from website.settings import BASE_DIR

from blog_api.schemas.articles import (
    ArticleListSchema, 
    ArticlesPaginatedSchema, 
    ArticleDetailSchema,
    ArticleCreateSchema,
    ArticleUpdateSchema
)
from blog_app.models import Article, Category, ArticleImage
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import os
from blog_api.services.article import article_service

router = Router(tags=['Articles'])

# бизнес логика
# архитектура api
# ddd

@router.get('/articles/', response=ArticlesPaginatedSchema)
def get_articles(request, limit: int = 0, offset: int = 2):
   return article_service.get_paginated_articles(limit, offset)


@router.get('/articles/{slug}/', response=ArticleDetailSchema)
def get_article_detail(request, slug: str):
    return article_service.get_article_detail(slug)


@router.post('/articles/', response=ArticleDetailSchema)
def create_new_article(request, data: Form[ArticleCreateSchema],
    preview: Optional[UploadedFile] = File(None),
    gallery: Optional[list[UploadedFile]] = File(None)
):
    return article_service.create_new_article(data=data, preview=preview, gallery=gallery)


@router.patch('/articles/{id}/update/', response=ArticleDetailSchema)
def update_article(request, id: int, data: ArticleUpdateSchema,
    preview: Optional[UploadedFile] = File(None),
    gallery: Optional[list[UploadedFile]] = File(None)
):
    return article_service.update_article(id, data, preview, gallery)
    

@router.delete('/articles/{id}/delete/')
def delete_article(request, id: int):
    return article_service.delete_article(id)