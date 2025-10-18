from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_redirect, name='home'), 
    path('register/user/', views.register_user_view, name='register_user'),
    path('register/admin/', views.register_admin_view, name='register_admin'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
]
