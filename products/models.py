
from django.db import models

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=200, verbose_name='Brand Name')
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name='Description')
    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=20, verbose_name='Color')
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Category Name')
    description = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.name


class Products(models.Model):
    pr_brand = models.ForeignKey(Brand, verbose_name='Brand Id', on_delete=models.CASCADE, null=True)
    pr_category = models.ForeignKey(Category, verbose_name='Category Id', on_delete=models.CASCADE, null=True)
    pr_name = models.CharField(max_length=200,verbose_name='Product Name')
    pr_quantity = models.IntegerField(verbose_name='Product Quantity', null=True, blank=True)
    active = models.BooleanField(default=True, null=True)
    out_of_stock = models.BooleanField(default=False, null=True)


    def __str__(self):
        return self.pr_name

# class ProductDetails(models.Model):
    # COLOR = (
    #     ('Red','Red'),
    #     ('Black','Black'),
    #     ('White','White'),
    #     ('Blue','Blue'),
    #     ('Silver','Silver'),
    #     ('Green','Green'),
    #     ('Yellow','Yellow'),
    #     ('Grey','Grey')
    # )
    # RAM = (
    #     ('4GB','4GB'),
    #     ('6GB','6GB'),
    #     ('8GB','8GB'),
    #     ('12GB','12GB'),
    # )
    # STORAGE = (
    #     ('32GB','32GB'),
    #     ('64GB','64GB'),
    #     ('128GB','128GB'),
    #     ('512GB','512GB'),
    # )
    # DISPLAY = (
    #     ('Amoled','Amoled'),
    #     ('SAmoled','SAmoled'),
    #     ('Oled','Oled'),
    #     ('LCD','LCD'),
    #     ('SuperRetina','SuperRetina'),
    #     ('SuperRetina XDR','SuperRetina XDR'),
    # )
    # CH = (
    #     ('Yes','Yes'),
    #     ('No','No')
    # )
    # pr = models.OneToOneField(Products,on_delete=models.CASCADE)
    # description = models.TextField(max_length=500,blank=True,null=True)
    # processor = models.CharField(max_length=100,blank=True,null=True)
    # camera = models.CharField(max_length=100,blank=True,null=True)
    # color = models.CharField(max_length=20,choices=COLOR,default = 'Red')
    # ram = models.TextField(max_length=10,choices=RAM,default = '4GB')
    # storage = models.TextField(max_length=10,choices=STORAGE,default = '32GB')
    # display = models.CharField(max_length=30,choices=DISPLAY,default = 'LCD')
    # battery = models.CharField(max_length=20)
    # removable_battery = models.CharField(max_length=30,choices=CH,default = 'No')
    # active = models.BooleanField(default=True, null=True)
    # out_of_stock = models.BooleanField(default=False, null=True)


    # def __str__(self):
        
    #     return (self.pr.pr_name) +' '+ (self.color) +' '+ (self.ram) +' '+ (self.storage)
    

class ProductVariation(models.Model):
    product = models.ForeignKey(Products, verbose_name='Product Id', on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Description')
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/',verbose_name='Product Image')
    price = models.FloatField(verbose_name='Product Price')
    quantity = models.IntegerField(verbose_name='Product Quantity')
    active = models.BooleanField(default=True, null=True)
    out_of_stock = models.BooleanField(default=False, null=True)
    

