from django.contrib import admin
from .models import *

# Register your models here.

class ProductDetailsinline(admin.TabularInline):
    model = ProductDetails

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('pr_brand','pr_name','pr_price','pr_quantity')
    list_filter = ('pr_brand',)

    inlines = [
        ProductDetailsinline,
    ]




admin.site.register(Products, ProductsAdmin),

