from sqlalchemy import create_engine
from sqlalchemy_utils.functions import database_exists, create_database
from .book_data.books import books


def check_and_create_database(application, database):
    db_exists = database_exists('postgresql://@localhost/bookstore_rebuild')
    
    print(f"Does DB exist: {db_exists}")

    if not db_exists:
        the_database = create_engine('postgresql://@localhost/bookstore_rebuild')
        create_database(the_database.url)

        with application.app_context():
            from .models import User, Book, Cart, Order
            # database.init_app(application)
            database.create_all()
            database.session.commit()
            add_initial_book_data(Book, database)


def add_initial_book_data(Book, db):
    print('Creating initial book data.')
    for book in books:
        new_book = Book(
            isbn = book['isbn'],
            author = book['author'],
            title = book['title'],
            price = book['price'],
            stock_quantity = book['stock_quantity'],
            description = book['description'],
            category = book['category'],
            image_file = book['image_file'],
        )
        db.session.add(new_book)
        db.session.commit()