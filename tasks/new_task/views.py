from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from tasks.models import Task

# Create your views here.


@method_decorator(login_required, name="dispatch")
class NewTask(View):
    def get(self, request):
        tl_list = list(User.objects.filter(
            groups__name='Team Leader - CS department'))
        tm_list = list(User.objects.filter(
            groups__name='Team Member - CS department'))
        users = tl_list + tm_list
        context = {
            'users': users
        }

        return render(request, "new-task.html", context)

    def post(self, request):
        # save the new task in DB

        given_to = User.objects.get(username=request.POST["given_to"])
        given_by = request.user
        task_date = request.POST["task_date"]
        deadline = request.POST["task_deadline"]

        task = Task.objects.create(
            given_to=given_to,
            given_by=given_by,
            task_date=task_date,
            deadline=deadline
        )
        task.save()

        return redirect(reverse('tasks:add-products', args=[task.id]))
