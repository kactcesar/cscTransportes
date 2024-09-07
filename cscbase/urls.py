from django.urls import path
from .views import * 

app_name = 'cscbase' 

urlpatterns = [
    path('', index, name='index'),
]