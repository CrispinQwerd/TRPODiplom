import tkinter as tk
from tkinter import messagebox
import re

daily_planner = {}

def is_valid_date(date_str):
    # Проверка формата даты (дд-мм-гггг)
    if not re.match(r'\d{2}-\d{2}-\d{4}', date_str):
        return False
    
    # Разделение даты на день, месяц и год
    day, month, year = map(int, date_str.split('-'))
    
    # Проверка корректности дня и месяца
    if month < 1 or month > 12:
        return False
    if day < 1 or day > 31:
        return False
    
    # Проверка корректности числа дней в месяце
    if month in [4, 6, 9, 11] and day > 30:
        return False
    if month == 2:
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            if day > 29:
                return False
        elif day > 28:
            return False
    
    return True

def add_event():
    date = date_entry.get()
    event = event_entry.get()
    
    # Проверка правильности формата даты
    if not is_valid_date(date):
        messagebox.showerror("Ошибка", "Неправильный формат даты или неверная дата.")
        return
    
    if date == "" or event == "":
        messagebox.showerror("Ошибка", "Пожалуйста, введите дату и событие.")
        return
    
    if date not in daily_planner:
        daily_planner[date] = []
    daily_planner[date].append(event)
    
    # Запись событий в текстовый файл
    with open("daily_planner.txt", "a") as file:
        file.write(f"{date}: {event}\n")
    
    messagebox.showinfo("Успех", "Событие добавлено успешно.")

def view_events():
    date = date_entry.get()
    if date in daily_planner:
        events = "\n".join(daily_planner[date])
        messagebox.showinfo("События на день", events)
    else:
        messagebox.showinfo("События на день", "Нет событий на этот день.")

# Создание главного окна
root = tk.Tk()
root.title("Ежедневник")

# Создание и размещение виджетов
date_label = tk.Label(root, text="Дата (дд-мм-гггг):")
date_label.grid(row=0, column=0, padx=5, pady=5)

date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1, padx=5, pady=5)

event_label = tk.Label(root, text="Событие:")
event_label.grid(row=1, column=0, padx=5, pady=5)

event_entry = tk.Entry(root)
event_entry.grid(row=1, column=1, padx=5, pady=5)

add_button = tk.Button(root, text="Добавить событие", command=add_event)
add_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="we")

view_button = tk.Button(root, text="Просмотреть события", command=view_events)
view_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")

# Запуск главного цикла обработки событий
root.mainloop()
