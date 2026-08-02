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
    path('test-email/', views.test_email_view, name='test_email'),
]
