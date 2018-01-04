from django.urls import path, re_path
from . import views

urlpatterns = [

    # /home/
    path('', views.index, name='index'),

    # /f1better/index.html
    path('index.html', views.index, name='index'),
    path('details_track/<int:track_id>/', views.details_track, name='details_track'),

    path('make_bet/<int:track_id>/', views.make_bet, name='make_bet'),

    path('register', views.register, name='register'),
    path('register.html', views.register, name='register'),

    path('login', views.login, name='login'),
    path('login.html', views.login, name='login'),

    path('logout', views.logout, name='logout'),
]