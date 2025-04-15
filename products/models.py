from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    

class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    first_payment_date = models.DateField(default=timezone.now)
    next_due_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.total_cost:
            self.total_cost = self.product.price * self.quantity
        self.due_amount = self.total_cost - self.paid_amount

        
        if self.due_amount > 0 and not self.next_due_date:
            self.next_due_date = self.first_payment_date + timedelta(days=30)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order:{self.pk}, Customer: {self.customer.email}"