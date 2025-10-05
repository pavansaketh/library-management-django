create database db;
show databases;
use db;
-- 1) Library
CREATE TABLE Library (
    library_id     INT AUTO_INCREMENT PRIMARY KEY,
    name           VARCHAR(100) NOT NULL,
    campus_location VARCHAR(100),
    contact_email  VARCHAR(100),
    phone_number   VARCHAR(20),
    created_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT uq_library_name UNIQUE (name)
);

INSERT INTO Library (name, campus_location, contact_email, phone_number)
VALUES
('Central Library', 'Main Campus', 'central@univ.edu', '1234567890'),
('Science Library', 'Science Campus', 'science@univ.edu', '2345678901'),
('Arts Library', 'Arts Campus', 'arts@univ.edu', '3456789012');

-- 2) Book  (FK -> Library)
CREATE TABLE Book (
    book_id           INT AUTO_INCREMENT PRIMARY KEY,
    title             VARCHAR(200) NOT NULL,
    isbn              VARCHAR(20) UNIQUE,
    publication_date  DATE,
    total_copies      INT DEFAULT 0,
    available_copies  INT DEFAULT 0,
    library_id        INT,
    created_at        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_book_library
        FOREIGN KEY (library_id) REFERENCES Library(library_id),
    CONSTRAINT chk_book_copies CHECK (available_copies <= total_copies)
);

INSERT INTO Book (title, isbn, publication_date, total_copies, available_copies, library_id)
VALUES
('1984', 'ISBN001', '1949-06-08', 10, 8, 1),
('Animal Farm', 'ISBN002', '1945-08-17', 8, 7, 1),
('Pride and Prejudice', 'ISBN003', '1813-01-28', 12, 10, 1),
('Adventures of Huckleberry Finn', 'ISBN004', '1884-12-10', 6, 5, 1),
('Harry Potter and the Sorcerer''s Stone', 'ISBN005', '1997-06-26', 20, 18, 2),
('Harry Potter and the Chamber of Secrets', 'ISBN006', '1998-07-02', 18, 17, 2),
('To Kill a Mockingbird', 'ISBN007', '1960-07-11', 15, 14, 2),
('The Great Gatsby', 'ISBN008', '1925-04-10', 10, 9, 2),
('War and Peace', 'ISBN009', '1869-01-01', 5, 4, 3),
('Anna Karenina', 'ISBN010', '1877-01-01', 7, 6, 3),
('Murder on the Orient Express', 'ISBN011', '1934-01-01', 9, 8, 3),
('The Hobbit', 'ISBN012', '1937-09-21', 14, 13, 1),
('A Brief History of Time', 'ISBN013', '1988-03-01', 10, 10, 2),
('The Selfish Gene', 'ISBN014', '1976-01-01', 6, 6, 2),
('Sapiens: A Brief History of Humankind', 'ISBN015', '2011-01-01', 8, 8, 3);

-- 3) Author
CREATE TABLE Author (
    author_id    INT AUTO_INCREMENT PRIMARY KEY,
    first_name   VARCHAR(100) NOT NULL,
    last_name    VARCHAR(100) NOT NULL,
    birth_date   DATE,
    nationality  VARCHAR(100),
    biography    TEXT,
    created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT uq_author_natural UNIQUE (first_name, last_name, birth_date)
);

INSERT INTO Author (first_name, last_name, birth_date, nationality, biography)
VALUES
('George', 'Orwell', '1903-06-25', 'British', 'Author of 1984 and Animal Farm'),
('Jane', 'Austen', '1775-12-16', 'British', 'Author of Pride and Prejudice'),
('Mark', 'Twain', '1835-11-30', 'American', 'Author of Adventures of Huckleberry Finn'),
('J.K.', 'Rowling', '1965-07-31', 'British', 'Author of Harry Potter series'),
('Harper', 'Lee', '1926-04-28', 'American', 'Author of To Kill a Mockingbird'),
('F. Scott', 'Fitzgerald', '1896-09-24', 'American', 'Author of The Great Gatsby'),
('Leo', 'Tolstoy', '1828-09-09', 'Russian', 'Author of War and Peace'),
('Agatha', 'Christie', '1890-09-15', 'British', 'Mystery novelist');

-- 4) Category
CREATE TABLE Category (
    category_id  INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    description  TEXT,
    created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT uq_category_name UNIQUE (name)
);

INSERT INTO Category (name, description)
VALUES
('Fiction', 'General fiction books'),
('Science', 'Scientific research and textbooks'),
('History', 'Historical accounts and biographies'),
('Mystery', 'Detective and crime novels'),
('Fantasy', 'Fantasy and magical worlds');

-- 5) Member
CREATE TABLE Member (
    member_id         INT AUTO_INCREMENT PRIMARY KEY,
    first_name        VARCHAR(100) NOT NULL,
    last_name         VARCHAR(100) NOT NULL,
    email             VARCHAR(100) UNIQUE,
    phone             VARCHAR(20),
    member_type       ENUM('student','faculty') NOT NULL,
    registration_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    created_at        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO Member (first_name, last_name, email, phone, member_type)
VALUES
('Alice', 'Smith', 'alice@univ.edu', '1111111111', 'student'),
('Bob', 'Johnson', 'bob@univ.edu', '1111111112', 'faculty'),
('Charlie', 'Williams', 'charlie@univ.edu', '1111111113', 'student'),
('David', 'Brown', 'david@univ.edu', '1111111114', 'student'),
('Eve', 'Jones', 'eve@univ.edu', '1111111115', 'faculty'),
('Frank', 'Garcia', 'frank@univ.edu', '1111111116', 'student'),
('Grace', 'Miller', 'grace@univ.edu', '1111111117', 'student'),
('Hank', 'Davis', 'hank@univ.edu', '1111111118', 'faculty'),
('Ivy', 'Martinez', 'ivy@univ.edu', '1111111119', 'student'),
('Jack', 'Lopez', 'jack@univ.edu', '1111111120', 'student'),
('Karen', 'Wilson', 'karen@univ.edu', '1111111121', 'faculty'),
('Leo', 'Anderson', 'leo@univ.edu', '1111111122', 'student'),
('Mia', 'Thomas', 'mia@univ.edu', '1111111123', 'student'),
('Nina', 'Taylor', 'nina@univ.edu', '1111111124', 'faculty'),
('Oscar', 'Moore', 'oscar@univ.edu', '1111111125', 'student'),
('Pam', 'Jackson', 'pam@univ.edu', '1111111126', 'student'),
('Quinn', 'Martin', 'quinn@univ.edu', '1111111127', 'student'),
('Rita', 'Lee', 'rita@univ.edu', '1111111128', 'faculty'),
('Sam', 'Perez', 'sam@univ.edu', '1111111129', 'student'),
('Tina', 'White', 'tina@univ.edu', '1111111130', 'student');

-- 6) Borrowing  (FK -> Member, Book)
CREATE TABLE Borrowing (
    borrowing_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id    INT NOT NULL,
    book_id      INT NOT NULL,
    borrow_date  DATE NOT NULL,
    due_date     DATE NOT NULL,
    return_date  DATE,
    late_fee     DECIMAL(6,2) NOT NULL DEFAULT 0,
    created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_borrowing_member FOREIGN KEY (member_id) REFERENCES Member(member_id),
    CONSTRAINT fk_borrowing_book   FOREIGN KEY (book_id)   REFERENCES Book(book_id),
    CONSTRAINT chk_borrowing_dates CHECK (due_date >= borrow_date),
    CONSTRAINT chk_return_after_borrow CHECK (return_date IS NULL OR return_date >= borrow_date),
    CONSTRAINT chk_late_fee_nonneg CHECK (late_fee >= 0)
);

INSERT INTO Borrowing (member_id, book_id, borrow_date, due_date, return_date, late_fee)
VALUES
(1,1,'2025-01-01','2025-01-15','2025-01-14',0),
(2,2,'2025-01-05','2025-01-19','2025-01-25',5.00),
(3,3,'2025-01-10','2025-01-24','2025-01-20',0),
(4,4,'2025-01-11','2025-01-25',NULL,0),
(5,5,'2025-01-12','2025-01-26','2025-01-28',3.00),
(6,6,'2025-01-13','2025-01-27','2025-01-27',0),
(7,7,'2025-01-14','2025-01-28',NULL,0),
(8,8,'2025-01-15','2025-01-29','2025-01-29',0),
(9,9,'2025-01-16','2025-01-30',NULL,0),
(10,10,'2025-01-17','2025-01-31','2025-02-02',2.00),
(11,11,'2025-01-18','2025-02-01','2025-01-30',0),
(12,12,'2025-01-19','2025-02-02','2025-02-01',0),
(13,13,'2025-01-20','2025-02-03','2025-02-05',4.00),
(14,14,'2025-01-21','2025-02-04','2025-02-04',0),
(15,15,'2025-01-22','2025-02-05',NULL,0),
(16,1,'2025-01-23','2025-02-06','2025-02-06',0),
(17,2,'2025-01-24','2025-02-07','2025-02-09',3.00),
(18,3,'2025-01-25','2025-02-08','2025-02-07',0),
(19,4,'2025-01-26','2025-02-09','2025-02-10',2.00),
(20,5,'2025-01-27','2025-02-10','2025-02-15',5.00),
(1,6,'2025-01-28','2025-02-11',NULL,0),
(2,7,'2025-01-29','2025-02-12','2025-02-13',0),
(3,8,'2025-01-30','2025-02-13','2025-02-14',0),
(4,9,'2025-01-31','2025-02-14','2025-02-16',3.00),
(5,10,'2025-02-01','2025-02-15',NULL,0);

-- 7) Review  (FK -> Member, Book)
CREATE TABLE Review (
    review_id   INT AUTO_INCREMENT PRIMARY KEY,
    member_id   INT NOT NULL,
    book_id     INT NOT NULL,
    rating      TINYINT NOT NULL,
    comment     TEXT,
    review_date DATE NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_review_member FOREIGN KEY (member_id) REFERENCES Member(member_id),
    CONSTRAINT fk_review_book   FOREIGN KEY (book_id)   REFERENCES Book(book_id),
    CONSTRAINT chk_rating_1_5   CHECK (rating BETWEEN 1 AND 5)
);

INSERT INTO Review (member_id, book_id, rating, comment, review_date)
VALUES
(1,1,5,'Excellent read','2025-02-01'),
(2,2,4,'Very insightful','2025-02-02'),
(3,3,5,'Classic masterpiece','2025-02-03'),
(4,4,3,'Good but lengthy','2025-02-04'),
(5,5,5,'Amazing fantasy world','2025-02-05'),
(6,6,4,'Loved it','2025-02-06'),
(7,7,5,'Highly recommended','2025-02-07'),
(8,8,4,'Well written','2025-02-08'),
(9,9,5,'Epic story','2025-02-09'),
(10,10,3,'Hard to follow','2025-02-10'),
(11,11,4,'Great mystery','2025-02-11'),
(12,12,5,'One of my favorites','2025-02-12');

-- 8) BookAuthor (junction)
CREATE TABLE BookAuthor (
    book_id    INT NOT NULL,
    author_id  INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (book_id, author_id),
    CONSTRAINT fk_ba_book   FOREIGN KEY (book_id)   REFERENCES Book(book_id),
    CONSTRAINT fk_ba_author FOREIGN KEY (author_id) REFERENCES Author(author_id)
);

INSERT INTO BookAuthor (book_id, author_id)
VALUES
(1,1), (2,1),
(3,2),
(4,3),
(5,4), (6,4),
(7,5),
(8,6),
(9,7), (10,7),
(11,8),
(12,4),
(13,7),
(14,7),
(15,7);

-- 9) BookCategory (junction)
CREATE TABLE BookCategory (
    book_id     INT NOT NULL,
    category_id INT NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (book_id, category_id),
    CONSTRAINT fk_bc_book     FOREIGN KEY (book_id)     REFERENCES Book(book_id),
    CONSTRAINT fk_bc_category FOREIGN KEY (category_id) REFERENCES Category(category_id)
);

INSERT INTO BookCategory (book_id, category_id)
VALUES
(1,1), (2,1),
(3,1),
(4,1),
(5,5), (6,5),
(7,1),
(8,1),
(9,3), (10,3),
(11,4),
(12,5),
(13,2),
(14,2),
(15,3);


