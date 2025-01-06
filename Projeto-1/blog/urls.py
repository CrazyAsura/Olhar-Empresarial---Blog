"""
URL configuration for NewJornal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('news/', views.news, name='news'),
    path('new/<int:post_id>/', views.new_details, name='new_details'),
    path('new/<int:post_id>/add-like/', views.add_like, name='add_like'),
    path('new/<int:post_id>/remove-like/', views.remove_like, name='remove_like'),
    path('new/<int:post_id>/add-dislike/', views.add_dislike, name='add_dislike'),
    path('new/<int:post_id>/remove-dislike/', views.remove_dislike, name='remove_dislike'),
    path('categories/', views.categories, name='categories'),
    path('categories/<int:category_id>/', views.new_by_category, name='new_by_category'),
    path('categories/<int:category_id>/new/<int:post_id>/', views.new_details_by_category, name='new_details_by_category'),
    path('faq/', views.faq, name='faq'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('password-reset/', views.password_reset, name='password_reset'),
    path('terms-of-use/', views.terms_of_use, name='terms_of_use'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
]
