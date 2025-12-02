# Здесь должно быть представление для работы с читателями согласно README.md

import tkinter as tk
from tkinter import ttk, messagebox

class ReaderView(ttk.Frame):
    def __init__(self, parent, reader_controller) -> None:
        super().__init__(parent)
        self.reader_controller = reader_controller
        self.create_widgets()
        self.refresh_readers()

    def create_widgets(self) -> None:
        
        form_frame = ttk.LabelFrame(self, text="Добавить/редактировать читателя", padding=10)
        form_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(form_frame, text="Имя:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.name_entry = ttk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Email:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.email_entry = ttk.Entry(form_frame, width=30)
        self.email_entry.grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(form_frame, text="Телефон:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.phone_entry = ttk.Entry(form_frame, width=30)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=2)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)

        self.add_button = ttk.Button(button_frame, text="Добавить", command=self.add_reader)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.update_button = ttk.Button(button_frame, text="Обновить", command=self.update_reader)
        self.update_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ttk.Button(button_frame, text="Удалить", command=self.delete_selected)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        columns = ("ID", "Имя", "Email", "Телефон", "Дата регистрации")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)

        self.tree.bind('<Double-1>', self.on_item_double_click)

    def refresh_readers(self) -> None:
        
        for item in self.tree.get_children():
            self.tree.delete(item)

        readers = self.reader_controller.get_all_readers()
        for reader in readers:
            self.tree.insert("", "end", values=(
                reader.id, reader.name, reader.email, 
                reader.phone, reader.registration_date.strftime("%Y-%m-%d %H:%M:%S")
            ))

    def add_reader(self) -> None:
        try:
            name = self.name_entry.get().strip()
            email = self.email_entry.get().strip()
            phone = self.phone_entry.get().strip()

            if not name or not email or not phone:
                messagebox.showerror("Ошибка", "Заполните все обязательные поля")
                return

            self.reader_controller.add_reader(name, email, phone)
            self.clear_form()
            self.refresh_readers()
            messagebox.showinfo("Успех", "Читатель добавлен")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить читателя: {e}")

    def update_reader(self) -> None:
        try:
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showwarning("Предупреждение", "Выберите читателя для обновления")
                return

            item = self.tree.item(selected_item)
            reader_id = item['values'][0]

            name = self.name_entry.get().strip()
            email = self.email_entry.get().strip()
            phone = self.phone_entry.get().strip()

            if not name or not email or not phone:
                messagebox.showerror("Ошибка", "Заполните все обязательные поля")
                return

            self.reader_controller.update_reader(
                reader_id, name=name, email=email, phone=phone
            )
            self.clear_form()
            self.refresh_readers()
            messagebox.showinfo("Успех", "Читатель обновлен")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить читателя: {e}")

    def delete_selected(self) -> None:
        try:
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showwarning("Предупреждение", "Выберите читателя для удаления")
                return

            item = self.tree.item(selected_item)
            reader_id = item['values'][0]

            if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этого читателя?"):
                self.reader_controller.delete_reader(reader_id)
                self.refresh_readers()
                messagebox.showinfo("Успех", "Читатель удален")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить читателя: {e}")

    def on_item_double_click(self, event) -> None:
        try:
            selected_item = self.tree.selection()
            if not selected_item:
                return

            item = self.tree.item(selected_item)
            values = item['values']

            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, values[1])

            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, values[2])

            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, values[3])
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные читателя: {e}")

    def clear_form(self) -> None:
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

