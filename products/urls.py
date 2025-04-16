from django.urls import path
from . import views

urlpatterns = [
    path("api/products/", views.product_order ,name="product_order"),
    path("api/orders/", views.orderCreate ,name="orderCreate"),
    # path("api/dashboard/", views.dashboard_view, name='dashboard'),
 ]