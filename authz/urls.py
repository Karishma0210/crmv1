from . import views
from django.urls import path
app_name = 'authz'
urlpatterns = [
    path('', views.Login.as_view(), name="login"),
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.logout, name="logout"),
    path('register/', views.Register.as_view(), name="register")
]
