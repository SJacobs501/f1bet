from django.urls import path, re_path
from . import views

urlpatterns = [

    # /home/
    path('', views.races, name='races'),
    path('races', views.races, name='races'),
    path('help', views.help, name='help'),
    path('about_us', views.about_us, name='about_us'),

    path('details_track/<int:race_id>', views.details_track, name='details_track'),

    path('make_bet/<int:race_id>', views.make_bet, name='make_bet'),

    path('register', views.register, name='register'),

    path('login', views.login, name='login'),

    path('logout', views.logout, name='logout'),

    path('manage', views.manage, name='manage'),

    path('add_race', views.add_race, name='add_race'),
    path('add_driver', views.add_driver, name='add_driver'),
    path('add_track', views.add_track, name='add_track'),
    path('remove_race', views.remove_race, name='remove_race'),
    path('remove_driver', views.remove_driver, name='remove_driver'),
    path('remove_track', views.remove_track, name='remove_track'),

    path('account', views.account, name='account'),
    path('add_balance', views.add_balance, name='add_balance'),

    path('end_bet', views.end_bet, name='end_bet'),
]
