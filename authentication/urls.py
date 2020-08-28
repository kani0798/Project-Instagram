from django.urls import path
from .views import (RegisterView, VerifyEmail, LoginAPIView, FollowUserView, UserProfile, GetFollowersView,
                    GetFollowingsView, OwnProfile, FeedsView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('profile/', OwnProfile.as_view(), name='own-profile'),
    path('feeds/', FeedsView.as_view(), name='feeds'),
    path('profile/<str:username>/', UserProfile.as_view(), name='user-profile'),
    path('profile/<str:username>/followers/', GetFollowersView.as_view(), name='followers'),
    path('profile/<str:username>/followings/', GetFollowingsView.as_view(), name='followings'),
    path('follow/<str:username>/', FollowUserView.as_view(), name='follow-user'),
]

