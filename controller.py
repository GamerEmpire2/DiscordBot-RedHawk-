import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys

# Define the path to your virtual environment's Python executable
if os.name == 'nt':  # For Windows
    venv_python = os.path.join('venv', 'Scripts', 'python.exe')
else:  # For Unix-like OS
    venv_python = os.path.join('venv', 'bin', 'python')

# Define bot control functions
main_bot_running = False
logger_bot_running = False

main_bot_process = None
logger_bot_process = None

def start_main_bot():
    global main_bot_running, main_bot_process
    if not main_bot_running:
        try:
            main_bot_process = subprocess.Popen([venv_python, 'server\\main_bot.py'])
            main_bot_running = True
            status_label_main.config(text="Main Bot: Running")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start Main Bot: {e}")
    else:
        messagebox.showinfo("Info", "Main Bot is already running.")

def stop_main_bot():
    global main_bot_running, main_bot_process
    if main_bot_running:
        main_bot_process.terminate()
        main_bot_running = False
        status_label_main.config(text="Main Bot: Stopped")
    else:
        messagebox.showinfo("Info", "Main Bot is already stopped.")

def start_logger_bot():
    global logger_bot_running, logger_bot_process
    if not logger_bot_running:
        try:
            logger_bot_process = subprocess.Popen([venv_python, 'server\\logger_bot.py'])
            logger_bot_running = True
            status_label_logger.config(text="Logger Bot: Running")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start Logger Bot: {e}")
    else:
        messagebox.showinfo("Info", "Logger Bot is already running.")

def stop_logger_bot():
    global logger_bot_running, logger_bot_process
    if logger_bot_running:
        logger_bot_process.terminate()
        logger_bot_running = False
        status_label_logger.config(text="Logger Bot: Stopped")
    else:
        messagebox.showinfo("Info", "Logger Bot is already stopped.")

# Initialize main window
root = tk.Tk()
root.title("Bot Controller")

# Create buttons for main bot
start_button_main = tk.Button(root, text="Start Main Bot", command=start_main_bot)
stop_button_main = tk.Button(root, text="Stop Main Bot", command=stop_main_bot)
start_button_main.grid(row=0, column=0, padx=10, pady=10)
stop_button_main.grid(row=0, column=1, padx=10, pady=10)

# Create status label for main bot
status_label_main = tk.Label(root, text="Main Bot: Stopped")
status_label_main.grid(row=0, column=2, padx=10, pady=10)

# Create buttons for logger bot
start_button_logger = tk.Button(root, text="Start Logger Bot", command=start_logger_bot)
stop_button_logger = tk.Button(root, text="Stop Logger Bot", command=stop_logger_bot)
start_button_logger.grid(row=1, column=0, padx=10, pady=10)
stop_button_logger.grid(row=1, column=1, padx=10, pady=10)

# Create status label for logger bot
status_label_logger = tk.Label(root, text="Logger Bot: Stopped")
status_label_logger.grid(row=1, column=2, padx=10, pady=10)

# Check if this file is being run directly
if __name__ == "__main__":
    # Run the main event loop
    root.mainloop()