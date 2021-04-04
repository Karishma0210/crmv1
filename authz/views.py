from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import auth, User, Group
from django.urls import reverse
# Create your views here.


class Login(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        try:
            username = User.objects.get(email=email.lower()).username
            # print(username, "tryinn to login")
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                if request.GET.get('next', "") != "":
                    return redirect(request.GET['next'])
                return redirect(reverse('tasks:task-list'))
            else:
                # print("FALSE USERNAME OR PASS")
                messages.info(request, "invalid credentials")
                return redirect(reverse('authz:login'))
        except Exception:
            messages.info(request, "email is not registered")
            return redirect(reverse('authz:login'))


class Register(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        full_name = request.POST['full_name']
        email = request.POST['email']
        password0 = request.POST['password0']
        password1 = request.POSpassword0 = request.POST['password1']
        firstname = full_name.split()[0]
        lastname = full_name.split()[-1]
        username = email.split("@")[0]

        if password0 == password1:
            if email.split("@")[1] == "efutureye.com":
                # also, it has to be a legimate efutureye.com's email
                if User.objects.filter(email=email).exists():
                    messages.info(request,
                                  'You are already registered, Please <a href="/crm/login/">Log In</a>',
                                  extra_tags='safe')
                    return redirect(reverse('authz:register'))
                else:  # if user is new

                    user = User.objects.create_user(
                        username=username,
                        password=password0,
                        email=email,
                        first_name=firstname,
                        last_name=lastname
                    )
                    teamMember = Group.objects.get(
                        name='Team Member - CS department')
                    teamMember.user_set.add(user)
                    user.save()
                    auth.login(request, user)
                    messages.info(request, "Welcome " + firstname + "!")
                    return redirect(reverse('tasks:task-list'))
            else:
                messages.info(request, "Sorry, you can not register!")
                return redirect(reverse('authz:register'))


def logout(request):
    auth.logout(request)
    return redirect('../login/')
