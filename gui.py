import tkinter as tk
from tkinter import filedialog
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import threading

def make_request():
    global request_count, error_count

    url = url_entry.get()
    request_limit = int(requests_entry.get())
    start_time = int(start_entry.get())
    stop_time = int(stop_entry.get())

    if request_count >= request_limit:
        stop_requests()
        return

    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Menjalankan Chrome dalam mode headless
        options.add_argument('--remote-debugging-port=0')  # Menonaktifkan DevTools

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(30)

        driver.get(url)

        driver.quit()

        request_count += 1

        log_text.configure(state=tk.NORMAL)
        log_text.insert(tk.END, f"{request_count}. Request  success\n", "success")
        log_text.configure(state=tk.DISABLED)

    except Exception as e:
        log_text.configure(state=tk.NORMAL)
        log_text.insert(tk.END, f"{request_count}. Request  fail\n", "error")
        log_text.configure(state=tk.DISABLED)
        error_count += 1

    if request_count < request_limit:
        wait_time = random.randint(start_time, stop_time)
        log_text.after(wait_time * 1000, make_request)  # Waktu dalam milidetik
    else:
        log_text.configure(state=tk.NORMAL)
        log_text.insert(tk.END, f"REQUEST END\n\n", "success")
        log_text.configure(state=tk.DISABLED)
        stop_requests()

def start_requests():
    global request_count, error_count

    url = url_entry.get()
    request_limit = int(requests_entry.get())

    if not url or not request_limit:
        return

    request_count = 0
    error_count = 0

    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    clear_button.config(state=tk.DISABLED)
    url_entry.config(state=tk.DISABLED)
    requests_entry.config(state=tk.DISABLED)
    start_entry.config(state=tk.DISABLED)
    stop_entry.config(state=tk.DISABLED)

    log_text.configure(state=tk.NORMAL)
    log_text.delete('1.0', tk.END)
    log_text.configure(state=tk.DISABLED)

    # Membuat thread baru untuk menjalankan permintaan
    request_thread = threading.Thread(target=make_request)
    request_thread.start()

def stop_requests():
    global request_count, error_count

    request_count = 0
    error_count = 0

    # Kembalikan GUI ke keadaan semula
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    clear_button.config(state=tk.NORMAL)
    url_entry.config(state=tk.NORMAL)
    requests_entry.config(state=tk.NORMAL)
    start_entry.config(state=tk.NORMAL)
    stop_entry.config(state=tk.NORMAL)

def clear_logs():
    log_text.configure(state=tk.NORMAL)
    log_text.delete('1.0', tk.END)
    log_text.configure(state=tk.DISABLED)
    clear_button.config(state=tk.DISABLED)

window = tk.Tk()
window.title("HTTP Requester")
window.geometry("400x400")

url_label = tk.Label(window, text="URL:")
url_label.pack()
url_entry = tk.Entry(window, width=50)
url_entry.pack()

requests_label = tk.Label(window, text="Request Limit:")
requests_label.pack()
requests_entry = tk.Entry(window, width=10)
requests_entry.pack()

start_label = tk.Label(window, text="Start Time (sec):")
start_label.pack()
start_entry = tk.Entry(window, width=10)
start_entry.pack()

stop_label = tk.Label(window, text="Stop Time (sec):")
stop_label.pack()
stop_entry = tk.Entry(window, width=10)
stop_entry.pack()

start_button = tk.Button(window, text="Start Requests", command=start_requests)
start_button.pack()

stop_button = tk.Button(window, text="Stop", command=stop_requests, state=tk.DISABLED)
stop_button.pack()

clear_button = tk.Button(window, text="Clear Logs", command=clear_logs, state=tk.DISABLED)
clear_button.pack()

log_label = tk.Label(window, text="Logs:")
log_label.pack()
log_text = tk.Text(window, height=15, width=50)
log_text.pack()
log_text.configure(state=tk.DISABLED)

log_text.tag_configure("success", foreground="green")
log_text.tag_configure("error", foreground="red")

window.mainloop()
