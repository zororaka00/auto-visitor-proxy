import tkinter as tk
from tkinter import filedialog
import requests
import random
import time
from threading import Thread

def load_proxy_list(file_path):
    with open(file_path, 'r') as file:
        proxy_list = file.read().splitlines()
    return proxy_list

def load_user_agents(file_path):
    with open(file_path, 'r') as file:
        user_agents = file.read().splitlines()
    return user_agents

def load_referers(file_path):
    with open(file_path, 'r') as file:
        referers = file.read().splitlines()
    return referers

def change_proxy(proxy_list):
    proxy = random.choice(proxy_list)
    proxies = {
        'http': proxy,
        'https': proxy
    }
    return proxies

def select_user_agent(user_agents):
    user_agent = random.choice(user_agents)
    headers = {
        'User-Agent': user_agent
    }
    return headers

def select_referer(referers):
    referer = random.choice(referers)
    headers = {
        'Referer': referer
    }
    return headers

def make_request(url, proxies, headers):
    try:
        response = requests.get(url, proxies=proxies, headers=headers, timeout=30)
        if response.status_code == 200:
            proxy = proxies.get('http', '')
            referer = headers.get('Referer', '')
            user_agent = headers.get('User-Agent', '')
            log_text.insert(tk.END, f"Request successful - Proxy: {proxy}, Referer: {referer}, User Agent: {user_agent}\n", "success")
        else:
            log_text.insert(tk.END, "Request failed\n", "error")
    except requests.exceptions.RequestException:
        log_text.insert(tk.END, "Request failed\n", "error")

def start_requests():
    global running
    url = url_entry.get()
    request_limit = int(requests_entry.get())
    proxy_file_path = proxy_entry.get()
    user_agents_file_path = user_agents_entry.get()
    referers_file_path = referers_entry.get()
    start_time = int(start_entry.get())
    stop_time = int(stop_entry.get())

    proxy_list = load_proxy_list(proxy_file_path)
    random.shuffle(proxy_list)
    user_agents = load_user_agents(user_agents_file_path)
    referers = load_referers(referers_file_path)

    request_count = 0
    error_count = 0
    running = True

    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    url_entry.config(state=tk.DISABLED)
    requests_entry.config(state=tk.DISABLED)
    proxy_entry.config(state=tk.DISABLED)
    user_agents_entry.config(state=tk.DISABLED)
    referers_entry.config(state=tk.DISABLED)
    proxy_browse_button.config(state=tk.DISABLED)
    user_agents_browse_button.config(state=tk.DISABLED)
    referers_browse_button.config(state=tk.DISABLED)
    start_entry.config(state=tk.DISABLED)
    stop_entry.config(state=tk.DISABLED)

    while request_count < request_limit and running:
        proxies = change_proxy(proxy_list)
        user_agent_headers = select_user_agent(user_agents)
        referer_headers = select_referer(referers)
        headers = {**user_agent_headers, **referer_headers}

        try:
            make_request(url, proxies, headers)
            request_count += 1
        except:
            error_count += 1
            log_text.insert(tk.END, "Request failed\n", "error")

        if error_count > 0:
            continue

        wait_time = random.randint(start_time, stop_time)
        time.sleep(wait_time)

    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    url_entry.config(state=tk.NORMAL)
    requests_entry.config(state=tk.NORMAL)
    proxy_entry.config(state=tk.NORMAL)
    user_agents_entry.config(state=tk.NORMAL)
    referers_entry.config(state=tk.NORMAL)
    proxy_browse_button.config(state=tk.NORMAL)
    user_agents_browse_button.config(state=tk.NORMAL)
    referers_browse_button.config(state=tk.NORMAL)
    start_entry.config(state=tk.NORMAL)
    stop_entry.config(state=tk.NORMAL)

def stop_requests():
    global running
    running = False

def browse_proxy_file():
    file_path = filedialog.askopenfilename()
    proxy_entry.delete(0, tk.END)
    proxy_entry.insert(tk.END, file_path)

def browse_user_agents_file():
    file_path = filedialog.askopenfilename()
    user_agents_entry.delete(0, tk.END)
    user_agents_entry.insert(tk.END, file_path)

def browse_referers_file():
    file_path = filedialog.askopenfilename()
    referers_entry.delete(0, tk.END)
    referers_entry.insert(tk.END, file_path)

window = tk.Tk()
window.title("HTTP Requester")
window.geometry("400x600")

url_label = tk.Label(window, text="URL:")
url_label.pack()
url_entry = tk.Entry(window, width=50)
url_entry.pack()

requests_label = tk.Label(window, text="Request Limit:")
requests_label.pack()
requests_entry = tk.Entry(window, width=10)
requests_entry.pack()

proxy_label = tk.Label(window, text="Proxy File:")
proxy_label.pack()
proxy_entry = tk.Entry(window, width=50)
proxy_entry.pack()
proxy_browse_button = tk.Button(window, text="Browse", command=browse_proxy_file)
proxy_browse_button.pack()

user_agents_label = tk.Label(window, text="User Agents File:")
user_agents_label.pack()
user_agents_entry = tk.Entry(window, width=50)
user_agents_entry.pack()
user_agents_browse_button = tk.Button(window, text="Browse", command=browse_user_agents_file)
user_agents_browse_button.pack()

referers_label = tk.Label(window, text="Referers File:")
referers_label.pack()
referers_entry = tk.Entry(window, width=50)
referers_entry.pack()
referers_browse_button = tk.Button(window, text="Browse", command=browse_referers_file)
referers_browse_button.pack()

start_label = tk.Label(window, text="Start Time (sec):")
start_label.pack()
start_entry = tk.Entry(window, width=10)
start_entry.pack()

stop_label = tk.Label(window, text="Stop Time (sec):")
stop_label.pack()
stop_entry = tk.Entry(window, width=10)
stop_entry.pack()

start_button = tk.Button(window, text="Start Requests", command=lambda: Thread(target=start_requests).start())
start_button.pack()

stop_button = tk.Button(window, text="Stop", command=stop_requests, state=tk.DISABLED)
stop_button.pack()

log_label = tk.Label(window, text="Logs:")
log_label.pack()
log_text = tk.Text(window, height=15, width=50)
log_text.pack()

log_text.tag_configure("success", foreground="green")
log_text.tag_configure("error", foreground="red")

window.mainloop()
