from datetime import timedelta
import razorpay
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ForgotPasswordForm, RegisterForm,LoginForm, ResetPasswordForm,UpdateProfileForm, VerifyOtpForm
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.http import JsonResponse
from products.models import Products
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import random
from django.contrib import messages

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
            messages.add_message(request, messages.WARNING, 'Invalid username or password')
            return redirect('login')

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
    return redirect('login')

# Forgot password
def forgot_password(request):
    try:
        context = {}
        if request.method == 'GET':

            form_obj = ForgotPasswordForm()
            context['form'] = form_obj
            return render(request, 'forgot_password.html', context)
        elif request.method == 'POST':
            form_obj = ForgotPasswordForm(data=request.POST)
            if form_obj.is_valid():

                email = form_obj.cleaned_data['email']
                db_logintable = LoginTable.objects.filter(email = email).first()
                if db_logintable:

                    request.session['email'] = email
                    otp = generate_otp()
                    is_otp_saved = save_otp(email, int(otp))
                    if is_otp_saved:

                        print('Your otp is :: ' + str(otp))
                        form_obj = VerifyOtpForm()
                        context['form'] = form_obj
                        return render(request, 'verify_otp.html', context)
                    else:
                        messages.add_message(request, messages.WARNING, 'Otp not send. Please send again')
                        return HttpResponseRedirect(request.path_info)
                else:
                  
                    messages.add_message(request, messages.WARNING, 'This email id does not belongs to our company')
                    return HttpResponseRedirect(request.path_info)

    except Exception as e:
        messages.add_message(request, messages.WARNING, 'An internal error occurred during operation')
        return HttpResponseRedirect(request.path_info)

def verify_otp(request):
    try:
        context = {}
        if request.method == "GET":
            form_obj = VerifyOtpForm()
            context['form'] = form_obj
            return render(request, 'verify_otp.html', context)
        elif request.method == "POST":
            form_obj = VerifyOtpForm(data=request.POST)
            if form_obj.is_valid():

                otp = form_obj.cleaned_data['otp']
                if 'email' in request.session:
                    email = request.session['email']
                
                is_verified, msg = verify_email_otp(email, otp)
                if is_verified:
                    form_obj = ResetPasswordForm()
                    context['form'] = form_obj
                    messages.add_message(request, messages.SUCCESS, msg)
                    return render(request, 'reset_password.html', context)

                else:
                    messages.add_message(request, messages.WARNING, msg)
                    return HttpResponseRedirect(request.path_info)
               
    except Exception as e:
        messages.add_message(request, messages.WARNING, 'An internal error occurred during operation')
        return HttpResponseRedirect(request.path_info)


def reset_password(request):
    try:
        context = {}
        if request.method == "GET":
            return render(request, 'reset_password.html')

        elif request.method == "POST":
            form_obj = ResetPasswordForm(data=request.POST)
            if form_obj.is_valid():
                password = form_obj.cleaned_data['password']
                if 'email' in request.session:
                    email = request.session['email']
                
                db_otp = CustomerOtp.objects.filter(email = email).first()
                if db_otp:
                    if db_otp.verified == True:
                        db_logintable = LoginTable.objects.filter(email = email).first()
                        if db_logintable:
                            db_logintable.set_password(password)
                            db_logintable.save()
                            messages.add_message(request, messages.SUCCESS, 'Password reset success. Please login to continue')
                            return redirect('login')
                        else:
                            messages.add_message(request, messages.WARNING, 'User data not found')
                            return HttpResponseRedirect(request.path_info)
                
                    else:
                        
                        messages.add_message(request, messages.WARNING, 'You are not verified the otp to reset the password')
                        return HttpResponseRedirect(request.path_info)
                
                else:
                    messages.add_message(request, messages.WARNING, 'You are not verified the otp to reset the password')
                    return HttpResponseRedirect(request.path_info)
    
    

    except Exception as e:
        messages.add_message(request, messages.WARNING, 'An internal error occurred during operation')
        return HttpResponseRedirect(request.path_info)

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
    total_items = 0
    customer_id = request.user.id
    cart_obj = Cart.objects.filter(user_id=customer_id)
    for item in cart_obj:
        item.product.pr_price *= item.quantity
        total += item.product.pr_price
        total_items += item.quantity
    grand_total = total + 40 # Delivery fee
    context['data'] = cart_obj
    context['total'] = int(total)
    context['total_items'] = int(total_items)
    context['grand_total'] = int(grand_total)
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
            total_items = 0
            obj = Cart.objects.filter(user_id=customer_id)
            for item in obj:
                item.product.pr_price *= item.quantity
                total += item.product.pr_price
                total_items += item.quantity
            grand_total = total + 40 # Delivery fee
            data = {'cart_qty':cart_obj.quantity,'cart_price':cart_obj.product.pr_price,'success':1,'total':total, 'total_items':total_items, 'grand_total':grand_total}
            return JsonResponse(data)
        else:
            return JsonResponse('outof stock',safe=False)
    else:
        cart_obj.quantity -= 1
        if cart_obj.quantity == 0:
            cart_obj.delete()
            total = 0
            total_items = 0
            obj = Cart.objects.filter(user_id=customer_id)
            for item in obj:
                item.product.pr_price *= item.quantity
                total += item.product.pr_price
                total_items += item.quantity
            grand_total = total + 40 # Delivery fee
            data = {'cart_qty':0, 'total':total, 'total_items':total_items, 'grand_total':grand_total}
            return JsonResponse(data)
        else:
            cart_obj.product.pr_price *= cart_obj.quantity
            cart_obj.save()
            # total cart items price
            total = 0
            total_items = 0
            obj = Cart.objects.filter(user_id=customer_id)
            for item in obj:
                item.product.pr_price *= item.quantity
                total += item.product.pr_price
                total_items += item.quantity
            grand_total = total + 40 # Delivery fee
            data = {'cart_qty':cart_obj.quantity,'cart_price':cart_obj.product.pr_price,'total':total, 'total_items':total_items, 'grand_total':grand_total}
            return JsonResponse(data)

        
def cart_remove(request):
    try:
        if request.user.is_authenticated:
            pr_id = request.GET['pr_id']
            customer_id = request.user.id
            cart_obj = Cart.objects.filter(user_id=customer_id, product_id=pr_id).first()
            if cart_obj:
                cart_obj.delete()
                total = 0
                total_items = 0
                cart_obj = Cart.objects.filter(user_id=customer_id)
                for item in cart_obj:
                    item.product.pr_price *= item.quantity
                    total += item.product.pr_price
                    total_items += item.quantity
                grand_total = total + 40 # Delivery fee
                data = {'total':total, 'total_items':total_items, 'grand_total':grand_total, 'status': True, 'msg': 'Product removed form cart'}
                return JsonResponse(data)
            else:
                data = {'success':3, 'status': False, 'msg': "No cart data found"}
                return JsonResponse(data)
        else:
            data = {'success':3, 'status': False, 'msg': "Unauthorized access"}
            return JsonResponse(data)

    except Exception as e:
        data = {'success':3, 'status': False, 'msg': "Internal error occurred"}
        return JsonResponse(data)


# check out page
def view_checkout(request):
    try:
        if request.user.is_authenticated:  
            context = {}
            total = 0
            customer_id = request.user.id
            cust_details_obj = LoginTable.objects.get(id=customer_id)
            cart_obj = Cart.objects.filter(user_id=customer_id).all()
            # checking cart is empty or not
            if cart_obj:
                print('yes')
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
                context['total'] = total + 40
                context['data'] = car_obj
                return render(request,'checkout.html',context)
            else:
                print('not')
                messages.add_message(request, messages.WARNING, 'Your cart is empty. Please add some products to continue..')
                return redirect('cart')
        else:
            messages.add_message(request, messages.WARNING, 'Please login to continue..')
            return redirect('cart')
    except Exception as e:
        print(e)
        messages.add_message(request, messages.WARNING, 'An internal error occurred during operation')
        return redirect('cart')
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
                        
                        if product_obj.pr_quantity == 0:
                            product_obj.out_of_stock = True
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
    order_obj.status = 5
    order_obj.save()
    return JsonResponse('hai',safe=False)

def generate_otp():
    numbers = '1234567890'
    ot = random.choices(numbers, k = 4)
    otp=''.join(ot)
    otp = 1234
    return otp

def save_otp(email, otp):
    try:
        db_otp = CustomerOtp.objects.filter(email = email).first()
        if db_otp:
            db_otp.otp = otp
            db_otp.created = datetime.now()
            db_otp.modified = datetime.now()
            db_otp.verified = False
            db_otp.save()
        else:
            new_otp = CustomerOtp.objects.create(email=email, otp=otp, created=datetime.now(), modified=datetime.now(), verified=False)
            new_otp.save()

        return True

    except Exception as e:
        return False

def verify_email_otp(email, otp):
    try:
        db_otp = CustomerOtp.objects.filter(email=email).first()
        if db_otp:
            
            current_time = datetime.now().replace(tzinfo=timezone.utc)
            otp_created_time = db_otp.created.replace(tzinfo=timezone.utc)
            otp_expire_time = otp_created_time + timedelta(minutes=15)
            if current_time <= otp_expire_time:
                if str(db_otp.otp) == str(otp):
                    db_otp.verified = True
                    db_otp.save()
                    return True, 'OTP verified, You can now reset password'
                else:
                    return False, 'Invalid OTP, Please enter correct OTP'
            else:
                return False, 'OTP expired. Please send again'
        else:
            return False, 'No otp requested yet'

    except Exception as e:
        print('error-------->>',e)
        return False, 'Error while verifying otp'