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
            if user.is_active == True:
                if user.blocked != True:
                    login(request,user)
                    return redirect('home')
                messages.add_message(request, messages.WARNING, 'Your account is blocked please contact admin')
                return redirect('login')
            messages.add_message(request, messages.WARNING, 'You do not have an active account')
            return redirect('login')
                
        else:
            messages.add_message(request, messages.WARNING, 'Invalid username or password')
            return redirect('login')

# user registration
def view_reg(request):
    try:
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
                messages.add_message(request, messages.SUCCESS, 'Account created successfully. Please login to continue')
                return redirect('login')
                
            else:
                messages.add_message(request, messages.WARNING, 'The form you submitted is not valid')
                return HttpResponseRedirect(request.path_info)
    except Exception as e:
        messages.add_message(request, messages.WARNING, 'An internal error occurred during operation')
        return HttpResponseRedirect(request.path_info)

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
            else:
                messages.add_message(request, messages.WARNING, 'Invalid email address')
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
    cart_obj = Cart.objects.filter(user_id=customer_id).all()
    for item in cart_obj:
        item.product_variation.price *= item.quantity
        total += item.product_variation.price
        total_items += item.quantity
    grand_total = total + 40 # Delivery fee
    context['data'] = cart_obj
    context['total'] = int(total)
    context['total_items'] = int(total_items)
    context['grand_total'] = int(grand_total)
    context['page'] = 'pages'
    return render(request, 'shopping-cart.html', context)

# items adding to cart
def add_to_cart(request):
    if request.user.is_authenticated:
        prod_var_id = request.GET['val']
        customer = request.user.id
        prod_var_obj = ProductVariation.objects.filter(id=prod_var_id).first()
        if prod_var_id:
            cart_obj, created = Cart.objects.get_or_create(product_variation_id=prod_var_id,user_id=customer, product_id=prod_var_obj.product_id)
            if created:
                quantity = 1
                cart_obj.quantity = quantity
                cart_obj.save()
                data = {'success':1}
                return JsonResponse(data)
            else:
                if cart_obj.quantity < prod_var_obj.quantity and cart_obj.quantity < 5:
                    cart_obj.quantity += 1
                    cart_obj.save()
                    data = {'success':2}
                    return JsonResponse(data)
                else:
                    data = {'success':0}
                    return JsonResponse(data)
        else:
            data = {'success':4}
            return JsonResponse(data)
    else:
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
    product_variation_id = request.GET['pr_id']
    product_variation_obj = ProductVariation.objects.get(id=product_variation_id)
    customer_id = request.user.id
    cart_obj = Cart.objects.get(user_id=customer_id,product_id=product_variation_obj.product_id, product_variation_id=product_variation_id)
    if int(val) == 1:
        if cart_obj.quantity < product_variation_obj.quantity and cart_obj.quantity < 5:
            cart_obj.quantity += 1
            cart_obj.product_variation.price *= cart_obj.quantity
            cart_obj.save()
            # total cart items price
            total = 0
            total_items = 0
            obj = Cart.objects.filter(user_id=customer_id)
            for item in obj:
                item.product_variation.price *= item.quantity
                total += item.product_variation.price
                total_items += item.quantity
            grand_total = total + 40 # Delivery fee
            data = {'cart_qty':cart_obj.quantity,'cart_price':cart_obj.product_variation.price,'success':1,'total':total, 'total_items':total_items, 'grand_total':grand_total}
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
                item.product_variation.price *= item.quantity
                total += item.product_variation.price
                total_items += item.quantity
            grand_total = total + 40 # Delivery fee
            data = {'cart_qty':0, 'total':total, 'total_items':total_items, 'grand_total':grand_total}
            return JsonResponse(data)
        else:
            cart_obj.product_variation.price *= cart_obj.quantity
            cart_obj.save()
            # total cart items price
            total = 0
            total_items = 0
            obj = Cart.objects.filter(user_id=customer_id)
            for item in obj:
                item.product_variation.price *= item.quantity
                total += item.product_variation.price
                total_items += item.quantity
            grand_total = total + 40 # Delivery fee
            data = {'cart_qty':cart_obj.quantity,'cart_price':cart_obj.product_variation.price,'total':total, 'total_items':total_items, 'grand_total':grand_total}
            return JsonResponse(data)

        
def cart_remove(request):
    try:
        if request.user.is_authenticated:
            product_variation_id = request.GET['pr_id']
            customer_id = request.user.id
            cart_obj = Cart.objects.filter(user_id=customer_id, product_variation_id=product_variation_id).first()
            if cart_obj:
                cart_obj.delete()
                total = 0
                total_items = 0
                cart_obj = Cart.objects.filter(user_id=customer_id)
                for item in cart_obj:
                    item.product_variation.price *= item.quantity
                    total += item.product_variation.price
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
            data = []
            amount = 0
            currency = 'INR'
            customer_id = request.user.id
            customer_obj = LoginTable.objects.filter(id=customer_id).first()
            if customer_obj:
                cart_obj = Cart.objects.select_related('product').filter(user_id=customer_id).all()
                # print('cartobj   ',cart_obj)
                # checking cart is empty or not
                if cart_obj:
                    address_obj = Address.objects.filter(customer_id = customer_id).first()
                    # for item in cart_obj:
                    #     if item.quantity <= item.product_variation.quantity:
                    #         item.product_variation.price *= item.quantity
                    #         total += item.product_variation.price
                    #         car_obj = Cart.objects.filter(user_id=customer_id)
                    #     elif item.product_variation.quantity == 0:
                    #         item.delete()
                    #         # cart object without outof stock product
                    #         car_obj = Cart.objects.filter(user_id=customer_id)
                    #     else:
                    #         item.quantity = item.product_variation.quantity
                    #         item.save()
                    subtotal_price = 0
                    for product in cart_obj:
                        if product.quantity > product.product_variation.quantity:
                            messages.add_message(request, messages.WARNING, 'Some products in your cart is out of stock for now. Please remove them to checkout.')
                            return redirect('cart')
                        else:
                            temp_data = {}
                            temp_data['product_name'] = product.product.pr_name
                            temp_data['total_per_item'] = product.product_variation.price * product.quantity
                            # print('temp_data---->>',temp_data)
                            subtotal_price += product.product_variation.price * product.quantity
                            
                            data.append(temp_data)

                    if address_obj:
                        context['line1'] = address_obj.line1
                        context['line2'] = address_obj.line2
                        context['city'] = address_obj.city
                        context['zipcode'] = address_obj.zipcode
                        context['state'] = address_obj.state

                    context['first_name'] = customer_obj.first_name
                    context['last_name'] = customer_obj.last_name
                    context['email'] = customer_obj.email
                    context['phone_no'] = customer_obj.phone_no
                    context['total_price'] = subtotal_price  + 40 # Delivery fee
                    context['subtotal_price'] = subtotal_price
    
                    context['data'] = data

                    
                    for item in cart_obj:
                        item.product_variation.price *= item.quantity
                        amount += item.product_variation.price
                    amount *= 100
                
                    # Create a Razorpay Order
                    razorpay_order = razor_pay_client.order.create(dict(amount=amount,
                                                                    currency=currency,
                                                                    payment_capture='0'))
                
                    # order id of newly created order.
                    razorpay_order_id = razorpay_order['id']
                    callback_url = 'paymenthandler/'
                
                    # we need to pass these details to frontend.
    
                    context['razorpay_order_id'] = razorpay_order_id
                    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
                    context['razorpay_amount'] = amount/100
                    context['currency'] = currency
                    context['callback_url'] = callback_url
                    context['email'] = customer_obj.email
                    context['phone'] = customer_obj.phone_no

                    # print(context)
                    # context['data'] = car_obj
                    return render(request,'checkout.html', context)
                else:
                    print('not')
                    messages.add_message(request, messages.WARNING, 'Your cart is empty. Please add some products to continue..')
                    return redirect('cart')
            else:
                messages.add_message(request, messages.WARNING, 'Unauthorized request')
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
    customer_obj = LoginTable.objects.get(id=request.user.id)

    amount = 0
    currency = 'INR'
    # if len(cart_obj) > 0:
    if len(cart_obj) == 0:
        messages.add_message(request, messages.WARNING, 'Your cart is empty. Can not make purchase')
        return HttpResponseRedirect(request.path_info)

    # elif order_count == 1:
    #     return HttpResponse('current order is processing.Wait until it reaches to you')
    
    else:
        for item in cart_obj:
            item.product_variation.price *= item.quantity
            amount += item.product_variation.price
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
        context['email'] = customer_obj.email
        context['phone'] = customer_obj.phone_no

    
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
                    item.product_variation.price *= item.quantity
                    amount += item.product_variation.price
                amount *= 100  
                try:

                    # capture the payemt
                    payment_capture = razor_pay_client.payment.capture(payment_id, amount)
                    if payment_capture is not None:     

                        # render success page on successful caputre of payment
                        new_order = Order.objects.create(user=request.user,
                                                    total_amount=amount/100,
                                                    order_status=1,
                                                    date_ordered=datetime.now(),
                                                    razor_pay_order_id=razorpay_order_id,
                                                    razor_pay_payment_id=payment_id,
                                                    razor_pay_signature=signature)
                        new_order.save()
                        for item in cart_obj:
                            new_order_detail = OrderDetails.objects.create(product=item.product,
                                                                           product_variation=item.product_variation,
                                                                           order=new_order,
                                                                           quantity=item.quantity,
                                                                           amount=item.product_variation.price)
                            new_order_detail.save()
                        cart_obj.delete()
                        
            
                        
                        order_detail_obj = OrderDetails.objects.filter(order_id=new_order.id)
                        for order_detail in order_detail_obj:
                            product_variation_obj = ProductVariation.objects.filter(id=order_detail.product_variation_id).first()
                            product_variation_obj.quantity -= item.quantity
                            product_variation_obj.save()
                        
                            if product_variation_obj.quantity == 0:
                                product_variation_obj.out_of_stock = True
                                product_variation_obj.save()
                            
                        # return HttpResponse('success order placed')
                        messages.add_message(request, messages.SUCCESS, 'Success order placed')
                        return redirect('order')
                    else:
                        return HttpResponse('payment is none')
                        messages.add_message(request, messages.WARNING, 'Payment is none')
                        return HttpResponseRedirect(request.path_info)
                except:
 
                    # if there is an error while capturing payment.
                    return HttpResponse('fail')
                    messages.add_message(request, messages.WARNING, 'Error occurred while capturing payment')
                    return HttpResponseRedirect(request.path_info)
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
        order_pr_obj = OrderDetails.objects.filter(order_id=order_id)
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