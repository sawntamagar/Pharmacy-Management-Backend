from django.urls import path
from rest_framework import routers


from inventory.views import (
    ProductInventoryViewSet,ProductViewSet,
    CategoryViewSet, BrandViewSet, StockViewSet)

router = routers.DefaultRouter()
router.register(r"productinventory", ProductInventoryViewSet, basename="inventory")
router.register(r"products", ProductViewSet, basename="products")
router.register(r"category", CategoryViewSet, basename="categories")
router.register(r"stock", StockViewSet, basename="stocks")
router.register(r"brand", BrandViewSet, basename="brand")




urlpatterns =  router.urls
