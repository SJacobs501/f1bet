from django.conf.urls import url
from django.contrib import admin
from . import views


urlpatterns = [

    # /home/
    url(r'^$', views.index, name='index'),

    url(r'^details_track/<int:track_id>/$', views.details_track, name='details_track'),

    url(r'^make_bet/<int:track_id>/$', views.make_bet, name='make_bet'),

    url(r'^register/$', views.register, name='register'),

    url(r'^login/$', views.login, name='login'),

    url(r'^logout/$', views.logout, name='logout'),
]
