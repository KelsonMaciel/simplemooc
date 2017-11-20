from django.conf.urls import include, url
from simplemooc.forum import views

urlpatterns = [
     url(r'^$',views.index, name='index'),
     url(r'^tag/(?P<tag>[\w_-]+)/$',views.index, name='index_tagged'),
     url(r'^respostas/(?P<pk>\d+)/correta/$',views.replay_correct, name='replay_correct'),
     url(r'^respostas/(?P<pk>\d+)/incorreta/$',views.replay_incorrect, name='replay_incorrect'),
     url(r'^(?P<slug>[\w_-]+)/$',views.thread, name='thread'),
     
]