from django.contrib import admin
from .models import *

# Register your models here.

class ProductDetailsinline(admin.TabularInline):
    model = ProductVariation

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('pr_brand','pr_name', 'pr_category', 'pr_quantity')
    list_filter = ('pr_brand',)

    inlines = [
        ProductDetailsinline,
    ]
    # inlines = ['MyInlineAdmin']



admin.site.register(Products, ProductsAdmin)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Category)
admin.site.register(ProductVariation)


