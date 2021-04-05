import json
import pickle
from woocommerce import API
from django.shortcuts import render, HttpResponse
from tasks.models import Task, Product
from django.http import Http404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.

filepath = "superman"
fetched_data = ""
with open(filepath, 'rb') as inFile:
    fetched_data = pickle.load(inFile)
    inFile.close()
# print(fetched_data)
fetched_data = fetched_data['upload_secrets']


@method_decorator(login_required, name="dispatch")
class AddProducts(View):
    def get(self, request, taskid):

        try:
            task = Task.objects.get(id=taskid)
            # print(task.status)

            if request.user == task.given_by:
                if task.status != Task.NEW:
                    return HttpResponse("Products already added", 405)
            else:
                return HttpResponse("You cannot add products!!", 401)
        except Task.DoesNotExist:
            return HttpResponse("Task does not exist", 404)
        try:
            rootLevelParents, secondLevelParents = getCategories()
        except KeyError:
            return HttpResponse("API credentials are not working", 200)
        context = {
            "rootLevelParents": rootLevelParents,
            "secondLevelParents": secondLevelParents,

        }

        if 'category' in request.GET:
            catId = request.GET['category']

            simpleProducts, variableProducts, variationProducts = getCatProd(
                catId)
            already_added_products = list(Product.objects.values_list(
                'product_id', flat=True).filter(task_id=taskid))
            # print(already_added_products)
            context = {
                "rootLevelParents": rootLevelParents,
                "secondLevelParents": secondLevelParents,
                "variableProducts": variableProducts,
                "variationProducts": variationProducts,
                "simpleProducts": simpleProducts,
                "already_added_products": already_added_products
            }

        return render(request, "add-products.html", context)

    def post(self, request, taskid):
        product_ids = request.POST.getlist("product_ids")
        # print("received for assigning to the task - {}:\n".format(product_ids))
        # print("iskey baad")
        # for e in request.POST:
        #     print(e)
        already_added_products = list(Product.objects.values_list(
            'product_id', flat=True).filter(task_id=taskid))
        asssigned_prod = len(product_ids)
        for product_id in product_ids:
            # print("product_id - ", product_id)
            task = Task.objects.get(pk=taskid)
            if product_id in already_added_products:
                asssigned_prod -= 1
                continue
            else:
                regular_price = request.POST.get("regular_price_"+product_id)
                # print("regular price", regular_price)
                try:
                    regular_price = float(request.POST.get(
                        "regular_price_"+product_id, 0.0))
                except ValueError:
                    regular_price = None
                    # print("value error!")
                except TypeError:
                    regular_price = None
                    # print("type error!")

                try:
                    sale_price = float(request.POST.get(
                        "sale_price_"+product_id, 0.0))
                except ValueError:
                    sale_price = None
                    # print("value error!")
                except TypeError:
                    sale_price = None
                    # print("type error!")

                product = Product.objects.create(
                    product_id=product_id,
                    name=request.POST.get("name_"+product_id),
                    regular_price=regular_price,
                    sale_price=sale_price,
                    # curr_price=curr_price,
                    task_id=task,
                    last_modified_by=request.user,
                    last_mod_onsite=request.POST.get(
                        "last_mod_onsite_"+product_id),
                    parent_id=request.POST.get("parent_"+product_id),
                    permalink=request.POST.get("permalink_"+product_id)
                )
                product.save()

        return HttpResponse("Successfully assigned " + str(asssigned_prod) + " products")


def getCategories():
    wcapi = API(
        url=fetched_data['url'],
        consumer_key=fetched_data['consumer_key'],
        consumer_secret=fetched_data['consumer_secret'],
        version=fetched_data['version']
    )

    catResp = wcapi.get("products/categories?per_page=100")
    # print("===== catresp headers===")
    # for el in catResp.headers:
    #     print(el)

    totalPages = catResp.headers['X-WP-TotalPages']

    totalCat = int(catResp.headers['X-WP-Total'])
    rootLevelParents = []
    secondLevelParents = []
    catWoRoot = []
    # cat id rom the form submit
    # find rootLevelParents
    for nextPage in range(2, int(totalPages)+2):
        for cat in catResp.json():
            if cat['parent'] == 0:
                # print(cat['name'])
                rootLevelParents.append((cat['id'], cat['name']))
            else:
                catWoRoot.append(
                    (cat['id'], cat['name'], cat['parent']))
        catResp = wcapi.get(
            "products/categories?per_page=100&page={}".format(nextPage))

    # print("total cat", totalCat)
    # print("root cat", len(rootLevelParents))
    # print("cat wo root", len(catWoRoot))

    # find secondLevelParents
    for catRow in catWoRoot:
        for rootRow in rootLevelParents:
            if catRow[2] == rootRow[0]:
                secondLevelParents.append(catRow)

    # print("secondLevelParents", len(secondLevelParents))
    # print("=======TESTTTTTTTTTT================")
    # print(rootLevelParents
    # print("=======TESTTTTTTTTTT================")
    # print(secondLevelParents))
    return (rootLevelParents, secondLevelParents)


def getCatProd(catId):
    wcapi = API(
        url=fetched_data['url'],
        consumer_key=fetched_data['consumer_key'],
        consumer_secret=fetched_data['consumer_secret'],
        version=fetched_data['version']
    )

    prodResp = wcapi.get(
        "products?category={}&per_page=100".format(catId))

    # print("===== prodresp headers===")
    # for el in prodResp.headers:
    #     print(el)

    totalProd = int(prodResp.headers['X-WP-Total'])
    totalPages = int(prodResp.headers['X-WP-TotalPages'])

    # with open("jsonData3706.json", 'w') as outFile:
    #     json.dump(prodResp.json(), outFile)

    variableProducts = {}  # (id, name, link)
    # (id, name, regular_price, sale_price, curr_date date_mod, parent_id)
    variationProducts = {}
    # (id, name, regular_price, sale_price, curr_price, date_mod)
    simpleProducts = {}

    nextPage = 1
    while(nextPage <= totalPages and prodResp.status_code == 200):
        for prod in prodResp.json():
            if prod['type'] == 'variable':
                # print("having variations")
                # display in accordion
                # print(prod['id'], prod['name'])
                variableProducts[prod['id']] = {
                    'name': prod['name'],
                    'permalink': prod['permalink']
                }
                # variableProducts.append(
                #     (prod['id'], prod['name'], prod['permalink']))
                variationResp = wcapi.get(
                    "products/{}/variations?per_page=100".format(prod['id']))
                totalVariations = int(
                    variationResp.headers['X-WP-Total'])
                # print("Variations dir from resp =>", totalVariations)
                for variation in variationResp.json():
                    # print(variation['id'], variation['attributes'])
                    variationProducts[variation['id']] = {
                        'name': prod['name'],
                        'permalink': variation['permalink'],
                        'attributes': variation['attributes'],
                        'regular_price': variation['regular_price'],
                        'sale_price': variation['sale_price'],
                        # 'curr_price': variation['price'],
                        'date_modified': variation['date_modified'],
                        'parent': prod['id']
                    }
                    # print("PERMALINK TEST- ",
                    #       variationProducts[variation['id']]['permalink'])

                # print("attribute check",
                #       variationProducts[variation['id']]['attributes'])
                # variationProducts.append((variation['id'], prod['name'], variation['attributes'],
                #                           variation['regular_price'],
                #                           variation['sale_price'], variation['date_modified'], prod['id']))
            # product without variables or variations
            elif prod['type'] != 'variable' and 'name' in prod.keys():
                # get all products and display without accordion
                # print("not having variations")
                simpleProducts[prod['id']] = {
                    'name': prod['name'],
                    'permalink': prod['permalink'],
                    'regular_price': prod['regular_price'],
                    'sale_price': prod['sale_price'],
                    'price': prod['price'],
                    'date_modified': prod['date_modified'],
                    'parent': 0
                }
                # simpleProducts.append((prod['id'], prod['name'], prod['regular_price'],
                #                        prod['sale_price'], prod['date_modified']))
                # print(prod['id'], prod['name'])

        nextPage += 1
        prodResp = wcapi.get(
            "products?category={}&per_page=100&page={}".format(catId, nextPage))
        # print(prodResp.status_code)
    # print("total products received based on cat =>", totalProd)
    # print("total pages", totalPages)
    # print("variableProducts", len(variableProducts))
    # print("variationProducts", len(variationProducts))
    # print("simpleProducts", len(simpleProducts))

    return (simpleProducts, variableProducts, variationProducts)
