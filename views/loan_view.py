# Здесь должно быть представление для работы с займами согласно README.md

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class LoanView(ttk.Frame):
    def __init__(self, parent, loan_controller, book_controller, reader_controller) -> None:
        super().__init__(parent)
        self.loan_controller = loan_controller
        self.book_controller = book_controller
        self.reader_controller = reader_controller
        self.create_widgets()
        self.refresh_loans()

    def create_widgets(self) -> None:

        form_frame = ttk.LabelFrame(self, text="Создать выдачу", padding=10)
        form_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(form_frame, text="Книга:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.book_combo = ttk.Combobox(form_frame, width=40, state="readonly")
        self.book_combo.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Читатель:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.reader_combo = ttk.Combobox(form_frame, width=40, state="readonly")
        self.reader_combo.grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(form_frame, text="Дата выдачи:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.loan_date_entry = ttk.Entry(form_frame, width=20)
        self.loan_date_entry.grid(row=1, column=1, padx=5, pady=2)
        self.loan_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ttk.Label(form_frame, text="Дата возврата:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        self.return_date_entry = ttk.Entry(form_frame, width=20)
        self.return_date_entry.grid(row=1, column=3, padx=5, pady=2)
        self.return_date_entry.insert(0, (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"))

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)

        self.create_loan_button = ttk.Button(button_frame, text="Создать выдачу", command=self.create_loan)
        self.create_loan_button.pack(side=tk.LEFT, padx=5)

        self.return_button = ttk.Button(button_frame, text="Вернуть", command=self.return_selected)
        self.return_button.pack(side=tk.LEFT, padx=5)

        self.load_books()
        self.load_readers()

        filter_frame = ttk.Frame(self)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(filter_frame, text="Фильтр:").pack(side=tk.LEFT)
        
        self.filter_var = tk.StringVar(value="all")
        ttk.Radiobutton(filter_frame, text="Все", variable=self.filter_var, value="all", command=self.refresh_loans).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(filter_frame, text="Активные", variable=self.filter_var, value="active", command=self.refresh_loans).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(filter_frame, text="Просроченные", variable=self.filter_var, value="overdue", command=self.refresh_loans).pack(side=tk.LEFT, padx=5)

        columns = ("ID", "Книга", "Читатель", "Дата выдачи", "Дата возврата", "Возвращена")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)

    def load_books(self) -> None:
        """Загрузка книг в комбобокс"""
        try:
            books = self.book_controller.get_all_books()
            book_options = [(book.id, f"{book.title} ({book.author})") for book in books]
            self.book_options = book_options
            self.book_combo['values'] = [f"{title}" for _, title in book_options]
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить книги: {e}")

    def load_readers(self) -> None:
        """Загрузка читателей в комбобокс"""
        try:
            readers = self.reader_controller.get_all_readers()
            reader_options = [(reader.id, f"{reader.name} ({reader.email})") for reader in readers]
            self.reader_options = reader_options
            self.reader_combo['values'] = [f"{name}" for _, name in reader_options]
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить читателей: {e}")

    def refresh_loans(self) -> None:
        
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            if self.filter_var.get() == "overdue":
                loans = self.loan_controller.get_overdue_loans()
            else:
                loans = self.loan_controller.get_all_loans()

            for loan in loans:
                
                book = self.book_controller.get_book(loan.book_id)
                reader = self.reader_controller.get_reader(loan.reader_id)

                book_title = book.title if book else "Неизвестная книга"
                reader_name = reader.name if reader else "Неизвестный читатель"

                if self.filter_var.get() == "active" and loan.is_returned:
                    continue

                self.tree.insert("", "end", values=(
                    loan.id, book_title, reader_name,
                    loan.loan_date.strftime("%Y-%m-%d"),
                    loan.return_date.strftime("%Y-%m-%d"),
                    "Да" if loan.is_returned else "Нет"
                ))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить список выдач: {e}")

    def create_loan(self) -> None:
        try:

            if self.book_combo.current() < 0 or self.reader_combo.current() < 0:
                messagebox.showerror("Ошибка", "Выберите книгу и читателя")
                return

            book_id = self.book_options[self.book_combo.current()][0]
            reader_id = self.reader_options[self.reader_combo.current()][0]

            loan_date_str = self.loan_date_entry.get().strip()
            return_date_str = self.return_date_entry.get().strip()

            loan_date = datetime.strptime(loan_date_str, "%Y-%m-%d")
            return_date = datetime.strptime(return_date_str, "%Y-%m-%d")

            loan_id = self.loan_controller.create_loan(book_id, reader_id, loan_date, return_date)
            
            self.refresh_loans()
            messagebox.showinfo("Успех", "Выдача создана")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте формат ГГГГ-ММ-ДД")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать выдачу: {e}")

    def return_selected(self) -> None:
        try:
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showwarning("Предупреждение", "Выберите выдачу для возврата")
                return

            item = self.tree.item(selected_item)
            loan_id = item['values'][0]

            loan = self.loan_controller.get_loan(loan_id)
            if loan and loan.is_returned:
                messagebox.showwarning("Предупреждение", "Книга уже возвращена")
                return

            success = self.loan_controller.return_book(loan_id)
            if success:
                self.refresh_loans()
                messagebox.showinfo("Успех", "Книга возвращена")
            else:
                messagebox.showerror("Ошибка", "Не удалось вернуть книгу")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось вернуть книгу: {e}")
