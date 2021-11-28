from django.shortcuts import render
from django.shortcuts import redirect,render
from .models import Products,ProductDetails
from django.http import JsonResponse
import json
from django.core.serializers import serialize

# Create your views here.

def view_product(request):
    context = {}
    # print('helo')
    pr_obj = Products.objects.all()
    context['products'] = pr_obj
    return render(request,'products.html',context)

def product_details(request,id):
    context = {}
    pr_obj = Products.objects.get(id=id)
    obj = ProductDetails.objects.get(pr_id=id)
    # print(obj.description)
    context['details'] = obj
    context['pr_details'] = pr_obj

    return render(request,'product_details.html',context)

def home(request):
    context = {}
    pr_obj = Products.objects.all()
    context['products'] = pr_obj
    for item in pr_obj:
        print(item.pr_image)
    return render(request,'home.html', context)

def product_view_bybrand(request):
    brand = request.GET['brand']
    pr_obj = Products.objects.filter(pr_brand=brand)
    pr_obj_serialize = json.loads(serialize('json',pr_obj))
    pr_count = len(pr_obj_serialize)
    data = {'pr_obj':pr_obj_serialize,'pr_count':pr_count}

    print(data['pr_obj'][0]['pk'])
    return JsonResponse(data)