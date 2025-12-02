# Здесь должен быть контроллер для работы с займами согласно README.md

from models.loan import Loan
from datetime import datetime

class LoanController:
    def __init__(self, db_manager) -> None:
        self.db_manager = db_manager

    def create_loan(self, book_id, reader_id, loan_date, return_date) -> int:
        loan = Loan(book_id, reader_id, loan_date, return_date)
        return self.db_manager.add_loan(loan)

    def get_loan(self, loan_id) -> Loan | None:
        return self.db_manager.get_loan_by_id(loan_id)

    def get_all_loans(self) -> list[Loan]:
        return self.db_manager.get_all_loans()

    def return_book(self, loan_id) -> bool:
        loan = self.db_manager.get_loan_by_id(loan_id)
        if loan and loan.return_book():
            # Обновляем статус возврата в базе данных
            success = self.db_manager.update_loan(loan_id, is_returned=loan.is_returned)
            return success
        return False

    def get_overdue_loans(self) -> list[Loan]:
        return self.db_manager.get_overdue_loans()

    def get_reader_loans(self, reader_id) -> list[Loan]:
        return self.db_manager.get_reader_loans(reader_id)