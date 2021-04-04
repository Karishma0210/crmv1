from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',
         views.AddProducts.as_view(), name="add-products")
]
