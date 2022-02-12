
from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser
from products.models import Products, ProductVariation
from django.utils import timezone
from datetime import date, datetime
# Create your models here.

class LoginTable(AbstractUser):
    phone_no = models.BigIntegerField(null=True,blank=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    zipcode = models.IntegerField(null=True,blank=True)

class Cart(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    product_variation = models.ForeignKey(ProductVariation,on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(LoginTable,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username

class Order(models.Model):
    ORDER_STATUS = (
        (1,'Not packed'),
        (2,'Packed'),
        (3,'Shipped'),
        (4,'Delivered'),
        (5,'Canceled'),
        
    )
    PAYMENT_STATUS = (
        (1,'Success'),
        (2,'Pending'),
        (3,'Failed')
        
    )
    user = models.ForeignKey(LoginTable,on_delete=models.SET_NULL,null=True)
    total_amount = models.FloatField()
    order_status = models.IntegerField(choices=ORDER_STATUS,default=1)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default=2)
    date_ordered = models.DateTimeField(default=datetime.now())
    razor_pay_order_id = models.CharField(max_length=50,null=True,blank=True)
    razor_pay_payment_id = models.CharField(max_length=50,null=True,blank=True)
    razor_pay_signature = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.user.username

class OrderDetails(models.Model):
    product = models.ForeignKey(Products,on_delete=models.SET_NULL,null=True)
    product_variation = models.ForeignKey(ProductVariation,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0)
    amount = models.FloatField()
    created = models.DateTimeField(default=datetime.now())
    modified = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.order.user.username

class CustomerOtp(models.Model):
    email = models.TextField()
    otp = models.TextField()
    created = models.DateTimeField(default=datetime.now())
    modified = models.DateTimeField(default=datetime.now())
    verified = models.BooleanField(default=False)
