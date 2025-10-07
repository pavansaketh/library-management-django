from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q, Count, Avg
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta

from .models import Library, Book, Author, Category, Member, Borrowing, Review
from .serializers import (
    LibrarySerializer, BookSerializer, AuthorSerializer,
    CategorySerializer, MemberSerializer, BorrowingSerializer, ReviewSerializer
)

class LibraryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

class LibraryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.select_related('library').all()
    serializer_class = BookSerializer

class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.select_related('library').all()
    serializer_class = BookSerializer

class BookSearchAPIView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '').strip()
        books = Book.objects.all()

        if query:
            books = books.filter(
                Q(title__icontains=query) |
                Q(authors__first_name__icontains=query) |
                Q(authors__last_name__icontains=query) |
                Q(categories__name__icontains=query)
            ).distinct()

        # prefetch authors/categories to avoid N+1
        books = books.prefetch_related('authors', 'categories', 'library')
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class BookAvailabilityAPIView(APIView):
    def get(self, request, pk):
        book = get_object_or_404(Book.objects.select_related('library'), pk=pk)
        return Response({
            'book_id': book.id,
            'title': book.title,
            'is_available': book.is_available(),
            'available_copies': book.available_copies,
            'total_copies': book.total_copies
        })

class BorrowBookAPIView(APIView):
    def post(self, request):
        book_id = request.data.get('book_id')
        member_id = request.data.get('member_id')
        days = int(request.data.get('days', 14))

        if not book_id or not member_id:
            return Response({'error': 'book_id and member_id are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # use select_for_update in a transaction for concurrency-critical updates in production;
            # here we keep it simple
            book = Book.objects.get(id=book_id)
            member = Member.objects.get(id=member_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        except Member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)

        if not book.is_available():
            return Response({'error': 'Book not available'}, status=status.HTTP_400_BAD_REQUEST)

        # Create borrowing - set borrow_date and due_date explicitly (DB expects borrow_date)
        borrow_date = datetime.now().date()
        due_date = borrow_date + timedelta(days=days)

        borrowing = Borrowing.objects.create(
            book=book,
            member=member,
            borrow_date=borrow_date,
            due_date=due_date
        )

        # Update book availability
        # If you need concurrency safety, wrap this in a transaction + select_for_update
        book.available_copies = (book.available_copies or 0) - 1
        if book.available_copies < 0:
            # should not happen due to earlier check, but guard anyway
            book.available_copies = 0
        book.save(update_fields=['available_copies'])

        serializer = BorrowingSerializer(borrowing)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ReturnBookAPIView(APIView):
    def post(self, request):
        borrowing_id = request.data.get('borrowing_id')
        if not borrowing_id:
            return Response({'error': 'borrowing_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            borrowing = Borrowing.objects.get(id=borrowing_id)
        except Borrowing.DoesNotExist:
            return Response({'error': 'Borrowing not found'}, status=status.HTTP_404_NOT_FOUND)

        if borrowing.is_returned:
            return Response({'error': 'Book already returned'}, status=status.HTTP_400_BAD_REQUEST)

        # Update borrowing
        borrowing.return_date = datetime.now().date()
        borrowing.is_returned = True
        borrowing.save(update_fields=['return_date', 'is_returned'])

        # Update book availability
        book = borrowing.book
        book.available_copies = (book.available_copies or 0) + 1
        book.save(update_fields=['available_copies'])

        serializer = BorrowingSerializer(borrowing)
        return Response(serializer.data)

class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AuthorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MemberListCreateAPIView(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class MemberDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class MemberBorrowingsAPIView(APIView):
    def get(self, request, pk):
        member = get_object_or_404(Member, pk=pk)
        borrowings = member.borrowings.all().order_by('-borrow_date')
        serializer = BorrowingSerializer(borrowings, many=True)
        return Response(serializer.data)

class BorrowingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

class BorrowingDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class StatisticsAPIView(APIView):
    def get(self, request):
        stats = {
            'total_books': Book.objects.count(),
            'total_members': Member.objects.count(),
            'active_borrowings': Borrowing.objects.filter(return_date__isnull=True).count(),
            'total_libraries': Library.objects.count(),
            'average_rating': Review.objects.aggregate(Avg('rating'))['rating__avg'],
            'most_borrowed_books': list(
                Book.objects.annotate(
                    borrow_count=Count('borrowings')
                ).order_by('-borrow_count')[:5].values('title', 'borrow_count')
            )
        }
        return Response(stats)
