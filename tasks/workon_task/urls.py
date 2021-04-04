from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',
         views.WorkonTask.as_view(), name="workon-task"),
    path('mark-as-complete',
         views.MarkComplete.as_view(), name="mark-as-complete")
]
