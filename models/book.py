# Здесь должна быть модель Book согласно README.md

from datetime import datetime

class Book:
    def __init__(self, title, author, isbn, year, quantity) -> None:

        if not title or not title.strip():
            raise ValueError("Название книги не может быть пустым")
        if year < 0:
            raise ValueError("Год издания не может быть отрицательным")
        if quantity < 0:
            raise ValueError("Количество экземпляров не может быть отрицательным")
        
        self.id = None
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.quantity = quantity
        self.available = quantity

    def borrow_book(self) -> bool:
        """Выдать книгу (уменьшить available)"""
        if self.available > 0:
            self.available -= 1
            return True
        return False

    def return_book(self) -> bool:
        """Вернуть книгу (увеличить available)"""
        if self.available < self.quantity:
            self.available += 1
            return True
        return False

    def is_available(self) -> bool:
        """Проверить доступность"""
        return self.available > 0

    def to_dict(self) -> dict:
        """Вернуть словарь с данными книги"""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "year": self.year,
            "quantity": self.quantity,
            "available": self.available
        }
