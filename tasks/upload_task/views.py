from django.shortcuts import render, HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from tasks.models import Task, Product
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from woocommerce import API
from django.db.models import Q
import json
import pickle
import copy
# Create your views here.

filename = "super_secrets"
fetched_data = ""
with open(filename, 'rb') as inFile:
    fetched_data = pickle.load(inFile)
    inFile.close()
# print(fetched_data)
fetched_data = fetched_data['upload_secrets']


@method_decorator(login_required, name="dispatch")
class UploadTask(View):

    def get(self, request, taskid):
        # only show this page to uppload department
        if request.user in up_check():
            try:
                task = Task.objects.get(pk=taskid)
                products = Product.objects.filter(task_id=task)
                for i in range(len(products)):
                    if products[i].status == Product.UPLOADED or products[i].status == Product.REJECTED:
                        continue
                    else:
                        # print("breaking" + str(products[i].product_id))
                        break
                else:
                    task.status = Task.UPLOADED
                    task.save()

                if task.status == Task.READY_TO_UPLOAD or task.status == Task.UPLOADED:
                    products = Product.objects.filter(
                        Q(task_id=task) & (Q(status=Product.APPROVED) | Q(
                            status=Product.UPLOADED)))
                    context = {
                        "task": task,
                        "products": products
                    }
                    return render(request, "upload-task.html", context)
                return HttpResponse("Task is not ready to be uploaded!!", 404)
            except ObjectDoesNotExist:
                return HttpResponse("Task not found", 404)

        return HttpResponse("You are not authorized to upload the task page", 401)

    def post(self, request, taskid):
        if request.user in up_check():
            try:
                product_ids = request.POST.getlist("product_ids")
                print("received for assignments:\n", product_ids)
                # print("iskey baad")
                # for e in request.POST:
                #     print(e)
                already_uploaded_products = list(Product.objects.values_list(
                    'product_id', flat=True).filter(task_id=taskid, status=Product.UPLOADED))

                # uploaded_prod = len(product_ids)
                update_bucket = []
                for product_id in product_ids:
                    # print("product_id - ", product_id)

                    if product_id not in already_uploaded_products:
                        curr_product = Product.objects.get(
                            product_id=product_id, task_id=taskid)

                        update_bucket.append(
                            {
                                "id": product_id,
                                "regular_price": curr_product.new_reg_price,
                                "sale_price": curr_product.suggested_price,
                                "parent_id": curr_product.parent_id
                            }
                        )

                is_success = updatePrices(update_bucket)
                if is_success:
                    for p in update_bucket:
                        curr_product = Product.objects.get(
                            product_id=p['id'], task_id=taskid)
                        curr_product.status = Product.UPLOADED
                        curr_product.save()

                    return HttpResponse("Successfully uploaded " + str(len(update_bucket)) + " products")
                else:
                    return HttpResponse("product not uploaded", 500)

            except ObjectDoesNotExist:
                return HttpResponse("Task does not exist", 404)

        return HttpResponse("page getting ready for post")


def up_check():
    return User.objects.filter(groups__name='Upload Department')


def updatePrices(update_bucket):
    # print("inside upload prices")
    # print("length of the update bucket is - {}".format(len(update_bucket)))
    # print("RCVED FOR UPDATE", update_bucket)
    dummy_update_bucket = copy.deepcopy(update_bucket)
    # print("DUMMY FOR UPDATE AND INTERNAL USE", dummy_update_bucket)
    variations_update_bucket = []
    simples_update_bucket = []
    for bucket_product in dummy_update_bucket:
        if bucket_product['parent_id'] == 0:
            bucket_product.pop("parent_id")
            simples_update_bucket.append(bucket_product)
        else:
            variations_update_bucket.append(bucket_product)
    # print("AFTER POPPING UP PARENT ID FROM SIMPLES - DUMMY", dummy_update_bucket)
    # print("AFTER POOPING UP PARENT ID FROM SIMPLES - ORIGINAL", update_bucket)
    wcapi = API(
        url=fetched_data['url'],
        consumer_key=fetched_data['consumer_key'],
        consumer_secret=fetched_data['consumer_secret'],
        version=fetched_data['version']
    )
    updateResp = []
    if len(simples_update_bucket) > 0:
        last_no_in_batch = 0
        for batch_no in range(len(simples_update_bucket)//100 + 1):
            data = {
                "update": simples_update_bucket[last_no_in_batch:100*(batch_no+1)]
            }
            # print("data for batch", data)
            updateResp.append(wcapi.post("products/batch", data).json())
            last_no_in_batch += 1

    if len(variations_update_bucket) > 0:
        for bucket_product in variations_update_bucket:
            variation_id = bucket_product.pop("id")
            parent_id = bucket_product.pop("parent_id")
            data = {}
            for el_key, el_val in bucket_product.items():
                data[el_key] = str(el_val)

            # print("updating data for variations ", data)
            updateResp.append(wcapi.post("products/{}/variations/{}".format(
                parent_id, variation_id), data).json())

    with open("jsonDataUpdate.json", 'w') as outFile:
        json.dump(json.dumps(updateResp), outFile)

    # print("BEFORE SENDING ORIGINAL UPDATE -", update_bucket)
    # print("BEFORE SENDING DUMMY - ", dummy_update_bucket)
    # print("BEFORE SENDING VARIATIONS - ", variations_update_bucket)
    # print("BEFORE SENDING SIMPLES - ", simples_update_bucket)
    if len(updateResp) > 0:
        return True
    return False
