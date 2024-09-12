from django.urls import path
from . import views

urlpatterns = [
    # Example URL pattern
    path('', views.index, name='blog-home'),  # Modify this according to your view
]
