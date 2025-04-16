from django.urls import path
from .views import LoginWithOTP, LoginWithOTPView,  ValidateOTP, register_user, user_logout, verify_otp_view
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('api/register/', register_user, name='register_user'),
    path('api/login-with-otp/', LoginWithOTP.as_view(), name='login-with-otp'),
    path('api/validate-otp/', ValidateOTP.as_view(), name='validate-otp'),
    path('api/logout/', user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path("login/", LoginWithOTPView.as_view(), name="login"),
    path("verify-otp/", verify_otp_view, name="verify-otp"),
]

"ab2563c7df81501b1ed833cea3093c952f0e856f"