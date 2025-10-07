Library Management System (Django REST API)

A complete backend API for managing libraries, books, authors, categories, members, borrowings, and reviews — built using Django and Django REST Framework

CRUD APIs for:
  - Libraries
  - Books
  - Authors
  - Categories
  - Members
  - Borrowings
  - Reviews
- Book borrowing & returning workflow
- Availability tracking for books
- Member borrowing history
- Search API (by book title, author, or category)
- Statistics API (library insights)
- Swagger API documentation
- MySQL database integration

Backend Framework: Django REST Framework  
Database: MySQL  
Documentation: Swagger 
Language: Python

Clone the repository:
```bash
git clone https://github.com/library-management-django.git
cd library-management-django

activate the virtual environment:
   - venv\Scripts\activate

install the dependencies:
  - pip install -r requirements.txt
  dependencies:
    - Django==4.2.7
    - djangorestframework==3.14.0
    - psycopg2-binary==2.9.9
    - drf-yasg==1.21.7
    - python-dotenv==1.0.0
    - rest_framework

- create the database in the mysql and add the mysql in the settings.py file

Run the migrations:
  - python manage.py makemigrations
  - python manage.py migrate

Start the server:
  - python manage.py runserver

APIs
/admin/                                  → Django admin dashboard
/swagger/                                → Swagger UI API docs
/redoc/                                  → ReDoc API docs
/api/libraries/                          → List & create libraries
/api/libraries/<id>/                     → Retrieve, update, delete a library
/api/books/                              → List & create books
/api/books/<id>/                         → Retrieve, update, delete a book
/api/books/search/?q=<keyword>           → Search books by title, author, or category
/api/books/<id>/availability/            → Check if a book is available
/api/books/borrow/                       → Borrow a book
/api/books/return/                       → Return a borrowed book
/api/authors/                            → List & create authors
/api/authors/<id>/                       → Retrieve, update, delete an author
/api/categories/                         → List & create categories
/api/categories/<id>/                    → Retrieve, update, delete a category
/api/members/                            → List & create members
/api/members/<id>/                       → Retrieve, update, delete a member
/api/members/<id>/borrowings/            → View member’s borrowing history
/api/borrowings/                         → List & create borrowings
/api/borrowings/<id>/                    → Retrieve, update, delete a borrowing
/api/reviews/                            → List & create reviews
/api/reviews/<id>/                       → Retrieve, update, delete a review
/api/statistics/                         → Get library statistics (books, members, borrowings, ratings)


