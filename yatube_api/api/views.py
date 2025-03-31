from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import NotAuthenticated

from .serializers import (
    PostSerializer, FollowSerializer,
    CommentSerializer, GroupSerializer
)
from .permissions import IsOwnerOrReadOnly
from posts.models import Post, Follow, Group, Comment


class BaseViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        is_auth = request.user.is_authenticated
        if not is_auth and self.action not in ['list', 'retrieve']:
            raise NotAuthenticated({"detail": "Требуется авторизация"})


class PostViewSet(BaseViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    search_fields = ['text', 'author__username']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(BaseViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(BaseViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    http_method_names = ['get', 'head', 'options']


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['following__username']
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        """
        Возвращает подписки только текущего пользователя
        Для неавторизованных - пустой queryset и 401 статус
        """
        return Follow.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        """
        Обработка GET /follow/
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Обработка POST /follow/
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        """Сохранение подписки с текущим пользователем"""
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        Обработка DELETE /follow/{id}/
        """
        follow = get_object_or_404(
            Follow,
            user=request.user,
            following_id=kwargs['pk']
        )
        self.perform_destroy(follow)
        return Response(status=status.HTTP_204_NO_CONTENT)
