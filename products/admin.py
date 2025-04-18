from django.contrib import admin
from products.models import Product, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price','quantity') 
    search_fields = ['name']
    list_per_page = 5  

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'product', 'customer','paid_amount','due_amount','first_payment_date','next_due_date') 
#     search_fields = ['customer__username']
#     list_per_page = 5





from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'paid_amount', 'due_amount', 'first_payment_date', 'created_at')
    list_filter = ('created_at',)  
    change_list_template = "orders_changelist.html"
    search_fields = ['customer__username']
    list_per_page = 5

    def changelist_view(self, request, extra_context=None):
        today = timezone.now().date()

        one_week_ago = today - timedelta(days=7)
        one_month_ago = today - timedelta(days=30)

        weekly_orders = Order.objects.filter(created_at__date__gte=one_week_ago)
        monthly_orders = Order.objects.filter(created_at__date__gte=one_month_ago)

        weekly_paid = weekly_orders.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
        weekly_due = weekly_orders.aggregate(Sum('due_amount'))['due_amount__sum'] or 0

        monthly_paid = monthly_orders.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
        monthly_due = monthly_orders.aggregate(Sum('due_amount'))['due_amount__sum'] or 0

        extra_context = extra_context or {}
        extra_context['weekly_paid'] = weekly_paid
        extra_context['weekly_due'] = weekly_due
        extra_context['monthly_paid'] = monthly_paid
        extra_context['monthly_due'] = monthly_due

        return super().changelist_view(request, extra_context=extra_context)