from django.urls import path
from .views import *

urlpatterns = [
    path('download/<str:token>',get_files),
    path('upload/',upload_file),
]