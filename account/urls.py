from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]


