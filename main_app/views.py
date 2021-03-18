from datetime import timezone, timedelta

from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Category, Comment, Post, PostImages, Like, Rating
from .permissions import IsPostAuthor
from .serializers import CategorySerializer, PostImageSerializer, PostSerializer, CommentSerializer, LikeSerializer, \
    RatingSerializer


class MyPaginationClass(PageNumberPagination):
    page_size = 3

    def get_paginated_response(self, data):
        for i in range(self.page_size):
            text = data[i]['text']
            data[i]['text'] = text[:10] + "..."
        return super().get_paginated_response(data)


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ]


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = MyPaginationClass

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}

    def get_permissions(self):
        """ Переопределим данный меттод """
        print(self.action)
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsPostAuthor, ]
        else:
            permissions = [IsAuthenticated, ]
        return [permission() for permission in permissions]

    def get_queryset(self):
        queryset = super().get_queryset()
        days_count = self.request.query_params.get('day', 0)
        if days_count > 0:
            start_date = timezone.now() - timedelta(days=days_count)
            queryset = queryset.filter(created_at__gte=start_date)
        return queryset

    @action(detail=False, methods=['get'])
    def own(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) |
                                   Q(text__icontains=q))
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostImageView(generics.ListCreateAPIView):
    queryset = PostImages.objects.all()
    serializer_class = PostImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsPostAuthor]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


class LikeViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


class RatingViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}