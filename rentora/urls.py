from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rentals.urls')),
]

handler404 = 'rentals.views.custom_404_view'

