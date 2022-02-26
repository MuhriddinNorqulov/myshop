from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register(r"products", views.ProductViewSet)
router.register(r"categorys", views.CategoryViewSet)