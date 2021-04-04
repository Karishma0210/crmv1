from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',
         views.NewTask.as_view(), name="new-task")
]
