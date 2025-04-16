from django.shortcuts import render, redirect

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import generate_otp, send_otp_email
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from products.models import Order


class LoginWithOTP(APIView):
    def post(self, request):
        email = request.data.get('email', '')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        otp = generate_otp()
        user.otp = otp
        user.save()

        send_otp_email(email, otp)

        return Response({'message': 'OTP has been sent to your email.'}, status=status.HTTP_200_OK)
    

class ValidateOTP(APIView):
    def post(self, request):
        email = request.data.get('email', '')
        otp = request.data.get('otp', '')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if user.otp == otp:
            user.otp = None  
            user.save()

            
            token, _ = Token.objects.get_or_create(user=user)

            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        

# For registration
@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# For logout
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

        return redirect("/home")
    else:
        form = RegisterForm()

    return render(response, "register.html", {"form":form})


@login_required
def home(request):
    user = request.user
    orders = Order.objects.filter(customer=user)

    total_orders = orders.count()
    total_paid = sum(order.paid_amount for order in orders)
    total_due = sum(order.due_amount for order in orders)

    context = {
        "username": user.username,
        "total_orders": total_orders,
        "total_paid": total_paid,
        "total_due": total_due,
    }
    return render(request, "home.html", context)



# CustomLogin OTP view
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from .models import CustomUser
from .utils import send_otp_email, generate_otp  

class LoginWithOTPView(LoginView):
    template_name = 'login.html' 

    def form_valid(self, form):
        """Override default login flow to send OTP instead"""
        user = form.get_user()

        # Generate OTP
        user.otp = generate_otp() 
        user.save()
        send_otp_email(user.email, user.otp)

        self.request.session['temp_user_id'] = user.id

       
        return redirect('verify-otp')
    

from django.contrib.auth import login

def verify_otp_view(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        user_id = request.session.get('temp_user_id')

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid or expired session.")
            return redirect("login")

        if user.otp == entered_otp:
            login(request, user)  
            user.otp = ''
            user.save()
            del request.session['temp_user_id']
            return redirect("home")
        else:
            messages.error(request, "Incorrect OTP")

    return render(request, "verify_otp.html")