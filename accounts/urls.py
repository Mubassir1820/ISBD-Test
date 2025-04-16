from django.urls import path
from .views import LoginWithOTP, ValidateOTP, register_user, user_logout
from . import views

urlpatterns = [
    path('api/register/', register_user, name='register_user'),
    path('api/login-with-otp/', LoginWithOTP.as_view(), name='login-with-otp'),
    path('api/validate-otp/', ValidateOTP.as_view(), name='validate-otp'),
    path('api/logout/', user_logout, name='logout'),
    path('register/', views.register, name='register'),
    # path('login/', views.login_page, name='login'),
    # path('verify-otp/', views.verify_otp_page, name='verify_otp'),
    # path('dashboard/', views.dashboard_page, name='dashboard'),
]

"ab2563c7df81501b1ed833cea3093c952f0e856f"