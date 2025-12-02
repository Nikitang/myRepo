# Здесь должно быть представление для работы с книгами согласно README.md

import tkinter as tk
from tkinter import ttk, messagebox

class BookView(ttk.Frame):
    def __init__(self, parent, book_controller) -> None:
        super().__init__(parent)
        self.book_controller = book_controller
        self.create_widgets()
        self.refresh_books()

    def create_widgets(self) -> None:
        
        form_frame = ttk.LabelFrame(self, text="Добавить/редактировать книгу", padding=10)
        form_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(form_frame, text="Название:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.title_entry = ttk.Entry(form_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Автор:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.author_entry = ttk.Entry(form_frame, width=30)
        self.author_entry.grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(form_frame, text="ISBN:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.isbn_entry = ttk.Entry(form_frame, width=30)
        self.isbn_entry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Год:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        self.year_entry = ttk.Entry(form_frame, width=10)
        self.year_entry.grid(row=1, column=3, padx=5, pady=2)

        ttk.Label(form_frame, text="Количество:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.quantity_entry = ttk.Entry(form_frame, width=10)
        self.quantity_entry.grid(row=2, column=1, padx=5, pady=2)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)

        self.add_button = ttk.Button(button_frame, text="Добавить", command=self.add_book)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.update_button = ttk.Button(button_frame, text="Обновить", command=self.update_book)
        self.update_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ttk.Button(button_frame, text="Удалить", command=self.delete_selected)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.borrow_button = ttk.Button(button_frame, text="Выдать", command=self.borrow_selected)
        self.borrow_button.pack(side=tk.LEFT, padx=5)

        self.return_button = ttk.Button(button_frame, text="Вернуть", command=self.return_selected)
        self.return_button.pack(side=tk.LEFT, padx=5)

        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(search_frame, text="Поиск:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_entry.bind('<KeyRelease>', self.on_search_change)

        search_button = ttk.Button(search_frame, text="Поиск", command=self.on_search_change)
        search_button.pack(side=tk.LEFT, padx=5)

        columns = ("ID", "Название", "Автор", "ISBN", "Год", "Количество", "Доступно")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)

        self.tree.bind('<Double-1>', self.on_item_double_click)

    def refresh_books(self) -> None:

        for item in self.tree.get_children():
            self.tree.delete(item)

        books = self.book_controller.get_all_books()
        for book in books:
            self.tree.insert("", "end", values=(
                book.id, book.title, book.author, book.isbn, 
                book.year, book.quantity, book.available
            ))

    def add_book(self) -> None:
        try:
            title = self.title_entry.get().strip()
            author = self.author_entry.get().strip()
            isbn = self.isbn_entry.get().strip()
            year = int(self.year_entry.get().strip())
            quantity = int(self.quantity_entry.get().strip())

            if not title or not author or not isbn:
                messagebox.showerror("Ошибка", "Заполните все обязательные поля")
                return

            self.book_controller.add_book(title, author, isbn, year, quantity)
            self.clear_form()
            self.refresh_books()
            messagebox.showinfo("Успех", "Книга добавлена")
        except ValueError:
            messagebox.showerror("Ошибка", "Год и количество должны быть числами")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить книгу: {e}")

    def update_book(self) -> None:
        try:
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showwarning("Предупреждение", "Выберите книгу для обновления")
                return

            item = self.tree.item(selected_item)
            book_id = item['values'][0]

            title = self.title_entry.get().strip()
            author = self.author_entry.get().strip()
            isbn = self.isbn_entry.get().strip()
            year = int(self.year_entry.get().strip())
            quantity = int(self.quantity_entry.get().strip())

            if not title or not author or not isbn:
                messagebox.showerror("Ошибка", "Заполните все обязательные поля")
                return

            self.book_controller.update_book(
                book_id, title=title, author=author, 
                isbn=isbn, year=year, quantity=quantity
            )
            self.clear_form()
            self.refresh_books()
            messagebox.showinfo("Успех", "Книга обновлена")
        except ValueError:
            messagebox.showerror("Ошибка", "Год и количество должны быть числами")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить книгу: {e}")

    def delete_selected(self) -> None:
        try:
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showwarning("Предупреждение", "Выберите книгу для удаления")
                return

            item = self.tree.item(selected_item)
            book_id = item['values'][0]

            if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить эту книгу?"):
                self.book_controller.delete_book(book_id)
                self.refresh_books()
                messagebox.showinfo("Успех", "Книга удалена")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить книгу: {e}")

    def borrow_selected(self) -> None:
        try:
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showwarning("Предупреждение", "Выберите книгу для выдачи")
                return

            item = self.tree.item(selected_item)
            book_id = item['values'][0]
            available = item['values'][6]  

            if available <= 0:
                messagebox.showwarning("Предупреждение", "Нет доступных экземпляров для выдачи")
                return

            success = self.book_controller.borrow_book(book_id)
            if success:
                self.refresh_books()
                messagebox.showinfo("Успех", "Книга выдана")
            else:
                messagebox.showerror("Ошибка", "Не удалось выдать книгу")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось выдать книгу: {e}")

    def return_selected(self) -> None:
        try:
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showwarning("Предупреждение", "Выберите книгу для возврата")
                return

            item = self.tree.item(selected_item)
            book_id = item['values'][0]

            success = self.book_controller.return_book(book_id)
            if success:
                self.refresh_books()
                messagebox.showinfo("Успех", "Книга возвращена")
            else:
                messagebox.showerror("Ошибка", "Не удалось вернуть книгу")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось вернуть книгу: {e}")

    def on_item_double_click(self, event) -> None:
        try:
            selected_item = self.tree.selection()
            if not selected_item:
                return

            item = self.tree.item(selected_item)
            values = item['values']

            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, values[1])

            self.author_entry.delete(0, tk.END)
            self.author_entry.insert(0, values[2])

            self.isbn_entry.delete(0, tk.END)
            self.isbn_entry.insert(0, values[3])

            self.year_entry.delete(0, tk.END)
            self.year_entry.insert(0, values[4])

            self.quantity_entry.delete(0, tk.END)
            self.quantity_entry.insert(0, values[5])
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные книги: {e}")

    def clear_form(self) -> None:
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.isbn_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)

    def on_search_change(self, event=None) -> None:
        query = self.search_entry.get().strip()
        if query:
            books = self.book_controller.search_books(query)
        else:
            books = self.book_controller.get_all_books()

        
        for item in self.tree.get_children():
            self.tree.delete(item)

       
        for book in books:
            self.tree.insert("", "end", values=(
                book.id, book.title, book.author, book.isbn, 
                book.year, book.quantity, book.available
            ))