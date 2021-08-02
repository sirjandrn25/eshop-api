from django.db.models import base
from django.urls import path,include
from rest_framework.routers import SimpleRouter
from store.views import *



router = SimpleRouter()
router.register("fashions",FashionViewSet,basename="fashion")
router.register("categories",CategoryViewSet,basename="category")
router.register("products",ProductViewSet,basename="product")
router.register("product_sizes",ProductSizeViewSet,basename="product_size")
router.register("product_colors",ProductColorViewSet,basename="product_color")
router.register("carts",CartViewSet,basename="cart")
router.register("orders",OrderViewSet,basename="order")
router.register("product_color_images",ProductImageGallerViewSet,basename="product_color_image")



urlpatterns = [
    path("",include(router.urls)),
]
