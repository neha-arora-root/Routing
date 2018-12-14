# vrp/urls.py

from django.conf.urls import url
from vrp import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
]