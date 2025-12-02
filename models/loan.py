# Здесь должна быть модель Loan согласно README.md

from datetime import datetime

class Loan:
    def __init__(self, book_id, reader_id, loan_date, return_date) -> None:
        
        if book_id <= 0:
            raise ValueError("ID книги должен быть положительным числом")
        if reader_id <= 0:
            raise ValueError("ID читателя должен быть положительным числом")
        if loan_date > return_date:
            raise ValueError("Дата возврата не может быть раньше даты выдачи")
        
        self.id = None
        self.book_id = book_id
        self.reader_id = reader_id
        self.loan_date = loan_date
        self.return_date = return_date
        self.is_returned = False

    def return_book(self) -> bool:
        """Отметить книгу как возвращенную"""
        if not self.is_returned:
            self.is_returned = True
            return True
        return False

    def is_overdue(self) -> bool:
        """Проверить просрочку"""
        if self.is_returned:
            return False
        return datetime.now().date() > self.return_date.date()

    def to_dict(self) -> dict:
        """Вернуть словарь с данными выдачи"""
        return {
            "id": self.id,
            "book_id": self.book_id,
            "reader_id": self.reader_id,
            "loan_date": self.loan_date,
            "return_date": self.return_date,
            "is_returned": self.is_returned
        }