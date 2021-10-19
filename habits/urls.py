from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.urls import path, include

from . import views

urlpatterns = [
    path('list_of_habits/', views.list_of_habits, name='list_of_habits'),
    path('check/', views.checking, name='check'),
]
