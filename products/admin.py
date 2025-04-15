from django.contrib import admin
from products.models import Product, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price','quantity') 
    search_fields = ['name']
    list_per_page = 5  

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'customer','paid_amount','due_amount','first_payment_date','next_due_date') 
    search_fields = ['customer__username']
    list_per_page = 5