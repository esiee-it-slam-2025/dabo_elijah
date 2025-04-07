from django.urls import path, include
from .views import stadiums

urlpatterns = [
    path('api/stadiums/', stadiums, name='stadiums'),
]
