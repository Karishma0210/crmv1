"""crmv1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# URLS FOR TASKS
from django.urls import path, include
from . import views
app_name = 'tasks'

urlpatterns = [
    path('', views.TaskList.as_view(), name="task-list"),
    path('<int:taskid>/', views.task, name="task"),
    path('delete-product/', views.delete_product, name="delete-product"),
    path('new-task/', include('tasks.new_task.urls')),
    path('<int:taskid>/add-products/',
         include('tasks.add_products.urls')),
    path('<int:taskid>/workon-task/', include('tasks.workon_task.urls')),
    path('<int:taskid>/review-task/', include('tasks.review_task.urls')),
    path('<int:taskid>/upload-task/', include('tasks.upload_task.urls'))
]
