from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify



# Create your models here.

# таблица FAQ
# title, description, image, id - есть у всех заранее

# ORM - Object Relation Model

# objects - QueryManager

# название класса - добавляется в базу данных как название таблицы

# поле таблицы = тип данных поля

class Slider(models.Model):  # models.Model - специальный класс, с помощью которого, создаются таблицы
    # max_length = сколько максимально символов можно будет добавить
    # verbose_name = альтернативное название для поля в админ панели
    title = models.CharField(max_length=40, verbose_name='Заголовок')  # varchar
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(upload_to='slider/', verbose_name='Фото')
    # media/slider/1.jpg
    
    # categorys
    
    def __str__(self):
        return self.title
    
    class Meta:
        # Сортировка
        verbose_name = 'Слайд'  # меняет название таблицы в ед.ч
        verbose_name_plural = 'Слайды'  # меняет название таблицы в мн.ч
        
# python manage.py makemigrations - данная команда, проверяет правильность нашей таблицы, и создает файл с историей того, что мы сделали с нашей базой данных
# python manage.py migrate - выполняет файл с историей изменений нашей базы данных, и создает таблицы внутри файла базы данных


# создание суперпользователя(администратора) для проекта

# python manage.py createsuperuser

# создать таблицу FAQ
# добавить ее в админку


class FAQ(models.Model):
    question = models.TextField(verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')
    
    def __str__(self) -> str:
        return self.question
    
    class Meta:
        verbose_name = 'Вопрос ответ'
        verbose_name_plural = 'Вопросы ответы'


# спорт
class Category(models.Model):
    name = models.CharField(max_length=40, unique=True, verbose_name='Название')
    slug = models.SlugField(verbose_name='Слаг', 
        help_text='Данное поле заполняется автоматически'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(verbose_name='Слаг', null=True, blank=True)
    short_description = models.TextField(verbose_name='Краткое описание')
    full_description = models.TextField(verbose_name='Полное описание',
        null=True, blank=True)
    preview = models.ImageField(upload_to='articles/previews/', 
        null=True, blank=True, verbose_name='Превью')
    views = models.PositiveIntegerField(default=0, verbose_name='Кол-во просмотров')  # 27737
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, 
       related_name='articles', verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='articles', verbose_name='Автор')
    
    def save(self, *args, **kwargs):
        
        
        if not self.slug:
            self.slug = slugify(self.title)
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        

class ArticleImage(models.Model)    :
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья',
    related_name='gallery')
    photo = models.ImageField(upload_to='articles/gallery/', verbose_name='Фото')
    
    class Meta:
        verbose_name = 'Галлерея статьи'
        verbose_name_plural = 'Галлерея статьи'
        

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья', related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.author} - {self.article}'
        
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
    
    
class ArticleCountView(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
    verbose_name='Пользователь')
    

class Like(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE,
    related_name='likes', verbose_name='Статья')
    user = models.ManyToManyField(User, related_name='likes')
    

class Dislike(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE,
    related_name='dislikes', verbose_name='Статья')
    user = models.ManyToManyField(User, related_name='dislikes')


"""
таблица комментариев

комент

ссылка на статью
ссылка на пользователя
текст
дата создания комментария

строковое представление

класс мета

"""


# категория спорт: статья 1, статья 2
#  отдай все статьи где категория это спорт  Article.objects.filter(), category.articles.all
    