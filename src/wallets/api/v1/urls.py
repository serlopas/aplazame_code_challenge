from django.urls import re_path

from . import views

app_name = 'wallets'
urlpatterns = [
    re_path('^$', views.WalletsView.as_view(), name='wallets'),
    re_path(
        '^(?P<token>[0-9a-f]{32})$',
        views.WalletsDetailView.as_view(),
        name='wallets_detail'
    ),
    re_path(
        '^(?P<token>[0-9a-f]{32})/topup$',
        views.WalletsTopUpView.as_view(),
        name='wallets_top_up'
    ),
    re_path(
        '^(?P<token>[0-9a-f]{32})/charge$',
        views.WalletsChargeView.as_view(),
        name='wallets_charge'
    ),
]
