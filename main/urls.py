from django.urls import path

from .views import AddCommentView, DeleteCommentView, AddOrRemoveLike, GetLikers

urlpatterns = [
    path('addcomment/<int:pk>/', AddCommentView.as_view(), name='add-comment'),
    path('deletecomment/<int:pk>/', DeleteCommentView.as_view(), name='delete-comment'),
    path('like/<int:post_id>/', AddOrRemoveLike.as_view(), name='like'),
    path('likers/<int:post_id>/', GetLikers.as_view(), name='likers'),
]