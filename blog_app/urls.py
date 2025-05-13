from django.urls import path

from . import views


urlpatterns = [
    path('', views.render_home_page, name='home'),
    path('about/', views.render_about_page, name='about'),
    path('contacts/', views.render_contacts_page, name='contacts'),
    path('faq/', views.render_faq_page, name='faq'),
    path('articles/', views.render_articles_page, name='articles'),
    path('registration/', views.render_registration_page, name='registration'),
    path('login/', views.render_login_page, name='login'),
    path('articles/create/', views.create_article_page, name='create_article'),
    path('articles/<slug:slug>/', views.render_article_detail_page,
    name='article_detail'),
    path('articles/<int:article_id>/<str:action>/', views.add_vote, name='add_vote'),
    path('articles/<slug:slug>/update/', views.UpdateArticle.as_view(), name='update'),
    path('articles/<slug:slug>/delete/', views.DeleteArticle.as_view(), name='delete'),
    path('logout/', views.user_logout, name='logout'),
    
    path('search/', views.search, name='search'),
    path('profile/', views.profile_page, name='profile')
    
]