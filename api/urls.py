from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthorViewSet, GenreViewSet, ConditionViewSet,
    BookViewSet, BookRequestViewSet, RegisterView, SelectRecipientView
)

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'conditions', ConditionViewSet)
router.register(r'books', BookViewSet)
router.register(r'requests', BookRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('requests/<int:pk>/select/', SelectRecipientView.as_view(), name='select-recipient'),
]