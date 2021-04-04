from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from tasks.models import Task, Product
from django.contrib.auth.models import User
from django.views import View
from django.db.models import Count
from django.http import JsonResponse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


@method_decorator(login_required, name="dispatch")
class TaskList(View):
    def get(self, request):
        tasks = Task.objects.filter(
            Q(status=Task.READY_TO_REVIEW) | Q(status=Task.READY_TO_UPLOAD))
        for task in tasks:
            products = Product.objects.filter(task_id=task)

            for i in range(len(products)):
                if products[i].status == Product.APPROVED or products[i] == Product.REJECTED:
                    continue
                else:
                    # print("one is not reviewed")
                    break
                # if all the products are reviewed i.e. break statement has not been executed
            else:
                # print("if all the products are reviewed -")
                task.status = Task.READY_TO_UPLOAD
                task.save()

            for i in range(len(products)):
                if products[i].status == Product.UPLOADED or products[i].status == Product.REJECTED:
                    continue
                else:
                    print("breaking" + str(products[i].product_id))
                    break
            else:
                task.status = Task.UPLOADED
                task.save()

        if request.user in tl_check():
            options = [
                ('Ready to review', Task.READY_TO_REVIEW),
                ('Ready to Upload', Task.READY_TO_UPLOAD),
                ('Active/ In-Progress tasks', Task.IN_PROGRESS),
                ('Not Yet Started', Task.NEW),
                # ('Approved', 'APPROVED'),
                # ('Rejected', 'REJECTED'),
                ('Uploaded', Task.UPLOADED),
                ('Cancelled', Task.CANCELLED),
                ('Assigned tasks', 'assigned_tasks'),
                ('Completed Tasks', 'completed_tasks')
            ]
            context = {
                'options': options
            }
        elif request.user in up_check():
            options = [
                # ('Ready to review', Task.READY_TO_REVIEW),
                ('Ready to Upload', Task.READY_TO_UPLOAD),
                # ('Active/ In-Progress tasks', Task.IN_PROGRESS),
                # ('Not Yet Started', Task.NEW),
                # ('Approved', Task.APPROVED),
                # ('Rejected', Task.REJECTED),
                ('Uploaded', Task.UPLOADED),
                ('Cancelled', Task.CANCELLED)
            ]
            context = {
                'options': options
            }

        elif request.user in admin_check():
            options = [
                ('Ready to review', Task.READY_TO_REVIEW),
                ('Ready to Upload', Task.READY_TO_UPLOAD),
                ('Active/ In-Progress tasks', Task.IN_PROGRESS),
                ('Not Yet Started', Task.NEW),
                # ('Approved', Task.APPROVED),
                # ('Rejected', Task.REJECTED),
                ('Uploaded', Task.UPLOADED),
                ('Cancelled', Task.CANCELLED)
            ]
            context = {
                'options': options
            }
        else:
            options = [
                ('Assigned tasks', 'assigned_tasks'),
                ('Completed Tasks', 'completed_tasks')
            ]
            context = {
                'options': options
            }
        context['tls'] = tl_check()
        return render(request, "task-list-tl.html", context)

    def post(self, request):
        selected_status = request.POST.get('selected-task')
        # print("CAME FROM AJAX ", selected_status)

        if selected_status == "assigned_tasks":
            tasks = Task.objects.filter(Q(
                given_to=request.user) & (Q(status="new") | Q(
                    status="in_progress"))).annotate(
                        num_of_products=Count('product'))
            # print(len(tasks))
            # tasks = Task.objects.filter(given_to=request.user).annotate(
            #     num_of_products=Count('product')).annotate(
            #         num_of_approved_products=Count('product', filter=Q(status="approved"))).annotate(
            #             num_of_rejected_products=Count('product', filter=Q(status="rejected")))
        elif selected_status == "completed_tasks":
            tasks = Task.objects.filter(Q(given_to=request.user) & (Q(
                status=Task.READY_TO_REVIEW) | Q(status=Task.READY_TO_UPLOAD) | Q(
                    status=Task.UPLOADED))).annotate(
                num_of_products=Count('product')).annotate(
                        num_of_approved_products=Count('product', filter=Q(product__status="approved") | Q(product__status="uploaded"))).annotate(
                        num_of_rejected_products=Count('product', filter=Q(product__status="rejected")))

        else:
            # print(selected_status)
            tasks = Task.objects.filter(status=selected_status).annotate(
                num_of_products=Count('product')).annotate(
                num_of_approved_products=Count('product', filter=Q(product__status="approved") | Q(product__status="uploaded"))).annotate(
                num_of_rejected_products=Count('product', filter=Q(product__status="rejected")))

        # print(len(tasks))
        context = {
            'tasks': tasks
        }

        return render(request, "task-table.html", context)


@ login_required
def task(request, taskid):
    try:
        if has_task_permission(request.user, taskid):
            # print("permission passed")
            products = Product.objects.filter(task_id=taskid)
            task = Task.objects.get(pk=taskid)
            context = {
                "products": products,
                "task": task,
                "upload__group": up_check()
            }
            return render(request, "task.html", context)

        else:
            return HttpResponse("Not permitted to view this task", 401)
    except ObjectDoesNotExist:
        return HttpResponse("Task not found", 404)


@ login_required
def delete_product(request):
    if request.method == 'POST':
        # print("postttt")
        task_id = request.POST.get("task_id")
        # print("DELETING PROD IN TASKID", task_id)
        product_id = request.POST.get("product_id")
        task = Task.objects.get(pk=task_id)
        if request.user == task.given_by:
            Product.objects.filter(product_id=product_id,
                                   task_id=task_id).delete()
            return HttpResponse(str(product_id))
        else:
            return HttpResponse("Unauthorized access", 401)
    else:
        return HttpResponse("not found", 404)


def tl_check():
    return User.objects.filter(groups__name='Team Leader - CS department')


def up_check():
    return User.objects.filter(groups__name='Upload Department')


def admin_check():
    return User.objects.filter(groups__name="Super Admin")


def tm_check():
    return User.objects.filter(groups__name='Team Member - CS department')


def has_task_permission(user, taskid):

    allowed_users = list(User.objects.exclude(
        groups__name="Team Member - CS department"))
    allowed_users.append(Task.objects.get(pk=taskid).given_to)
    # for u in allowed_users:
    # print(u.first_name)
    return user in allowed_users
