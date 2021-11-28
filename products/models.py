from django.db import models

# Create your models here.

class Products(models.Model):
    BRAND = (
        ('Apple','Apple'),
        ('Samsung','Samsung'),
        ('Redmi','Redmi'),
        ('Realme','Realme'),
        ('Oppo','Oppo'),
        ('Vivo','Vivo'),
        ('Moto','Moto'),
        ('Oneplus','Oneplus')
    )
    pr_brand = models.CharField(max_length=200,verbose_name='Brand',choices=BRAND,default = 'Apple')
    pr_name = models.CharField(max_length=200,verbose_name='product name')
    pr_price = models.FloatField(verbose_name='product price')
    pr_quantity = models.IntegerField(verbose_name='product quantity')
    pr_image = models.ImageField(upload_to='images/',verbose_name='product image')


    def __str__(self):
        return self.pr_name

class ProductDetails(models.Model):
    COLOR = (
        ('Red','Red'),
        ('Black','Black'),
        ('White','White'),
        ('Blue','Blue'),
        ('Silver','Silver'),
        ('Green','Green'),
        ('Yellow','Yellow'),
        ('Grey','Grey')
    )
    RAM = (
        ('4GB','4GB'),
        ('6GB','6GB'),
        ('8GB','8GB'),
        ('12GB','12GB'),
    )
    STORAGE = (
        ('32GB','32GB'),
        ('64GB','64GB'),
        ('128GB','128GB'),
        ('512GB','512GB'),
    )
    DISPLAY = (
        ('Amoled','Amoled'),
        ('SAmoled','SAmoled'),
        ('Oled','Oled'),
        ('LCD','LCD'),
        ('SuperRetina','SuperRetina'),
        ('SuperRetina XDR','SuperRetina XDR'),
    )
    CH = (
        ('Yes','Yes'),
        ('No','No')
    )
    pr = models.OneToOneField(Products,on_delete=models.CASCADE)
    description = models.TextField(max_length=500,blank=True,null=True)
    processor = models.CharField(max_length=100,blank=True,null=True)
    camera = models.CharField(max_length=100,blank=True,null=True)
    color = models.CharField(max_length=20,choices=COLOR,default = 'Red')
    ram = models.TextField(max_length=10,choices=RAM,default = '4GB')
    storage = models.TextField(max_length=10,choices=STORAGE,default = '32GB')
    display = models.CharField(max_length=30,choices=DISPLAY,default = 'LCD')
    battery = models.CharField(max_length=20)
    removable_battery = models.CharField(max_length=30,choices=CH,default = 'No')
    def __str__(self):
        
        return (self.pr.pr_name) +' '+ (self.color) +' '+ (self.ram) +' '+ (self.storage)
    