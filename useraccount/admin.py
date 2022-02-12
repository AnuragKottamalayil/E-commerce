from django.contrib import admin
from .models import *


# class OrderProductsInline(admin.TabularInline):
#     model = OrderProducts

# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('user','total_amount','status','date_ordered')
#     list_filter = ('status',)
#     inlines = [OrderProductsInline,]

admin.site.register(Cart),
# admin.site.register(Order, OrderAdmin),
