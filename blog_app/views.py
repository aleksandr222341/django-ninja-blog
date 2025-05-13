from django.shortcuts import render, HttpResponse, redirect
from . import models
from .forms import LoginForm, RegistrationForm, CommentForm, ArticleForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import UpdateView, DeleteView
from slugify import slugify
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# accounts/login/
# login/

def render_home_page(request):
    categories = [f'category-{i}' for i in range(1, 11)]
    questions = models.FAQ.objects.all()  # select * from blog_app_faq
    slides = models.Slider.objects.all()
    articles = models.Article.objects.all()
    
    paginator = Paginator(articles, 2)  # [(1, [artc1, artc2]), (2, []), ()]
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    
    context = {
        'categories': categories,
        'questions': questions,
        'slides': slides,
        'articles': articles
    }
    return render(request, 'blog_app/index.html', context)
    

def render_articles_page(request):
    query_params = request.GET.get('category')
    page = request.GET.get('page')
    print(query_params)
    
    articles = models.Article.objects.all()
    
    if query_params:
        # category = models.Category.objects.get(slug=query_params)
        # select * from categories where slug = '';
        articles = articles.filter(category__slug=query_params)
    

        
    
    
    paginator = Paginator(articles, 2)  # [(1, [artc1, artc2]), (2, []), ()]
    
    articles = paginator.get_page(page)
    
    categories = models.Category.objects.all()
    context = {
        'articles': articles,
        'categories': categories,
        'slug': query_params
    }
    return render(request, 'blog_app/articles.html', context)
    
def render_about_page(request):
    return render(request, 'blog_app/about.html')
    
    
def render_contacts_page(request):
    return render(request, 'blog_app/contacts.html')
    

def render_faq_page(request):
    questions = models.FAQ.objects.all()
    context = {
        'questions': questions
    }
    return render(request, 'blog_app/faq.html', context)
    

def render_registration_page(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()  # сохранение данных в форму
            messages.success(request, 'Регистрация прошла успешно')
            return redirect('login')
        else:
            for i in form:
                for e in i.errors:
                    print(e)
                # print(dir(i.errors), i.errors.data)
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'blog_app/registration.html', context)
    

# GET, POST, PUT, DELETE
def render_login_page(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()  # AuthenticationForm. User | None
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно вошли в аккаунт')
                return redirect('home')
            else:
                messages.error(request, 'Пользователь не найден')
        else:

            messages.error(request, 'Неправильный логин или пароль')  # отображаем сообщение ошибки
    else:
        form = LoginForm()
    
    context = {
        'form': form
    }
    return render(request, 'blog_app/login.html', context)
    

def render_article_detail_page(request, slug):
    article = models.Article.objects.get(slug=slug)
    comments = models.Comment.objects.filter(article=article)
    
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.article = article
            form.author = request.user
            form.save()
            messages.success(request, 'комментарий успешно добавлен')
            return redirect('article_detail', slug=article.slug)
    else:
        form = CommentForm()
    
    if request.user.is_authenticated:
        is_viewed = models.ArticleCountView.objects.filter(
            article=article,
            user=request.user
        ).exists()  # True, False
        
        if not is_viewed:
            obj = models.ArticleCountView.objects.create(
                article=article,
                user=request.user
            )
            article.views += 1
            article.save()
            
    try:  # models.Like.objects.filter(article=article)
        article.likes  # пытаемся получить лайки статьи
    except Exception as e: 
        models.Like.objects.create(article=article) # создаем запись в таблице лайков и добавляем статью
    
    try:
        article.dislikes
    except Exception as e:
        models.Dislike.objects.create(article=article)
        
    total_likes = article.likes.user.all().count()
    total_dislikes = article.dislikes.user.all().count()
    context = {
        'article': article,
        'comments': comments,
        'form': form,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'total_comments': comments.count()
    }
    return render(request, 'blog_app/article_detail.html', context)
    

def user_logout(request):
    logout(request)
    return redirect('home')


def create_article_page(request):
    if request.method == 'POST':
        form = ArticleForm(data=request.POST, files=request.FILES)
        
        if form.is_valid():
            
            form = form.save(commit=False)
            form.slug = slugify(form.title)
            form.author = request.user
            form.save()
            
            obj = models.Article.objects.get(pk=form.pk)
            
            for item in request.FILES.getlist('gallery'):
                article = models.ArticleImage.objects.create(
                    article=obj,
                    photo=item
                )
                article.save()
            
            messages.success(request, 'Статья успешно создана')
            return redirect('article_detail', form.slug)
        else:
            messages.error(request, 'Что-то пошло не так')
    else:
        form = ArticleForm()
    
    context = {
        'form': form
    }
    return render(request, 'blog_app/article_form.html', context)


class UpdateArticle(UpdateView):
    model = models.Article
    # success_url = '/articles/'  Article.get_absolute_url
    form_class = ArticleForm
    template_name='blog_app/article_form.html'
    

class DeleteArticle(DeleteView):
    model = models.Article
    success_url = '/articles/'
    template_name = 'blog_app/article_confirm_delete.html'
    
""" 

articles/create/

написать функцию для отображения страницы создания статьи
написать ссылку на страницу статьи
рядом с кнопкой "выйти" создать кнопку "создать" которая перенаправляет на страницу создания статьи
"""

# article_id - int
# action - str
# articles/article_id/action
# name=add_vote

def add_vote(request, article_id, action):
    article = models.Article.objects.get(pk=article_id)
    
    # add_like
    # add_dislike
    user = request.user
    if action == 'add_like':
        if user in article.likes.user.all():
            # если лайк уже добавлен от пользователя
            # то удаляем его лайк
            article.likes.user.remove(user.pk)  
        else:
            # если лайк не добавлен
            # добавляем лайк, удаляем дизлайк
            article.likes.user.add(user.pk)
            article.dislikes.user.remove(user.pk)
    elif action == 'add_dislike':
        if user in article.dislikes.user.all():
            # если лайк уже добавлен от пользователя
            # то удаляем его лайк
            article.dislikes.user.remove(user.pk)  
        else:
            # если лайк не добавлен
            # добавляем лайк, удаляем дизлайк
            article.dislikes.user.add(user.pk)
            article.likes.user.remove(user.pk)
    
    return redirect('article_detail', slug=article.slug)
    

def search(request):
    query = request.GET.get('q')
    # регулярные выражения
    articles = models.Article.objects.filter(title__iregex=query)
    context = {
        'articles': articles,
        'total_articles': articles.count(),
        'query': query
    }
    return render(request, 'blog_app/search.html', context)

# на детальной странице статьи сделать подсчет комментариев и отобразить на странице


@login_required(login_url='login')
def profile_page(request):
    articles = models.Article.objects.filter(author=request.user)
    total_comments = sum([article.comment_set.all().count() for article in articles])
    total_views = sum([article.articlecountview_set.all().count() for article in articles])
    total_likes = sum([article.likes.user.all().count() for article in articles])
    total_dislikes = sum([article.dislikes.user.all().count() for article in articles])
    context = {
        'total_articles': articles.count(),
        'total_comments': total_comments,
        'total_views': total_views,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'articles': articles
    }
    return render(request, 'blog_app/profile.html', context)