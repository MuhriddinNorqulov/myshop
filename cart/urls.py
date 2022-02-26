from django.urls import path
from .views import add, remove

app_name = 'cart'

urlpatterns = [
    path('add/', add, name='add-cart'),
    path('remove/', remove, name='remove-cart'),
]