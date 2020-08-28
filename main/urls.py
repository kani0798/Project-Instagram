from django.urls import path

from .views import AddCommentView, DeleteCommentView, AddOrRemoveLike, GetLikers, GetComments, GetHashtagsView

urlpatterns = [
    path('addcomments/<int:pk>/', AddCommentView.as_view(), name='add-comment'),
    path('deletecomments/<int:pk>/', DeleteCommentView.as_view(), name='delete-comment'),
    path('comments/<int:post_id>/', GetComments.as_view(), name='comments'),
    path('like/<int:post_id>/', AddOrRemoveLike.as_view(), name='like'),
    path('likers/<int:post_id>/', GetLikers.as_view(), name='likers'),
    path('hashtags/', GetHashtagsView.as_view(), name='hashtags'),
]