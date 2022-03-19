from django.urls import re_path

from . import views

app_name = 'users'
urlpatterns = [
    re_path('^users/', views.UsersView.as_view(), name='users'),
]
