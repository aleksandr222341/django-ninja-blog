from blog_api.schemas.articles import (
    ArticlesPaginatedSchema,
    ArticleCreateSchema,
    ArticleUpdateSchema
)
from blog_app.models import Article, Category, ArticleImage
from django.shortcuts import get_object_or_404
from ninja import UploadedFile

from django.contrib.auth.models import User
from website.settings import BASE_DIR
from typing import Optional
import os

# овер инжиринг

class ArticleService:
    def __save_photo(self, file: UploadedFile, folder_path: str):
        file = file.read()
        with open(folder_path, 'wb') as _file:
            _file.write(file)
    
    def create_new_article(
        self,
        data: ArticleCreateSchema, 
        preview: Optional[UploadedFile],
        gallery: Optional[list[UploadedFile]]
    ):
        data = dict(**data.dict())
        category = get_object_or_404(Category, pk=data.pop('category'))
        author = get_object_or_404(User, pk=data.pop('author'))
        
        article = Article.objects.create(**data, category=category, author=author)
        if preview is not None:
            preview_path = f'{BASE_DIR}/media/articles/previews/{preview.name}'
            self.__save_photo(preview, preview_path)
            
            article.preview = f'articles/previews/{preview.name}'
            article.save()
            
        for item in gallery:
            item_path = f'{BASE_DIR}/media/articles/gallery/{item.name}'
            self.__save_photo(item, item_path)
            
            item_obj = ArticleImage.objects.create(
                article=article, 
                photo=f'articles/gallery{item.name}'
            )

        return article
        
    
    def get_paginated_articles(
        self, 
        limit: int = 2, 
        offset: int = 0
    ) -> ArticlesPaginatedSchema:
        articles = Article.objects.all()
        total = articles.count()
        
        # ?limit=0&offset=2
        # ?limit=2&offset=4
        articles = articles[limit:offset]
        
        return ArticlesPaginatedSchema(
            total=total,
            limit=limit, 
            offset=offset, 
            articles=articles
        )
    
    def get_article_detail(self, slug: str) -> Article:
        article = get_object_or_404(Article, slug=slug)
        return article
    
    def update_article(self, id: int, data: ArticleUpdateSchema, 
        preview: Optional[UploadedFile],
        gallery: Optional[list[UploadedFile]]
    ):
        article = get_object_or_404(Article, pk=id)
        for key, value in data.dict().items():
            if not value:
                current_value = getattr(article, key)
                setattr(article, key, current_value)
            else:
                if key == 'category':
                    category = get_object_or_404(Category, pk=value)
                    setattr(article, key, category)
                else:
                    setattr(article, key, value)
        article.save()
        
        if preview is not None:
            preview_content = preview.read()  # получаем байты фотографии для скачивания
            if article.preview:  # article.preview.url - путь до файла
                # media/articles/previews/file.png
                os.remove(f'{BASE_DIR}/{article.preview.url}')
            
            preview_path = f'{BASE_DIR}/media/articles/previews/{preview.name}'
            with open(preview_path, 'wb') as _file:
                _file.write(preview_content)
            
            article.preview = f'articles/previews/{preview.name}'
            article.save()
        
        if gallery is not None:
            for item in article.gallery.all():
                try:
                    os.remove(f'{BASE_DIR}/{item.photo.url}')
                except Exception as e:
                    print(e)
                    
                item.delete()  # удаляем фотографию
            for item in gallery:
                item_content = item.read()
                item_path = f'{BASE_DIR}/media/articles/gallery/{item.name}'
                with open(item_path, 'wb') as item_file:
                    item_file.write(item_content)
                
                item_obj = ArticleImage.objects.create(
                    article=article, 
                    photo=f'articles/gallery/{item.name}'
                )
        return article
        
    def delete_article(self, id: int):
        article = get_object_or_404(Article, id=id)
        article.delete()
        return {'is_deleted': True}
        
        


article_service = ArticleService()
