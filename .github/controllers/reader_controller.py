# Здесь должен быть контроллер для работы с читателями согласно README.md

from models.reader import Reader

class ReaderController:
    def __init__(self, db_manager) -> None:
        self.db_manager = db_manager

    def add_reader(self, name, email, phone) -> int:
        reader = Reader(name, email, phone)
        return self.db_manager.add_reader(reader)

    def get_reader(self, reader_id) -> Reader | None:
        return self.db_manager.get_reader_by_id(reader_id)

    def get_all_readers(self) -> list[Reader]:
        return self.db_manager.get_all_readers()

    def update_reader(self, reader_id, **kwargs) -> bool:
        return self.db_manager.update_reader(reader_id, **kwargs)

    def delete_reader(self, reader_id) -> bool:
        return self.db_manager.delete_reader(reader_id)

    def get_reader_loans(self, reader_id) -> list:
        return self.db_manager.get_reader_loans(reader_id)