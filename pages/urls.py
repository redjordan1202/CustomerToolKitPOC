from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.index, name='index'),
    path('result', views.result, name='result'),
    path('download', views.download_packet, name='download'),
]
