from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import generics, status, views, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from main.models import Post
from main.serializers import PostSerializer
from main.views import MyPaginations
from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer, UserProfileSerializer, \
    FollowSerializer
from .models import User
from .utils import Util
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import jwt


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        user_data = serializer.data

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')

        absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
        email_body = 'Hi, ' + user.username + ' Use link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email'}
        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter('token', in_= openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)


    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation link expired'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfile(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'username'
    permission_classes = [IsAuthenticated, ]


class OwnProfile(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None, pk=None):
        username = self.request.user.username
        query = get_user_model().objects.get(username=username)
        serializer = UserProfileSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FeedsView(APIView):
    permission_classes = [IsAuthenticated, ]
    pagination_class = MyPaginations

    def get(self, request, format=None, pk=None):
        user = self.request.user
        followings = user.followings.all()
        print(followings)
        posts = Post.objects.filter(user__in=followings)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None, username=None):
        to_user = get_user_model().objects.get(username=username)
        from_user = self.request.user
        follow = None
        if from_user != to_user:
            if from_user in to_user.followers.all():
                follow = False
                from_user.followings.remove(to_user)
                to_user.followers.remove(from_user)

            else:
                follow = True
                from_user.followings.add(to_user)
                to_user.followers.add(from_user)
        else:
            raise Exception('You cant follow yourself')
        context = {'follow': follow}
        return Response(context)


class GetFollowersView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        username = self.kwargs['username']
        queryset = get_user_model().objects.get(username=username).followers.all()
        return queryset


class GetFollowingsView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        username = self.kwargs['username']
        queryset = get_user_model().objects.get(username=username).followings.all()
        return queryset