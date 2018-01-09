from django.urls import path, re_path
from . import views

urlpatterns = [

    # /home/
    path('', views.login, name='login_home'),
    path('races', views.races, name='races'),
    path('help', views.help, name='help'),
    path('about_us', views.about_us, name='about_us'),

    path('details_track/<int:track_id>', views.details_track, name='details_track'),

    path('make_bet/<int:track_id>', views.make_bet, name='make_bet'),

    path('register', views.register, name='register'),

    path('login', views.login, name='login'),

    path('logout', views.logout, name='logout'),
]
