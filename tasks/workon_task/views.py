from django.shortcuts import render, HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from tasks.models import Task, Product
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


@method_decorator(login_required, name="dispatch")
class WorkonTask(View):

    def get(self, request, taskid):
        # if work is new/ in_progress
        task = Task.objects.get(pk=taskid)
        if request.user == task.given_to:
            if task.status == Task.NEW or task.status == Task.IN_PROGRESS:
                products = Product.objects.filter(task_id=taskid)
                context = {
                    "products": products
                }
                return render(request, "workontask.html", context)
            else:
                return HttpResponse("You cannot work on an already completed task!!", 405)
        else:
            return HttpResponse("You cannot work on other person's task!!", 401)

    def post(self, request, taskid):
        product_ids = [v for k, v in request.POST.items()
                       if k.startswith('id_')]
        # print(product_ids)
        task = Task.objects.get(pk=taskid)
        task.status = Task.IN_PROGRESS
        task.save()

        # for p in request.POST:
        #     print("-->" + p)
        #     print("->" + request.POST[p] + "-" + str(type(request.POST[p])))
        for product_id in product_ids:
            try:
                product = Product.objects.get(
                    task_id=taskid, product_id=product_id)

                new_reg_price = request.POST.get('new_reg_price_' + product_id)
                try:
                    product.new_reg_price = float(new_reg_price)
                except ValueError:
                    product.new_reg_price = None
                    print("value error!")
                except TypeError:
                    product.new_reg_price = None
                    print("type error!")

                suggested_price = request.POST.get(
                    'suggested_price_' + product_id)
                try:
                    product.suggested_price = float(suggested_price)
                except ValueError:
                    product.suggested_price = None
                    print("value error!")
                except TypeError:
                    product.suggested_price = None
                    print("type error!")

                sharaf_dg_price = request.POST.get(
                    'sharaf_price_' + product_id)
                try:
                    product.sharaf_dg_price = float(sharaf_dg_price)
                except ValueError:
                    product.sharaf_dg_price = None
                    print("value error!")
                except TypeError:
                    product.sharaf_dg_price = None
                    print("type error!")
                product.sharaf_dg_product_link = request.POST.get(
                    'sharaf_link_' + product_id)

                carrefour_price = request.POST.get(
                    'carrefour_price_' + product_id)
                try:
                    product.carrefour_price = float(carrefour_price)
                except ValueError:
                    product.carrefour_price = None
                    print("value error!")
                except TypeError:
                    product.carrefour_price = None
                    print("type error!")
                product.carrefour_product_link = request.POST.get(
                    'carrefour_link_' + product_id)

                lulu_price = request.POST.get('lulu_price_' + product_id)
                try:
                    product.lulu_price = float(lulu_price)
                except ValueError:
                    product.lulu_price = None
                    print("value error!")
                except TypeError:
                    product.lulu_price = None
                    print("type error!")
                product.lulu_product_link = request.POST.get(
                    'lulu_link_' + product_id)

                jumbo_price = request.POST.get('jumbo_price_' + product_id)
                try:
                    product.jumbo_price = float(jumbo_price)
                except ValueError:
                    product.jumbo_price = None
                    # print("value error!")
                except TypeError:
                    product.jumbo_price = None
                    # print("type error!")
                product.jumbo_product_link = request.POST.get(
                    'jumbo_link_' + product_id)

                axiom_price = request.POST.get('axiom_price' + product_id)
                try:
                    product.axiom_price = float(axiom_price)
                except ValueError as e:
                    product.axiom_price = None
                    # print("value error!")
                except TypeError as e:
                    product.axiom_price = None
                    # print("type error!")
                product.axiom_product_link = request.POST.get(
                    'axiom_link_' + product_id)

                product.save()
            except ObjectDoesNotExist:
                return HttpResponse("Product not found", 404)
        # print(request.POST.get(''))
        return HttpResponse(str(len(product_ids)))


@method_decorator(login_required, name="dispatch")
class MarkComplete(View):
    def get(self, request, taskid):
        return HttpResponse("page not found", 404)

    def post(self, request, taskid):
        try:
            task = Task.objects.get(pk=taskid)
            task.status = Task.READY_TO_REVIEW
            task.save()
            return HttpResponse("task id {} marked as completed".format(taskid))

        except ObjectDoesNotExist:
            return HttpResponse("Task not found", 404)
