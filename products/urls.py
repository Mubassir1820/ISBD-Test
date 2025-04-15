from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.product_order ,name="product_order"),
    path("orders/", views.orderCreate ,name="orderCreate"),
 ]