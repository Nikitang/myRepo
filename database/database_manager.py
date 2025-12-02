# Здесь должен быть менеджер базы данных согласно README.md

import sqlite3
from models.book import Book
from models.reader import Reader
from models.loan import Loan
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="library.db") -> None:
        pass

    def close(self) -> None:
        pass

    def create_tables(self) -> None:
        pass

    def add_book(self, book: Book) -> int:
        pass

    def get_book_by_id(self, book_id) -> Book | None:
        pass

    def get_all_books(self) -> list[Book]:
        pass

    def update_book(self, book_id, **kwargs) -> bool:
        pass

    def delete_book(self, book_id) -> bool:
        pass

    def search_books(self, query) -> list[Book]:
        pass

    def add_reader(self, reader: Reader) -> int:
        pass

    def get_reader_by_id(self, reader_id) -> Reader | None:
        pass

    def get_all_readers(self) -> list[Reader]:
        pass

    def update_reader(self, reader_id, **kwargs) -> bool:
        pass

    def delete_reader(self, reader_id) -> bool:
        pass

    def add_loan(self, loan: Loan) -> int:
        pass

    def get_loan_by_id(self, loan_id) -> Loan | None:
        pass

    def get_all_loans(self) -> list[Loan]:
        pass

    def update_loan(self, loan_id, **kwargs) -> bool:
        pass

    def get_reader_loans(self, reader_id) -> list[Loan]:
        pass

    def get_overdue_loans(self) -> list[Loan]:
        pass

