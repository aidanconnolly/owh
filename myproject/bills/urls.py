from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /bills/
    url(r'^$', views.index, name='index'),
]