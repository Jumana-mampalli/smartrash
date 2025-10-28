from django.urls import path
from . import api_views

app_name = 'api'

urlpatterns = [
    path('bin-status/', api_views.bin_status_update, name='bin_status'),
    path('bin-status/<str:bin_id>/', api_views.bin_status_detail, name='bin_status_detail'),
]
