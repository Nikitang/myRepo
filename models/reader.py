# Здесь должна быть модель Reader согласно README.md

from datetime import datetime
import re

class Reader:
    def __init__(self, name, email, phone) -> None:
        
        if not name or not name.strip():
            raise ValueError("Имя читателя не может быть пустым")
        if not self._is_valid_email(email):
            raise ValueError("Некорректный email")
        
        self.id = None
        self.name = name
        self.email = email
        self.phone = phone
        self.registration_date = datetime.now()

    def _is_valid_email(self, email) -> bool:
        """Проверка корректности email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def update_info(self, name=None, email=None, phone=None) -> None:
        """Обновить информацию о читателе"""
        if name is not None:
            if not name or not name.strip():
                raise ValueError("Имя читателя не может быть пустым")
            self.name = name
        
        if email is not None:
            if not self._is_valid_email(email):
                raise ValueError("Некорректный email")
            self.email = email
        
        if phone is not None:
            self.phone = phone

    def to_dict(self) -> dict:
        """Вернуть словарь с данными читателя"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "registration_date": self.registration_date
        }