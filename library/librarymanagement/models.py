from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
from django.db import models

class Library(models.Model):
    id = models.AutoField(primary_key=True, db_column='library_id')   # use .id in code
    name = models.CharField(max_length=100, db_column='name')
    campus_location = models.CharField(max_length=100, null=True, db_column='campus_location')
    contact_email = models.CharField(max_length=100, null=True, db_column='contact_email')
    phone_number = models.CharField(max_length=20, null=True, db_column='phone_number')
    created_at = models.DateTimeField(null=True, db_column='created_at')
    updated_at = models.DateTimeField(null=True, db_column='updated_at')

    class Meta:
        db_table = 'Library'
        managed = False
        verbose_name_plural = "Libraries"

    def __str__(self):
        return self.name

class Author(models.Model):
    id = models.AutoField(primary_key=True, db_column='author_id')
    first_name = models.CharField(max_length=100, db_column='first_name')
    last_name = models.CharField(max_length=100, db_column='last_name')
    birth_date = models.DateField(null=True, db_column='birth_date')
    nationality = models.CharField(max_length=100, null=True, db_column='nationality')
    biography = models.TextField(null=True, db_column='biography')
    created_at = models.DateTimeField(null=True, db_column='created_at')
    updated_at = models.DateTimeField(null=True, db_column='updated_at')

    class Meta:
        db_table = 'Author'
        managed = False

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Category(models.Model):
    id = models.AutoField(primary_key=True, db_column='category_id')
    name = models.CharField(max_length=100, db_column='name')
    description = models.TextField(null=True, db_column='description')
    created_at = models.DateTimeField(null=True, db_column='created_at')
    updated_at = models.DateTimeField(null=True, db_column='updated_at')

    class Meta:
        db_table = 'Category'
        managed = False
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Book(models.Model):
    id = models.AutoField(primary_key=True, db_column='book_id')
    title = models.CharField(max_length=200, db_column='title')
    isbn = models.CharField(max_length=20, unique=True, null=True, db_column='isbn')
    publication_date = models.DateField(null=True, db_column='publication_date')
    total_copies = models.IntegerField(default=0, db_column='total_copies')
    available_copies = models.IntegerField(default=0, db_column='available_copies')
    library = models.ForeignKey(
        Library, db_column='library_id', null=True,
        on_delete=models.DO_NOTHING, related_name='books'
    )
    created_at = models.DateTimeField(null=True, db_column='created_at')
    updated_at = models.DateTimeField(null=True, db_column='updated_at')

    authors = models.ManyToManyField(Author, through='BookAuthor', related_name='books')
    categories = models.ManyToManyField(Category, through='BookCategory', related_name='books')

    class Meta:
        db_table = 'Book'
        managed = False

    def __str__(self):
        return self.title

    def is_available(self):
        return (self.available_copies or 0) > 0

class Member(models.Model):
    id = models.AutoField(primary_key=True, db_column='member_id')
    first_name = models.CharField(max_length=100, db_column='first_name')
    last_name = models.CharField(max_length=100, db_column='last_name')
    email = models.CharField(max_length=100, null=True, db_column='email')
    phone = models.CharField(max_length=20, null=True, db_column='phone')
    MEMBER_TYPE_CHOICES = (('student', 'student'), ('faculty', 'faculty'))
    member_type = models.CharField(max_length=10, choices=MEMBER_TYPE_CHOICES, db_column='member_type')
    registration_date = models.DateField(null=True, db_column='registration_date')
    created_at = models.DateTimeField(null=True, db_column='created_at')
    updated_at = models.DateTimeField(null=True, db_column='updated_at')

    class Meta:
        db_table = 'Member'
        managed = False

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Borrowing(models.Model):
    id = models.AutoField(primary_key=True, db_column='borrowing_id')
    member = models.ForeignKey(Member, db_column='member_id', on_delete=models.DO_NOTHING, related_name='borrowings')
    book = models.ForeignKey(Book, db_column='book_id', on_delete=models.DO_NOTHING, related_name='borrowings')
    borrow_date = models.DateField(null=True, db_column='borrow_date')
    due_date = models.DateField(null=True, db_column='due_date')
    return_date = models.DateField(null=True, db_column='return_date')
    late_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0, db_column='late_fee')
    created_at = models.DateTimeField(null=True, db_column='created_at')
    updated_at = models.DateTimeField(null=True, db_column='updated_at')

    class Meta:
        db_table = 'Borrowing'
        managed = False

    def __str__(self):
        return f"{self.member} borrowed {self.book}"

class Review(models.Model):
    id = models.AutoField(primary_key=True, db_column='review_id')
    member = models.ForeignKey(Member, db_column='member_id', on_delete=models.DO_NOTHING, related_name='reviews')
    book = models.ForeignKey(Book, db_column='book_id', on_delete=models.DO_NOTHING, related_name='reviews')
    rating = models.PositiveSmallIntegerField(db_column='rating')
    comment = models.TextField(null=True, db_column='comment')
    review_date = models.DateField(null=True, db_column='review_date')
    created_at = models.DateTimeField(null=True, db_column='created_at')
    updated_at = models.DateTimeField(null=True, db_column='updated_at')

    class Meta:
        db_table = 'Review'
        managed = False
        unique_together = (('book', 'member'),)

    def __str__(self):
        return f"{self.book} - {self.rating} stars"

class BookAuthor(models.Model):
    book = models.ForeignKey(Book, db_column='book_id', on_delete=models.DO_NOTHING)
    author = models.ForeignKey(Author, db_column='author_id', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(null=True, db_column='created_at')
    updated_at = models.DateTimeField(null=True, db_column='updated_at')

    class Meta:
        db_table = 'BookAuthor'
        managed = False
        unique_together = (('book', 'author'),)

class BookCategory(models.Model):
    book = models.ForeignKey(Book, db_column='book_id', on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, db_column='category_id', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(null=True, db_column='created_at')
    updated_at = models.DateTimeField(null=True, db_column='updated_at')

    class Meta:
        db_table = 'BookCategory'
        managed = False
        unique_together = (('book', 'category'),)

