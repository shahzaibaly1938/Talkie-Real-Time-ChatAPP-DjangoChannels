from django.urls import path
from .import views


urlpatterns = [
    path('', views.Home, name='home_page'),
    path('about/', views.About, name='about_page'),

]