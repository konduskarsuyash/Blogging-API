from django.urls import path
from .views import PostAPIView,CommentAPIView,CommentDeleteAPIView

urlpatterns = [
    path('posts/', PostAPIView.as_view(), name='post-list'),  # Handles GET and POST (list and create)
    path('posts/<int:id>/', PostAPIView.as_view(), name='post-detail'),  # Handles GET, PUT, and DELETE (single post)
    path('posts/<int:post_id>/comments/', CommentAPIView.as_view(), name='comment-list-create'),  # POST and GET
    path('comments/<int:id>/', CommentDeleteAPIView.as_view(), name='comment-delete'),  # DELETE
]
