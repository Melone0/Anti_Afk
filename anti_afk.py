import tkinter as tk
from tkinter import ttk
import pyautogui
import time
import random
from threading import Thread

# Deaktiviere die FAILSAFE-Funktion von PyAutoGUI
pyautogui.FAILSAFE = False
valid_time = True

class AntiAFK(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AntiAFK")
        self.geometry("300x250")

        # Initialisiere Variablen für Mausbewegung
        self.move_mouse = False
        self.mouse_movement_thread = None
        self.move_mouse_var = tk.BooleanVar()

        # Hotkey-Einstellungen
        self.hotkey_var = tk.StringVar()
        self.hotkey_entry = ttk.Entry(self, textvariable=self.hotkey_var)
        self.hotkey_label = ttk.Label(self, text="Hotkey:")
        self.hotkey_label.grid(column=0, row=7)
        self.hotkey_entry.grid(column=1, row=7)

        # Erstelle GUI-Elemente
        self.create_widgets()
        self.error_label = ttk.Label(self, text="", foreground="red")
        self.error_label.grid(column=1, row=9)

    def create_widgets(self):
        # Statusvariablen für die Anzeige
        self.status = tk.StringVar()
        self.status.set("Move Off")

        # Labels für den Status der Mausbewegung
        self.move_on_label = tk.Label(self, text="On", fg="green")
        self.move_off_label = tk.Label(self, text="Off", fg="red")

        # GUI-Elemente für Mausbewegung
        ttk.Label(self, text="Move Mouse:").grid(column=0, row=0)
        self.move_off_label.grid(column=1, row=0)

        ttk.Button(self, text="Turn On", command=self.turn_on).grid(column=0, row=1)
        ttk.Button(self, text="Turn Off", command=self.turn_off).grid(column=1, row=1)

        ttk.Label(self, text=" ").grid(column=0, row=5)

        # GUI-Elemente für die Sleep-Zeiteinstellung
        ttk.Label(self, text="Set Sleep-Time:").grid(column=0, row=6)
        self.sleep_time_var = tk.StringVar()
        self.sleep_time_entry = ttk.Entry(self, textvariable=self.sleep_time_var)
        self.sleep_time_entry.grid(column=1, row=6)
        ttk.Label(self, text="seconds").grid(column=3, row=6)

        # Button zum Einreichen der Sleep-Zeit
        ttk.Button(self, text="Submit", command=self.submit_sleep_time).grid(column=1, row=8)

        # Hotkey-Bindung
        self.bind("<KeyPress>", self.check_hotkey)

    def turn_on(self):
        # Schaltet die Mausbewegung ein und zeigt die Sleep-Zeit-Widgets an
        self.status.set("Move On")
        self.move_on_label.grid(column=1, row=0)
        self.move_off_label.grid_forget()
        self.move_mouse = True
        self.show_sleep_time_widgets()
        self.start_mouse_movement_thread()

    def turn_off(self):
        # Schaltet die Mausbewegung aus und versteckt die Sleep-Zeit-Widgets
        self.status.set("Move Off")
        self.move_off_label.grid(column=1, row=0)
        self.move_on_label.grid_forget()
        self.move_mouse = False
        self.move_mouse_var.set(False)

    def submit_sleep_time(self):
        # Verarbeitet die eingegebene Sleep-Zeit und startet die Mausbewegung
        sleep_time_str = self.sleep_time_var.get()

        if sleep_time_str and sleep_time_str.isdigit():
            self.error_label.config(text="")
            while self.move_mouse:
                x = random.randint(600, 700)
                y = random.randint(200, 600)
                pyautogui.moveTo(x, y, 0, 5)
                time.sleep(int(sleep_time_str))
                self.move_mouse_var.set(True)
                self.update()  # Aktualisiere das GUI, um zu verhindern, dass es einfriert
        else:
            self.error_label.config(text="Enter a Valid Sleep Time")
            # Schedule the removal of the error message after 3000 milliseconds (3 seconds)
            self.after(3000, self.clear_error_message)

    def clear_error_message(self):
        # Clears the error message
        self.error_label.config(text="")


    def start_mouse_movement_thread(self):
        # Startet einen Thread für die Mausbewegung
        self.mouse_movement_thread = Thread(target=self.submit_sleep_time)
        self.mouse_movement_thread.start()

    def show_sleep_time_widgets(self):
        # Zeigt die Sleep-Zeit-Widgets an
        self.sleep_time_entry.config(state='normal')

    def check_hotkey(self, event):
        # Überprüft, ob der gedrückte Hotkey mit dem festgelegten Hotkey übereinstimmt
        hotkey_pressed = event.char.lower()
        target_hotkey = self.hotkey_var.get().lower()

        if hotkey_pressed == target_hotkey:
            self.turn_off()

if __name__ == "__main__":
    # Startet die Anwendung
    app = AntiAFK()
    app.mainloop()
