from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.enums import Choices
from django.db.models.fields import BigIntegerField
from products.models import Products
from django.utils import timezone

# Create your models here.

class LoginTable(AbstractUser):
    phone_no = models.BigIntegerField(null=True,blank=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    zipcode = models.IntegerField(null=True,blank=True)

class Cart(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    user = models.ForeignKey(LoginTable,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username

class Order(models.Model):
    STATUS = (
        (1,'Not packed'),
        (2,'Packed'),
        (3,'Shipped'),
        (4,'Delivered'),
        (5,'Canceled'),
        
    )
    user = models.ForeignKey(LoginTable,on_delete=models.SET_NULL,null=True)
    total_amount = models.FloatField()
    status = models.IntegerField(max_length=50,choices=STATUS,default=1)
    date_ordered = models.DateTimeField(default=timezone.now)
    razor_pay_order_id = models.CharField(max_length=50,null=True,blank=True)
    razor_pay_payment_id = models.CharField(max_length=50,null=True,blank=True)
    razor_pay_signature = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.user.username

class OrderProducts(models.Model):
    product = models.ForeignKey(Products,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0)
    price = models.FloatField()

    def __str__(self):
        return self.order.user.username