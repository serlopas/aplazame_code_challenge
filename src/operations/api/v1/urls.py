from django.urls import re_path

from . import views

app_name = 'operations'
urlpatterns = [
    re_path('^$', views.OperationsView.as_view(), name='operations'),
]
