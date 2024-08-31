# example/urls.py
from django.urls import path

from swmis.views import index


urlpatterns = [
    path('<str:type>/<str:method>/', index),
]