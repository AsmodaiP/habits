from django.contrib import admin
from django.urls import path, include

from .views import list_of_habits

urlpatterns = [
    path('list_of_habits/', list_of_habits, name='list_of_habits'),
]
