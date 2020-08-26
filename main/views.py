from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, generics, status
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Comment
from .permissions import IsPostAuthor, IsCommentAuthor
from .serializers import PostSerializer, CommentSerializer


class MyPaginations(PageNumberPagination):
    page_size = 3


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = MyPaginations
    permission_classes = [IsAuthenticated, ]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_permissions(self):
        """Переопределяем метод"""
        if self.action in ['create', 'myposts']:
            permissions = [IsAuthenticated, ]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthenticated, IsPostAuthor]
        else:
            permissions = []
        return [permission() for permission in permissions]

    @action(detail=False, methods=['get'])
    def myposts(self, request, pk=None):
        u = request.query_params.get('u')
        queryset = self.get_queryset()
        if u:
            queryset = queryset.filter(user__username=u)
        else:
            queryset = queryset.filter(user=request.user)
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(user__username__icontains=q)
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddCommentView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(post=post, user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCommentView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthor, ]


class AddOrRemoveLike(APIView):

    def get(self, request, format=None, post_id=None):
        post = Post.objects.get(pk=post_id)
        user = self.request.user
        if user.is_authenticated:
            if user in post.likes.all():
                like = False
                post.likes.remove(user)
            else:
                like = True
                post.likes.add(user)

        context = {'like': like}
        return Response(context)


class GetLikers(APIView):

    def get(self, request, format=None, post_id=None):
        post = Post.objects.get(pk=post_id)
        likers = post.likes.values_list('username', flat=True)
        # print(likers)
        return Response(list(likers))





#TODO: Comment count, children and parent
#TODO: Hashtags



