from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Registration & Login
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    
    # Protected page
    path('welcome/', views.welcome, name='welcome'),
    
    # Password Reset
    path('forgot-password/', views.send_password_reset, name='forgot_password'),
    path('reset_password/<str:token>/', views.reset_user_password, name='password_reset_token'),
    path('reset_password_complete/', views.reset_password, name='password_reset_complete'),
]
