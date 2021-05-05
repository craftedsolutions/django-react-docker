from django.urls import re_path, path, include

from . import views

urlpatterns = [
    path('api/user_details/', views.get_user_details),
    re_path(r'^api/', include('djoser.urls')),
    re_path(r'^api/', include('djoser.urls.authtoken')),
    # path('user/', views.create_user),
    # path('auth_token/', views.generate_token),
]
