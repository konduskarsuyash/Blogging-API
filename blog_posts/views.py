from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from .models import Post,Comment
from .serializers import PostSerializer,CommentSerializer,CommentGetSerializer

class PostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        # If `id` is provided, fetch the specific post; otherwise, fetch all posts.
        if id:
            try:
                post = Post.objects.get(id=id)
                serializer = PostSerializer(post)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Post.DoesNotExist:
                return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Create a new post with the logged-in user as the author
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            post = serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        # Update an existing post
        if not id:
            return Response({"message": "Post ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the logged-in user is the author of the post
        if post.author != request.user:
            raise PermissionDenied("You do not have permission to update this post.")

        serializer = PostSerializer(post, data=request.data, partial=True)  # partial=True allows updating only some fields
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        # Delete a post
        if not id:
            return Response({"message": "Post ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the logged-in user is the author of the post
        if post.author != request.user:
            raise PermissionDenied("You do not have permission to delete this post.")

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id=None):
        # Add a comment to a specific post
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create the comment for the post
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Setting author and post manually
            comment = serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, post_id=None):
        # Get all comments for a specific post
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        comments = post.comments.all()
        serializer = CommentGetSerializer(comments, many=True)  # Use the new serializer for GET
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id=None):
        # Delete a specific comment
        try:
            comment = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return Response({"message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the logged-in user is the author of the comment
        if comment.author != request.user:
            raise PermissionDenied("You do not have permission to delete this comment.")

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)