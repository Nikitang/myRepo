# Главное окно приложения согласно README.md

import tkinter as tk
from tkinter import ttk
from views.book_view import BookView
from views.reader_view import ReaderView
from views.loan_view import LoanView

class MainWindow(tk.Tk):
    def __init__(self, book_controller, reader_controller, loan_controller) -> None:
        super().__init__()
        self.title("Система управления библиотекой")
        self.geometry("800x600")
        
        # Создаем контроллеры
        self.book_controller = book_controller
        self.reader_controller = reader_controller
        self.loan_controller = loan_controller
        
        # Создаем вкладки
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создаем вкладки для книг, читателей и выдач
        self.book_view = BookView(self.notebook, self.book_controller)
        self.reader_view = ReaderView(self.notebook, self.reader_controller)
        self.loan_view = LoanView(self.notebook, self.loan_controller, self.book_controller, self.reader_controller)
        
        # Добавляем вкладки
        self.notebook.add(self.book_view, text="Книги")
        self.notebook.add(self.reader_view, text="Читатели")
        self.notebook.add(self.loan_view, text="Выдачи")