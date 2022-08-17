from django.contrib import admin

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('singlegame/', views.SingleGame.user_request, name='singlegame'),
    path('singlegame/gameview', views.SingleGame.single_game_view, name='gameview'),
    path('singlegame/result', views.SingleGame.single_game_result, name='result'),

]
