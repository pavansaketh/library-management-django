# library_management/urls.py

from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from librarymanagement import views

# Swagger Documentation
schema_view = get_schema_view(
   openapi.Info(
      title="My API",
      default_version='v1',
      description="API documentation",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Swagger Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Libraries
    path('api/libraries/', views.LibraryListCreateAPIView.as_view(), name='library-list-create'),
    path('api/libraries/<int:pk>/', views.LibraryDetailAPIView.as_view(), name='library-detail'),
    
    # Books
    path('api/books/', views.BookListCreateAPIView.as_view(), name='book-list-create'),
    path('api/books/<int:pk>/', views.BookDetailAPIView.as_view(), name='book-detail'),
    path('api/books/search/', views.BookSearchAPIView.as_view(), name='book-search'),
    path('api/books/<int:pk>/availability/', views.BookAvailabilityAPIView.as_view(), name='book-availability'),
    path('api/books/borrow/', views.BorrowBookAPIView.as_view(), name='book-borrow'),
    path('api/books/return/', views.ReturnBookAPIView.as_view(), name='book-return'),
    
    # Authors
    path('api/authors/', views.AuthorListCreateAPIView.as_view(), name='author-list-create'),
    path('api/authors/<int:pk>/', views.AuthorDetailAPIView.as_view(), name='author-detail'),
    
    # Categories
    path('api/categories/', views.CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('api/categories/<int:pk>/', views.CategoryDetailAPIView.as_view(), name='category-detail'),
    
    # Members
    path('api/members/', views.MemberListCreateAPIView.as_view(), name='member-list-create'),
    path('api/members/<int:pk>/', views.MemberDetailAPIView.as_view(), name='member-detail'),
    path('api/members/<int:pk>/borrowings/', views.MemberBorrowingsAPIView.as_view(), name='member-borrowings'),
    
    # Borrowings
    path('api/borrowings/', views.BorrowingListCreateAPIView.as_view(), name='borrowing-list-create'),
    path('api/borrowings/<int:pk>/', views.BorrowingDetailAPIView.as_view(), name='borrowing-detail'),
    
    # Reviews
    path('api/reviews/', views.ReviewListCreateAPIView.as_view(), name='review-list-create'),
    path('api/reviews/<int:pk>/', views.ReviewDetailAPIView.as_view(), name='review-detail'),
    
    # Statistics
    path('api/statistics/', views.StatisticsAPIView.as_view(), name='statistics'),
]