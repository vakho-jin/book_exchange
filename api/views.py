from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Author, Genre, Condition, Book, BookRequest
from .serializers import (
    AuthorSerializer, GenreSerializer, ConditionSerializer,
    BookSerializer, BookRequestSerializer, UserSerializer
)
from .permissions import IsOwnerOrReadOnly, IsBookOwner
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ConditionViewSet(viewsets.ModelViewSet):
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'genre', 'year', 'condition', 'is_available']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class BookRequestViewSet(viewsets.ModelViewSet):
    queryset = BookRequest.objects.all()
    serializer_class = BookRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)

class SelectRecipientView(generics.UpdateAPIView):
    queryset = BookRequest.objects.all()
    serializer_class = BookRequestSerializer
    permission_classes = [IsBookOwner]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'APPROVED'
        instance.book.is_available = False
        instance.book.save()
        instance.save()
        BookRequest.objects.filter(book=instance.book, status='PENDING').exclude(id=instance.id).update(status='REJECTED')
        return Response(self.get_serializer(instance).data)