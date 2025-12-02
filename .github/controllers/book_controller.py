# Здесь должен быть контроллер для работы с книгами согласно README.md

from models.book import Book

class BookController:
    def __init__(self, db_manager) -> None:
        self.db_manager = db_manager

    def add_book(self, title, author, isbn, year, quantity) -> int:
        book = Book(title, author, isbn, year, quantity)
        return self.db_manager.add_book(book)

    def get_book(self, book_id) -> Book | None:
        return self.db_manager.get_book_by_id(book_id)

    def get_all_books(self) -> list[Book]:
        return self.db_manager.get_all_books()

    def update_book(self, book_id, **kwargs) -> bool:
        return self.db_manager.update_book(book_id, **kwargs)

    def delete_book(self, book_id) -> bool:
        return self.db_manager.delete_book(book_id)

    def search_books(self, query) -> list[Book]:
        return self.db_manager.search_books(query)

    def borrow_book(self, book_id) -> bool:
        book = self.db_manager.get_book_by_id(book_id)
        if book and book.borrow_book():
            
            success = self.db_manager.update_book(book_id, available=book.available)
            return success
        return False

    def return_book(self, book_id) -> bool:
        book = self.db_manager.get_book_by_id(book_id)
        if book and book.return_book():
            
            success = self.db_manager.update_book(book_id, available=book.available)
            return success
        return False

