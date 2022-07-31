from django.shortcuts import render
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView


class ProfileView(generics.RetrieveAPIView):
    queryset = Profile.objects.select_related('user')
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, username, *args, **kwargs):
        try:
            profile = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound("no profile!!!")
        print(request.user)
        serializer = self.serializer_class(profile, context={
            'request': request
        })
        return Response({'profile': serializer.data}, status=status.HTTP_200_OK)


class FollowView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def post(self, request, username):
        follower = self.request.user.profile
        followee = Profile.objects.get(user__username=username)
        follower.follow(followee)
        serializer = self.serializer_class(followee, context={
            'request': request
        })
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, username):
        follower = self.request.user.profile
        followee = Profile.objects.get(user__username=username)
        follower.unfollow(followee)
        serializer = self.serializer_class(followee, context={
            'request': request
        })
        return Response(serializer.data, status=status.HTTP_200_OK)