# api/serializers.py

from rest_framework import serializers
from .models import Library, Book, Author, Category, Member, Borrowing, Review

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    author_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Author.objects.all(), 
        source='authors', write_only=True
    )
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all(), 
        source='categories', write_only=True
    )
    
    class Meta:
        model = Book
        fields = '__all__'
    
    def validate(self, data):
        if data.get('available_copies', 0) > data.get('total_copies', 0):
            raise serializers.ValidationError(
                "Available copies cannot exceed total copies"
            )
        return data

class BookSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'available_copies']

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class BorrowingSerializer(serializers.ModelSerializer):
    book_details = BookSimpleSerializer(source='book', read_only=True)
    member_name = serializers.CharField(source='member.name', read_only=True)
    
    class Meta:
        model = Borrowing
        fields = '__all__'
    
    def validate(self, data):
        if not data.get('is_returned', False):
            book = data.get('book')
            if book and not book.is_available():
                raise serializers.ValidationError("Book is not available")
        return data

class ReviewSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.name', read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
