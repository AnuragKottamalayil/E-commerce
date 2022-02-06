from django.urls import path
from .views import *

urlpatterns = [
    path('login/',view_login,name='login'),
    path('register/',view_reg,name='register'),
    path('logout/',view_logout,name='logout'),
    path('forgot-password/',forgot_password,name='forgot-password'),
    path('verify-otp/',verify_otp,name='verify-otp'),
    path('reset-password/',reset_password,name='reset-password'),
    path('profile/',view_profile,name='profile'),
    path('cart/',view_cart,name='cart'),
    path('products/add_to_cart/',add_to_cart,name='add_to_cart'),
    path('profile/edit_profile/',edit_profile,name='edit_profile'),
    path('edit_profile_from_checkout/',edit_profile_from_checkout,name='edit_profile_from_checkout'),
    path('cart/plus_minus/',cart_plus_minus,name='cart_plus_minus'),
    path('cart/remove/',cart_remove,name='cart_remove'),
    path('checkout/',view_checkout,name='checkout'),
    path('payment/',payment,name='payment'),
    path('payment/paymenthandler/',paymenthandler,name='paymenthandler'),
    path('order/',order,name='order'),
    path('order/cancel_order/',cancel_order,name='cancel_order'),


]