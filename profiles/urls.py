from django.urls import path
from profiles.views import ProfileView, FollowView


urlpatterns = [
    path('profiles/<str:username>', ProfileView.as_view()),
    path('profiles/<str:username>/follow', FollowView.as_view()),
    # path('profiles/<str:username>/follow', include('articles.urls')),
]