from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('properties/', views.properties_view, name='properties'),
    path('property/<slug:slug>/', views.property_detail_view, name='property_detail'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('verify-email/<str:token>/', views.verify_email_view, name='verify_email'),
    path('verification-pending/', views.verification_pending_view, name='verification_pending'),
    path('resend-verification/', views.resend_verification_view, name='resend_verification'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
]
