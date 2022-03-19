from django.urls import re_path, include

app_name = 'wallets'
urlpatterns = [
    re_path('^v1/', include(('wallets.api.v1.urls', 'v1'), namespace='v1')),
]
