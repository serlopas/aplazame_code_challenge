from django.urls import re_path, include

app_name = 'users'
urlpatterns = [
    re_path('^v1/', include(('users.api.v1.urls', 'v1'), namespace='v1')),
]
