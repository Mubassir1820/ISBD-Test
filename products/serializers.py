from rest_framework import serializers
from .models import Order, Product
from accounts.models import CustomUser
from rest_framework.fields import CurrentUserDefault


class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order

        fields = ['id','product','quantity','paid_amount','total_cost','due_amount']
        read_only_fields = ['total_cost','due_amount']


    def create(self, validated_data):
        product = validated_data['product']
        quantity = validated_data['quantity']
        paid = validated_data.get('paid_amount', 0)

        total_cost = product.price * quantity
        due_amount = total_cost - paid

        return Order.objects.create(
            customer = self.context['request'].user,
            product=product,
            quantity=quantity,
            paid_amount=paid,
            total_cost=total_cost,
            due_amount=due_amount
        )
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product

        fields = ['id','name','price','quantity']
        