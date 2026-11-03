import tkinter as tk
from tkinter import simpledialog
import random
import sys
import winsound
import threading
import multiprocessing
import time


# Функция для максимальной нагрузки ядра процессора
# Она должна быть вынесена на верхний уровень файла для корректной работы multiprocessing
def cpu_stress_worker():
    while True:
        pass  # Бесконечный цикл, загружающий ядро на 100%


class FullscreenScreamerVirus:
    def __init__(self, root):
        self.root = root
        self.root.title("SYSTEM CRITICAL ERROR")

        # Блокируем закрытие окна (Alt + F4)
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)

        # Разворачиваем окно на весь экран поверх остальных
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="black")

        # Скрываем курсор мыши
        self.root.config(cursor="none")

        self.countdown = 10
        self.screamer_activated = False
        self.cpu_processes = []

        # Запускаем нагрузку на процессор одновременно со стартом окна
        self.start_cpu_stress()

        # Визуальные элементы
        self.lbl_title = tk.Label(
            self.root,
            text="⚠️ SYSTEM CORRUPTION DETECTED ⚠️",
            font=("Courier New", 28, "bold"),
            bg="black",
            fg="#ff0000"
        )
        self.lbl_title.pack(pady=50)

        self.log_text = tk.Label(
            self.root,
            text="Инициализация протокола матрицы...\n"
                 "Обход брандмауэра Windows... [УСПЕШНО]\n"
                 "Подключение к ядру системы 3.14...\n"
                 "Запуск стресс-теста процессора... [100% CPU]",
            font=("Courier New", 14),
            bg="black",
            fg="#00ff00",
            justify="left"
        )
        self.log_text.pack(pady=20)

        self.lbl_timer = tk.Label(
            self.root,
            text=f"До перезагрузки осталось: {self.countdown} сек.",
            font=("Arial", 22, "bold"),
            bg="black",
            fg="white"
        )
        self.lbl_timer.pack(pady=40)

        # Бинд на секретную комбинацию для ввода пароля (Alt + Escape)
        self.root.bind("<Alt-Escape>", lambda e: self.check_password())

        # Запуск фоновых эффектов и таймера
        self.glitch_effect()
        self.countdown_loop()

    def start_cpu_stress(self):
        """Запуск фоновых процессов для полной загрузки процессора"""
        cores = multiprocessing.cpu_count()
        for _ in range(cores):
            p = multiprocessing.Process(target=cpu_stress_worker)
            p.daemon = True
            p.start()
            self.cpu_processes.append(p)

    def stop_cpu_stress(self):
        """Остановка всех нагружающих процессов"""
        for p in self.cpu_processes:
            p.terminate()

    def glitch_effect(self):
        if self.screamer_activated:
            return

        current_fg = self.lbl_title.cget("fg")
        new_fg = "black" if current_fg == "#ff0000" else "#ff0000"
        self.lbl_title.config(fg=new_fg)

        if random.random() < 0.15:
            self.log_text.config(bg="#440000")
        else:
            self.log_text.config(bg="black")

        self.root.after(200, self.glitch_effect)

    def countdown_loop(self):
        if self.screamer_activated:
            return

        if self.countdown > 0:
            self.countdown -= 1
            self.lbl_timer.config(text=f"До перезагрузки осталось: {self.countdown} сек.")
            self.root.after(1000, self.countdown_loop)
        else:
            self.activate_screamer()

    def creepy_sound_thread(self):
        for _ in range(8):
            freq = random.randint(100, 600)
            duration = random.randint(300, 800)
            winsound.Beep(freq, duration)
            time.sleep(random.uniform(0.1, 0.4))
        winsound.Beep(150, 2000)

    def activate_screamer(self):
        self.screamer_activated = True

        # Звук в отдельном потоке
        threading.Thread(target=self.creepy_sound_thread, daemon=True).start()

        self.lbl_title.pack_forget()
        self.log_text.pack_forget()
        self.lbl_timer.pack_forget()

        self.lbl_screamer = tk.Label(
            self.root,
            text="       👹 👹 👹       \n\n"
                 "💀 nmk 💀\n\n"
                 "   ",
            font=("Courier New", 45, "bold"),
            bg="black",
            fg="#ff0000"
        )
        self.lbl_screamer.pack(expand=True)

        self.flash_screen_loop()

    def flash_screen_loop(self):
        if not self.screamer_activated:
            return

        current_bg = self.root.cget("bg")
        if current_bg == "black":
            self.root.configure(bg="#550000")
            self.lbl_screamer.config(bg="#550000", fg="black")
        else:
            self.root.configure(bg="black")
            self.lbl_screamer.config(bg="black", fg="#ff0000")

        self.root.after(70, self.flash_screen_loop)

    def check_password(self):
        self.root.config(cursor="")
        password = simpledialog.askstring("ACCESS REQUIRED", "Введите ключ деактивации:", show='*', parent=self.root)

        if password == "1234":
            self.safe_exit()
        else:
            self.root.config(cursor="none")

    def safe_exit(self):
        self.stop_cpu_stress()  # Гасим нагрузку на процессор перед выходом
        self.root.config(cursor="")
        self.root.attributes("-fullscreen", False)
        self.root.destroy()
        sys.exit()


if __name__ == "__main__":
    # Защита для корректной работы multiprocessing в Windows
    multiprocessing.freeze_support()

    root = tk.Tk()
    app = FullscreenScreamerVirus(root)
    root.mainloop()
