from django.urls import path
from .views import add, remove

urlpatterns = [
    path('add/', add, name='add-wishlist'),
    path('remove/', remove, name='remove-wishlist'),
]