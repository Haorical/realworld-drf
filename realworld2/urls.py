from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('users.urls')),
    path('api/', include('profiles.urls')),
    # path('api/articles/', include('articles.urls')),
    # path('api/tags/', include('articles.urls')),
]
