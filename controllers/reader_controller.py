# Здесь должен быть контроллер для работы с читателями согласно README.md

from models.reader import Reader

class ReaderController:
    def __init__(self, db_manager) -> None:
        pass

    def add_reader(self, name, email, phone) -> int:
        pass

    def get_reader(self, reader_id) -> Reader | None:
        pass

    def get_all_readers(self) -> list[Reader]:
        pass

    def update_reader(self, reader_id, **kwargs) -> bool:
        pass

    def delete_reader(self, reader_id) -> bool:
        pass

    def get_reader_loans(self, reader_id) -> list:
        pass

