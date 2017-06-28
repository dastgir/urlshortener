from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /shortener/
    url(r'^$', views.index, name='index'),
    # ex: /add/
    url(r'^add/$', views.short_link, name='detail'),
    url(r'^add/$', views.short_link, name='detail'),
]