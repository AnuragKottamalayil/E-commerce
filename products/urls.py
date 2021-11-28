from django.urls import path
from .views import *

urlpatterns = [
    path('products/',view_product,name='products'),
    path('product_details/<int:id>/',product_details,name='products_details'),
    path('products/product_by_brand/',product_view_bybrand,name='product_view_bybrand')
]