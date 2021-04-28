from django.urls import path

from . import views

urlpatterns = [
    path('user/', views.create_user),
    path('auth_token/', views.generate_token),
]
