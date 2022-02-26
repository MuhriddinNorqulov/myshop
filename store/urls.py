# from django.conf.urls import url
from django.urls import path
from .views import index, product_detail, shopping_cart, wishlist, checkout, product_search

app_name = 'store'

urlpatterns = [
    path('', index, name='store'),
    path('shopping/cart/', shopping_cart, name='shopping-cart'),
    path('wishlist/', wishlist, name='wishlist'),
    path('product/detail/<slug:product_slug>/', product_detail, name='product-detail'),
    path('checkout/', checkout, name='checkout'),
    path('search/', product_search, name='product-search')
]