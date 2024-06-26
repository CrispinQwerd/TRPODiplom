import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar

# Возможные состояния задачи
TASK_STATES = ["в процессе", "выполнено", "не выполнено"]

class DailyPlanner:
    def __init__(self, master):
        # Инициализация основного окна приложения и его компонентов
        self.master = master
        self.master.title("Ежедневник")  # Установка заголовка окна

        # Инициализация списка задач
        self.tasks = []

        # Создание метки для выбора даты
        self.date_label = tk.Label(master, text="Выберите дату:")
        self.date_label.grid(row=0, column=0, padx=10, pady=5)

        # Создание календаря для выбора даты
        self.calendar = Calendar(master, selectmode="day", date_pattern="yyyy-MM-dd")
        self.calendar.grid(row=0, column=1, padx=10, pady=5)

        # Создание поля ввода для добавления задачи
        self.task_entry = tk.Entry(master, width=50)
        self.task_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        # Создание кнопки для добавления задачи
        self.add_button = tk.Button(master, text="Добавить задачу", command=self.add_task)
        self.add_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Создание списка для отображения задач
        self.task_listbox = tk.Listbox(master, width=60)
        self.task_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Создание кнопки для удаления выбранной задачи
        self.delete_button = tk.Button(master, text="Удалить выбранную задачу", command=self.delete_task)
        self.delete_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Создание радиокнопок для выбора состояния задачи
        self.state_var = tk.StringVar(value=TASK_STATES[0])  # Изначально состояние "в процессе"
        for i, state in enumerate(TASK_STATES):
            tk.Radiobutton(master, text=state, variable=self.state_var, value=state).grid(row=5+i, column=0, columnspan=2, padx=5, pady=1)

        # Создание кнопки для изменения состояния задачи
        self.change_state_button = tk.Button(master, text="Изменить состояние задачи", command=self.change_task_state)
        self.change_state_button.grid(row=5+len(TASK_STATES), column=0, columnspan=2, padx=5, pady=5)

        # Создание кнопки для сохранения задач в файл
        self.save_button = tk.Button(master, text="Сохранить", command=self.save_tasks)
        self.save_button.grid(row=6+len(TASK_STATES), column=0, columnspan=2, padx=5, pady=5)

        # Загрузка списка задач при запуске приложения
        self.load_tasks()

    def add_task(self):
        # Добавление задачи в список задач
        task = self.task_entry.get()
        date = self.calendar.get_date()
        if task:
            self.tasks.append((date, task, self.state_var.get()))
            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Пустая задача", "Введите текст задачи!")

    def delete_task(self):
        # Удаление выбранной задачи из списка задач
        try:
            selection = self.task_listbox.curselection()[0]
            del self.tasks[selection]
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("Нет выбранной задачи", "Выберите задачу для удаления!")

    def update_task_listbox(self):
        # Обновление списка задач в виджете Listbox
        self.task_listbox.delete(0, tk.END)
        for date, task, state in self.tasks:
            self.task_listbox.insert(tk.END, f"{date}: {task} ({state})")

    def change_task_state(self):
        # Изменение состояния выбранной задачи
        try:
            selection = self.task_listbox.curselection()[0]
            self.tasks[selection] = (self.tasks[selection][0], self.tasks[selection][1], self.state_var.get())
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("Нет выбранной задачи", "Выберите задачу для изменения состояния!")

    def save_tasks(self):
        # Сохранение текущего списка задач в файл
        with open("tasks.txt", "w", encoding="utf-8") as file:
            for date, task, state in self.tasks:
                file.write(f"{date}: {task}: {state}\n")
        messagebox.showinfo("Сохранение", "Задачи сохранены успешно!")

    def load_tasks(self):
        # Загрузка списка задач из файла (если он существует)
        try:
            with open("tasks.txt", "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split(": ")
                    if len(parts) == 3:
                        self.tasks.append((parts[0], parts[1], parts[2]))
            self.update_task_listbox()
        except FileNotFoundError:
            pass

def main():
    root = tk.Tk()
    app = DailyPlanner(root)
    root.mainloop()

if __name__ == "__main__":
    main()
