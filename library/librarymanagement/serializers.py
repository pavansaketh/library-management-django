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
    # nested read-only representations
    authors = AuthorSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    # writable PK lists to assign M2M relations
    author_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Author.objects.all(),
        source='authors', write_only=True, required=False
    )
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all(),
        source='categories', write_only=True, required=False
    )

    class Meta:
        model = Book
        fields = '__all__'

    def validate(self, data):
        # data may not contain both keys (partial updates) — use instance or default
        total = data.get('total_copies', getattr(self.instance, 'total_copies', 0))
        avail = data.get('available_copies', getattr(self.instance, 'available_copies', 0))
        if avail is not None and total is not None and avail > total:
            raise serializers.ValidationError("Available copies cannot exceed total copies")
        return data

    def create(self, validated_data):
        # handle authors/categories via source fields
        authors = validated_data.pop('authors', None)
        categories = validated_data.pop('categories', None)
        book = super().create(validated_data)
        if authors:
            book.authors.set(authors)
        if categories:
            book.categories.set(categories)
        return book

    def update(self, instance, validated_data):
        authors = validated_data.pop('authors', None)
        categories = validated_data.pop('categories', None)
        book = super().update(instance, validated_data)
        if authors is not None:
            book.authors.set(authors)
        if categories is not None:
            book.categories.set(categories)
        return book


class BookSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'available_copies']


class MemberSerializer(serializers.ModelSerializer):
    # provide a convenient 'name' property for compatibility with older code
    name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Member
        # include the computed name in the output
        fields = [
            'id', 'first_name', 'last_name', 'name',
            'email', 'phone', 'member_type',
            'registration_date', 'created_at', 'updated_at'
        ]

    def get_name(self, obj):
        # join first and last name, handle missing parts gracefully
        parts = [p for p in (obj.first_name, obj.last_name) if p]
        return " ".join(parts) if parts else None


class BorrowingSerializer(serializers.ModelSerializer):
    book_details = BookSimpleSerializer(source='book', read_only=True)
    member_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Borrowing
        fields = '__all__'

    def get_member_name(self, obj):
        if not obj or not obj.member:
            return None
        parts = [p for p in (obj.member.first_name, obj.member.last_name) if p]
        return " ".join(parts) if parts else None

    def validate(self, data):
        # For create operations where 'book' is present as object, validate availability
        book = data.get('book') or getattr(self.instance, 'book', None)
        is_returned = data.get('is_returned', getattr(self.instance, 'is_returned', False))
        # if we're creating/updating to a non-returned borrowing, ensure availability
        if book and not is_returned:
            if not book.is_available() and (not getattr(self.instance, 'is_returned', False)):
                raise serializers.ValidationError("Book is not available")
        return data


class ReviewSerializer(serializers.ModelSerializer):
    member_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def get_member_name(self, obj):
        if not obj or not obj.member:
            return None
        parts = [p for p in (obj.member.first_name, obj.member.last_name) if p]
        return " ".join(parts) if parts else None
