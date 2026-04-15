from django.urls import path
from . import views
from .views import CustomLoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<int:id>/', views.article_detail, name='article_detail'),
    path('register/', views.register, name='register'),
    path('add/', views.add_article, name='add_article'),
    path('profile/', views.profile, name='profile'),
    path('login/', CustomLoginView.as_view(), name='login'),
]