from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from tasks.models import Task, Product
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


@method_decorator(login_required, name="dispatch")
class ReviewTask(View):

    def get(self, request, taskid):
        try:
            task = Task.objects.get(pk=taskid)
            # only person who has given the task can review it
            if request.user == task.given_by:
                if task.status == Task.NEW or task.status == Task.IN_PROGRESS:
                    return HttpResponse("Task is not ready to be reviewed!!", 404)
                else:
                    # if task.status == Task.READY_TO_REVIEW:
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

                    context = {
                        "task": task,
                        "products": products
                    }
                    return render(request, "task-review.html", context)
                # return HttpResponse("Task has already been reviewed!!", 404)
            return HttpResponse("You cannot review task given by other person!!", 401)

        except ObjectDoesNotExist:
            return HttpResponse("Product not found", 404)

    def post(self, request, taskid):
        try:
            task_id = request.POST.get("task_id")
            task = Task.objects.get(pk=task_id)
            product_id = request.POST.get("product_id")
            product = Product.objects.get(
                product_id=product_id, task_id_id=task.id)
            # only person who has given the task can review it
            if request.user == task.given_by:
                if task.status == Task.READY_TO_REVIEW:
                    submitter_btn = request.POST.get("submitter_btn")
                    if submitter_btn == "approve_btn":
                        product.status = Product.APPROVED
                        product.save()

                    elif submitter_btn == "reject_btn":
                        product.status = Product.REJECTED
                        product.save()

                    return HttpResponse("successfully marked as - {}".format(product.status), 200)
                return HttpResponse("you cannot review already reviewed task", 405)
            else:
                return HttpResponse("You cannot review task given by other person!!", 401)
        except ObjectDoesNotExist as e:
            return HttpResponse(e, 404)

        return HttpResponse("post req", 200)


def changeStatus(request, taskid):
    if request.method == "POST":
        task_id = request.POST.get("task_id")
        try:
            task = Task.objects.get(pk=task_id)
            if request.user == task.given_by:
                submitter_btn = request.POST.get("submitter_btn")
                if submitter_btn == "task_ready_to_upload_btn":
                    task.status = Task.READY_TO_UPLOAD
                    task.save()
                elif submitter_btn == "task_cancelled_btn":
                    task.status = Task.CANCELLED
                    task.save()
                return HttpResponse("task marked as - {}".format(task.status), 200)
            else:
                return HttpResponse("You cannot review task given by other person!!", 401)
        except ObjectDoesNotExist:
            return HttpResponse("Task does not exists", 404)
