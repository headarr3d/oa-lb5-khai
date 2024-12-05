import tkinter as tk
from tkinter import messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import math


# Завдання 1: Клас для розрахунку площі кіл
class CircleCalculator(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill=tk.BOTH, expand=True)

        # Поля для введення радіусів
        self.label_r1 = tk.Label(self, text="Радіус 1:")
        self.entry_r1 = tk.Entry(self)

        self.label_r2 = tk.Label(self, text="Радіус 2:")
        self.entry_r2 = tk.Entry(self)

        self.label_r3 = tk.Label(self, text="Радіус 3:")
        self.entry_r3 = tk.Entry(self)

        # Кнопка для обчислення
        self.calc_button = tk.Button(self, text="Обчислити площі", command=self.calculate_areas)

        # Поле для виведення результату
        self.result_label = tk.Label(self, text="Результати:")
        self.result_text = tk.Text(self, height=5, state=tk.DISABLED)

        # Розміщення віджетів
        self.label_r1.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_r1.grid(row=0, column=1, padx=5, pady=5)

        self.label_r2.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_r2.grid(row=1, column=1, padx=5, pady=5)

        self.label_r3.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_r3.grid(row=2, column=1, padx=5, pady=5)

        self.calc_button.grid(row=3, column=0, columnspan=2, pady=10)
        self.result_label.grid(row=4, column=0, sticky=tk.W, padx=5)
        self.result_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def calculate_areas(self):
        # Обчислення площі трьох кіл
        try:
            # Зчитування значень радіусів
            r1 = float(self.entry_r1.get())
            r2 = float(self.entry_r2.get())
            r3 = float(self.entry_r3.get())

            # Перевірка на невід'ємність
            if r1 < 0 or r2 < 0 or r3 < 0:
                raise ValueError("Радіус має бути невід'ємним числом!")

            # Обчислення площ
            areas = [self.circle_area(r) for r in (r1, r2, r3)]

            # Виведення результатів
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Площа кола 1: {areas[0]:.2f}\n")
            self.result_text.insert(tk.END, f"Площа кола 2: {areas[1]:.2f}\n")
            self.result_text.insert(tk.END, f"Площа кола 3: {areas[2]:.2f}\n")
            self.result_text.config(state=tk.DISABLED)
        except ValueError as e:
            messagebox.showerror("Помилка введення", str(e))

    @staticmethod
    def circle_area(radius):
        # Обчислення площі кола
        pi = 3.14
        return pi * radius ** 2


# Завдання 2: Клас для роботи з графіками і файлами
class GraphApp(tk.Frame):
    # Клас для роботи з файлами і графіками.

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill=tk.BOTH, expand=True)

        # Кнопки
        self.create_file_btn = tk.Button(self, text="Створити файл", command=self.create_file)
        self.open_file_btn = tk.Button(self, text="Відкрити файл", command=self.open_file)
        self.plot_graph_btn = tk.Button(self, text="Побудувати графік", command=self.plot_graph)

        # Розміщення кнопок
        self.create_file_btn.grid(row=0, column=0, padx=5, pady=5)
        self.open_file_btn.grid(row=0, column=1, padx=5, pady=5)
        self.plot_graph_btn.grid(row=0, column=2, padx=5, pady=5)

        self.data = None  # Зчитані дані з файлу

    def create_file(self):
        # Створення текстового файлу з даними.
        try:
            # Генерація даних
            t = [i * 0.01 for i in range(101)]  # 101 точка
            y = [3.14 * math.sin(2 * math.pi * t[i]) for i in range(len(t))]
            lines = [f"{t[i]:.2f};{y[i]:.2f}\n" for i in range(len(t))]

            # Збереження файлу
            file = filedialog.asksaveasfile(mode='w', defaultextension=".txt",
                                            filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
            if file:
                file.writelines(lines)
                file.close()
                messagebox.showinfo("Успіх", "Файл успішно створено!")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def open_file(self):
        # Зчитування даних із файлу
        try:
            file = filedialog.askopenfile(mode='r', filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
            if file:
                self.data = [line.strip().split(';') for line in file.readlines()]
                file.close()
                messagebox.showinfo("Успіх", "Дані успішно зчитано!")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def plot_graph(self):
        # Побудова графіка
        if not self.data:
            messagebox.showwarning("Попередження", "Дані відсутні!")
            return
        try:
            x = [float(row[0]) for row in self.data]
            y = [float(row[1]) for row in self.data]

            # Побудова графіка
            fig = Figure(figsize=(5, 4))
            ax = fig.add_subplot(111)
            ax.plot(x, y, label="Графік функції", color="blue")
            ax.set_title("Графік функції")
            ax.set_xlabel("Час t")
            ax.set_ylabel("Значення y")
            ax.grid(True)
            ax.legend()

            # Відображення на Canvas
            canvas = FigureCanvasTkAgg(fig, master=self)
            canvas.get_tk_widget().grid(row=1, column=0, columnspan=3, padx=5, pady=5)
            canvas.draw()
        except Exception as e:
            messagebox.showerror("Помилка", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("lab5_3-91AVS-v01-Opanasiuk_Oleksandr")

    # Перемикач між завданнями
    tab_control = tk.Frame(root)
    tab_control.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    calc_app = CircleCalculator(tab_control)
    graph_app = GraphApp(tab_control)

    root.mainloop()
