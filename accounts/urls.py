from django.urls import path
from .views import LoginWithOTP, ValidateOTP, register_user, user_logout

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login-with-otp/', LoginWithOTP.as_view(), name='login-with-otp'),
    path('validate-otp/', ValidateOTP.as_view(), name='validate-otp'),
    path('logout/', user_logout, name='logout'),
]