from datetime import timezone
from django.shortcuts import render
from .serializers import OrderSerializer, ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from django.db.models.functions import TruncWeek, TruncMonth
from django.db.models import Sum
from .models import Order
from time import timezone
from datetime import datetime, timedelta
from django.utils.timezone import now
import json

# Create your views here.
@api_view(['POST'])
def product_order(request):
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def orderCreate(request):
    if request.method == 'POST':
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={"success": "Order created successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weekly_payment_report(request):
    user = request.user
    weekly_data = (
        Order.objects.filter(customer=user)
        .annotate(week=TruncWeek('created_at'))
        .values('week')
        .annotate(total_paid=Sum('paid_amount'))
        .order_by('week')
    )
    return Response(weekly_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthly_payment_report(request):
    user = request.user
    monthly_data = (
        Order.objects.filter(customer=user)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total_paid=Sum('paid_amount'))
        .order_by('month')
    )
    return Response(monthly_data)



def dashboard_view(request):
    weekly_data = (
        Order.objects
        .annotate(week=TruncWeek('created_at'))
        .values('week')
        .annotate(total=Sum('paid_amount'))
        .order_by('week')
    )

    monthly_data = (
        Order.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('paid_amount'))
        .order_by('month')
    )

    weekly_labels = [item['week'].strftime('%Y-%m-%d') for item in weekly_data]
    weekly_totals = [float(item['total']) for item in weekly_data]

    monthly_labels = [item['month'].strftime('%B %Y') for item in monthly_data]
    monthly_totals = [float(item['total']) for item in monthly_data]

    context = {
        'weekly_labels': json.dumps(weekly_labels),
        'weekly_totals': json.dumps(weekly_totals),
        'monthly_labels': json.dumps(monthly_labels),
        'monthly_totals': json.dumps(monthly_totals),
    }
    return render(request, 'payment.html', context)