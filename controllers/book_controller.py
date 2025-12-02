# Здесь должен быть контроллер для работы с книгами согласно README.md

from models.book import Book

class BookController:
    def __init__(self, db_manager) -> None:
        pass

    def add_book(self, title, author, isbn, year, quantity) -> int:
        pass

    def get_book(self, book_id) -> Book | None:
        pass

    def get_all_books(self) -> list[Book]:
        pass

    def update_book(self, book_id, **kwargs) -> bool:
        pass

    def delete_book(self, book_id) -> bool:
        pass

    def search_books(self, query) -> list[Book]:
        pass

    def borrow_book(self, book_id) -> bool:
        pass

    def return_book(self, book_id) -> bool:
        pass

