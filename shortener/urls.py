from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # ex: /shortener/
    url(r'^$', views.index, name='index'),
    # ex: /add/
    url(r'^add/$', views.short_link, name='add'),
    # ex: /history/
    url(r'^history/$', views.history, name='history'),
]