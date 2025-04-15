from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.product_order ,name="product_order"),
    path("orders/", views.orderCreate ,name="orderCreate"),
 ]


"ab2563c7df81501b1ed833cea3093c952f0e856f"