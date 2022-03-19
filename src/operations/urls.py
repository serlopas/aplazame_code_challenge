from django.urls import re_path, include

app_name = 'operations'
urlpatterns = [
    re_path('^v1/', include(('operations.api.v1.urls', 'v1'), namespace='v1')),
]
