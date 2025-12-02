# Здесь должен быть контроллер для работы с займами согласно README.md

from models.loan import Loan
from datetime import datetime

class LoanController:
    def __init__(self, db_manager) -> None:
        pass

    def create_loan(self, book_id, reader_id, loan_date, return_date) -> int:
        pass

    def get_loan(self, loan_id) -> Loan | None:
        pass

    def get_all_loans(self) -> list[Loan]:
        pass

    def return_book(self, loan_id) -> bool:
        pass

    def get_overdue_loans(self) -> list[Loan]:
        pass

    def get_reader_loans(self, reader_id) -> list[Loan]:
        pass

