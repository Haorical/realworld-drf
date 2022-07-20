from users import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('users', views.RegistrationView.as_view(), name='registry'),
    path('users/login', views.LoginView.as_view(), name='login'),
    path('user', views.UserRUView.as_view(), name='user-update'),
]
