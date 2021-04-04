from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',
         views.ReviewTask.as_view(), name="review-task"),
    path('changeStatus',
         views.changeStatus, name="change-status")
]
