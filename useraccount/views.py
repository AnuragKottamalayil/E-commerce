import json
from django.contrib import auth
import razorpay
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import RegisterForm,LoginForm,UpdateProfileForm
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.http import JsonResponse
from products.models import Products
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


# Authorizing razorpay client

razor_pay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))

# user login
def view_login(request):
    if request.method == 'GET':
        context = {}
        form_obj = LoginForm
        context['form'] = form_obj
        return render(request,'login.html',context)
    elif request.method == 'POST':
        form_obj = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse('error')

# user registration
def view_reg(request):
    if request.method == 'GET':
        context = {}
        form_obj = RegisterForm()
        context['form'] = form_obj
        return render(request,'register.html',context)
    elif request.method == 'POST':
        form_obj = RegisterForm(request.POST)
        password = request.POST['password']
        if form_obj.is_valid:
            obj = form_obj.save(commit=False)
            obj.set_password(password)
            obj.save()
            return redirect('login')
        else:
            return HttpResponse('error')

# user logout
def view_logout(request):
    logout(request)
    return redirect('home')

# user profile
def view_profile(request):
    context = {}
    customer_id = request.user.id
    cust_obj = LoginTable.objects.get(id=customer_id)
    context['data'] = cust_obj
    return render(request,'profile.html',context)

# user cart
def view_cart(request):
    context = {}
    total = 0
    customer_id = request.user.id
    obj = Cart.objects.filter(user_id=customer_id)
    for item in obj:
        item.product.pr_price *= item.quantity
        total += item.product.pr_price
    context['data'] = obj
    context['total'] = total
    return render(request,'cart.html',context)

# items adding to cart
def add_to_cart(request):
    if request.user.is_authenticated:
        pr_id = request.GET['val']
        customer = request.user.id
        pr_obj = Products.objects.get(id=pr_id)
        obj, created = Cart.objects.get_or_create(product_id=pr_id,user_id=customer)
        if created:
            quantity = 1
            obj.quantity = quantity
            obj.save()
            data = {'success':1}
            return JsonResponse(data)
        else:
            if obj.quantity < pr_obj.pr_quantity and obj.quantity < 5:
                obj.quantity += 1
                obj.save()
                data = {'success':2}
                return JsonResponse(data)
            else:
                data = {'success':0}
                return JsonResponse(data)
    else:
        print('not logged')
        pr_id = request.GET['val']
        data = {'success':3}
        return JsonResponse(data)

# user editing profile
def edit_profile(request):
    customer_id = request.user.id
    customer_obj = LoginTable.objects.get(id=customer_id)
        
    if request.method == 'GET':
        context = {}
        form_obj = UpdateProfileForm(instance=customer_obj)
        context['form'] = form_obj
        return render(request,'edit_profile.html',context)
    elif request.method == 'POST':
        form_obj = UpdateProfileForm(data=request.POST, instance=customer_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('profile')


# editing the address field from checkout page

def edit_profile_from_checkout(request):
    customer_id = request.user.id
    cust_obj = LoginTable.objects.get(id=customer_id)

    if request.method == "POST":
        address = request.POST['address']
        zip = request.POST['zip']
        cust_obj.address = address
        cust_obj.zipcode = zip
        cust_obj.save()
        data = {'status':1,'address':cust_obj.address, 'zip':cust_obj.zipcode}
        return JsonResponse(data)
    elif request.method == "GET":
        return render(request,'checkout.html')


# removing and adding items in cart

def cart_plus_minus(request):
    val = request.GET['val']
    pr_id = request.GET['pr_id']
    pr_obj = Products.objects.get(id=pr_id)
    customer_id = request.user.id
    cart_obj = Cart.objects.get(user_id=customer_id,product_id=pr_id)
    if int(val) == 1:
        if cart_obj.quantity < pr_obj.pr_quantity and cart_obj.quantity < 5:
            cart_obj.quantity += 1
            cart_obj.product.pr_price *= cart_obj.quantity
            cart_obj.save()
            # total cart items price
            total = 0
            obj = Cart.objects.filter(user_id=customer_id)
            for item in obj:
                item.product.pr_price *= item.quantity
                total += item.product.pr_price
            
            data = {'cart_qty':cart_obj.quantity,'cart_price':cart_obj.product.pr_price,'success':1,'total':total}
            return JsonResponse(data)
        else:
            return JsonResponse('outof stock',safe=False)
    else:
        cart_obj.quantity -= 1
        if cart_obj.quantity == 0:
            cart_obj.delete()
            data = {'cart_qty':0}
            return JsonResponse(data)
        else:
            cart_obj.product.pr_price *= cart_obj.quantity
            cart_obj.save()
            # total cart items price
            total = 0
            obj = Cart.objects.filter(user_id=customer_id)
            for item in obj:
                item.product.pr_price *= item.quantity
                total += item.product.pr_price
            data = {'cart_qty':cart_obj.quantity,'cart_price':cart_obj.product.pr_price,'total':total}
            return JsonResponse(data)

# check out page
def view_checkout(request):
    if request.user.is_authenticated:  
        context = {}
        total = 0
        customer_id = request.user.id
        cust_details_obj = LoginTable.objects.get(id=customer_id)
        cart_obj = Cart.objects.filter(user_id=customer_id)
        # checking cart is empty or not
        if len(cart_obj) > 0:
            for item in cart_obj:
                if item.quantity <= item.product.pr_quantity:
                    item.product.pr_price *= item.quantity
                    total += item.product.pr_price
                    car_obj = Cart.objects.filter(user_id=customer_id)
                elif item.product.pr_quantity == 0:
                    item.delete()
                    # cart object without outof stock product
                    car_obj = Cart.objects.filter(user_id=customer_id)
                else:
                    item.quantity = item.product.pr_quantity
                    print(item.quantity)
                    item.save()
            context['details'] = cust_details_obj
            context['total'] = total
            context['data'] = car_obj
            return render(request,'checkout.html',context)
        else:
            context['details'] = cust_details_obj
            context['total'] = total
            return render(request,'checkout.html',context)
    else:
        return redirect('login')
# Test payment using Razorpay

def payment(request):
    cart_obj = Cart.objects.filter(user_id=request.user.id)
    cust_obj = LoginTable.objects.get(id=request.user.id)
    order_count = Order.objects.filter(user=request.user).count()
    print(order_count)
    amount = 0
    currency = 'INR'
    # if len(cart_obj) > 0:
    if len(cart_obj) == 0:
        return HttpResponse('No items in cart.add some!!')

    # elif order_count == 1:
    #     return HttpResponse('current order is processing.Wait until it reaches to you')
    
    else:
        for item in cart_obj:
            item.product.pr_price *= item.quantity
            amount += item.product.pr_price
        amount *= 100
    
        # Create a Razorpay Order
        razorpay_order = razor_pay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))
    
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = 'paymenthandler/'
    
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount/100
        context['currency'] = currency
        context['callback_url'] = callback_url
        context['email'] = cust_obj.email
        context['phone'] = cust_obj.phone_no

    
        return render(request,'payment.html',context=context)

@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razor_pay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                amount = 0
                cart_obj = Cart.objects.filter(user_id=request.user.id)
                for item in cart_obj:
                    item.product.pr_price *= item.quantity
                    amount += item.product.pr_price
                amount *= 100  
                try:

                    # capture the payemt
                    payment_capture = razor_pay_client.payment.capture(payment_id, amount)
                    print(payment_capture)
                    if payment_capture is not None:     

                        # render success page on successful caputre of payment
                        order = Order.objects.create(user=request.user,
                                                    total_amount=amount/100,
                                                    razor_pay_order_id=razorpay_order_id,
                                                    razor_pay_payment_id=payment_id,
                                                    razor_pay_signature=signature)
                        order.save()
                        for item in cart_obj:
                            order_product = OrderProducts.objects.create(product=item.product,
                                                                        order=order,
                                                                        quantity=item.quantity,
                                                                        price=item.product.pr_price)
                            order_product.save()
                        cart_obj.delete()
                        
            
                        
                        order_product_obj = OrderProducts.objects.filter(order_id=order.id)
                        for item in order_product_obj:
                            product_obj = Products.objects.get(id=item.product_id)
                            product_obj.pr_quantity -= item.quantity
                            product_obj.save()
                            
                        return HttpResponse('success order placed')
                    else:
                        return HttpResponse('payment is none')
                except:
 
                    # if there is an error while capturing payment.
                    return HttpResponse('fail')
            else:
 
                # if signature verification fails.
                return HttpResponse('signature fail')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponse('No params in POST data')
    else:
       # if other than POST request is made.
        return HttpResponse('Request otherthan POST')

# To view order details
def order(request):
    if request.method == 'GET':
        context = {}
        cust_id = request.user.id
        order_obj = Order.objects.filter(user_id=cust_id)
        context['order_obj'] = order_obj
        return render(request,'order.html',context)
    elif request.method == 'POST':
        order_id = request.POST['order_id']
        print(order_id)
        context = {}
        status = 0
        order_pr_obj = OrderProducts.objects.filter(order_id=order_id)
        for order_item in order_pr_obj:
            status += order_item.order.status
            break
        context['status'] = status
        context['order_id'] = order_id
        context['order_pr_obj'] = order_pr_obj
        return render(request,'order_details.html',context)
        

# order cancel
def cancel_order(request):
    order_id = request.POST['order_id']

    order_obj = Order.objects.get(id=order_id)
    print(order_obj.status)
    order_obj.status = 5
    order_obj.save()
    return JsonResponse('hai',safe=False)

