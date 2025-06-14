from rest_framework import serializers
from .models import Author, Genre, Condition, Book, BookRequest
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    genre = GenreSerializer()
    condition = ConditionSerializer()
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

class BookRequestSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    requester = UserSerializer(read_only=True)

    class Meta:
        model = BookRequest
        fields = '__all__'