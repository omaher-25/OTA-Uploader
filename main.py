import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests
import json
import os

# ---------------- Color Scheme ----------------
COLORS = {
    'bg': '#1a1a2e',
    'card': '#16213e',
    'accent': '#0f3460',
    'highlight': '#e94560',
    'text': '#eaeaea',
    'text_dim': '#a0a0a0',
    'success': '#00d26a',
    'entry_bg': '#0f3460',
    'listbox_bg': '#0f3460',
    'button_hover': '#e94560',
}

def upload_firmware():
    ip = ip_entry.get().strip()
    file_path = file_entry.get().strip()

    if not ip or not file_path:
        status_label.config(text="⚠️ Enter ESP32 IP and select firmware file.", fg=COLORS['highlight'])
        return

    # Disable button and show uploading state
    upload_btn.config(state=tk.DISABLED, text="⏳ Uploading...", bg='#666')
    progress_bar.pack(pady=(5, 0))
    progress_bar.start(10)  # Indeterminate progress
    status_label.config(text="⏳ Uploading firmware...", fg=COLORS['text'])
    root.update()

    url = f"http://{ip}/update"

    try:
        with open(file_path, "rb") as f:
            files = {"file": f}
            r = requests.post(url, files=files, timeout=60)

        if r.status_code == 200:
            status_label.config(text="✅ Firmware uploaded! ESP32 rebooting...", fg=COLORS['success'])
        else:
            status_label.config(text=f"❌ Upload failed. Status: {r.status_code}", fg=COLORS['highlight'])

    except Exception as e:
        status_label.config(text=f"❌ Error: {str(e)[:50]}", fg=COLORS['highlight'])

    # Re-enable button
    upload_btn.config(state=tk.NORMAL, text="🚀 Upload Firmware", bg=COLORS['highlight'])
    progress_bar.stop()
    progress_bar.pack_forget()
    root.update()


# ---------------- IP storage ----------------
IPS_FILE = os.path.join(os.path.dirname(__file__), "ips.json")

def load_ips():
    try:
        if os.path.exists(IPS_FILE):
            with open(IPS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
    except Exception:
        pass
    return []

def save_ips(ips):
    try:
        with open(IPS_FILE, "w", encoding="utf-8") as f:
            json.dump(ips, f, indent=2)
    except Exception as e:
        status_label.config(text=f"❌ Failed saving IPs", fg=COLORS['highlight'])

def refresh_ip_listbox():
    ips = load_ips()
    ip_listbox.delete(0, tk.END)
    for ip in ips:
        ip_listbox.insert(tk.END, f"  📡  {ip}")

def save_current_ip():
    ip = ip_entry.get().strip()
    if not ip:
        status_label.config(text="⚠️ Enter an IP to save.", fg=COLORS['highlight'])
        return
    ips = load_ips()
    if ip in ips:
        status_label.config(text="ℹ️ IP already saved.", fg=COLORS['text_dim'])
        return
    ips.append(ip)
    save_ips(ips)
    refresh_ip_listbox()
    status_label.config(text=f"✅ IP {ip} saved!", fg=COLORS['success'])

def remove_selected_ip():
    sel = ip_listbox.curselection()
    if not sel:
        status_label.config(text="⚠️ Select an IP to remove.", fg=COLORS['highlight'])
        return
    idx = sel[0]
    ips = load_ips()
    try:
        removed = ips.pop(idx)
        save_ips(ips)
        refresh_ip_listbox()
        status_label.config(text=f"🗑️ IP removed.", fg=COLORS['text_dim'])
    except Exception:
        pass

def use_selected_ip(event=None):
    sel = ip_listbox.curselection()
    if not sel:
        return
    ip_text = ip_listbox.get(sel[0])
    ip = ip_text.replace("📡", "").strip()
    ip_entry.delete(0, tk.END)
    ip_entry.insert(0, ip)
    status_label.config(text=f"✅ IP loaded: {ip}", fg=COLORS['success'])


# ---------------- Hover Effects ----------------
def on_enter(e):
    e.widget.config(bg=COLORS['highlight'], fg='white')

def on_leave(e, original_bg):
    e.widget.config(bg=original_bg, fg=COLORS['text'])

# ---------------- GUI ----------------
root = tk.Tk()
root.title("OTA Uploader")
root.geometry("520x580")
root.resizable(False, False)
root.configure(bg=COLORS['bg'])

# Main container
main_frame = tk.Frame(root, bg=COLORS['bg'], padx=30, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# Header
header_frame = tk.Frame(main_frame, bg=COLORS['bg'])
header_frame.pack(fill=tk.X, pady=(0, 20))

title_label = tk.Label(header_frame, text="⚡ OTA Uploader", 
                       font=('Segoe UI', 18, 'bold'), bg=COLORS['bg'], fg=COLORS['text'])
title_label.pack()

subtitle = tk.Label(header_frame, text="Upload firmware wirelessly", 
                    font=('Segoe UI', 10), bg=COLORS['bg'], fg=COLORS['text_dim'])
subtitle.pack(pady=(5, 0))

# Card: Connection Settings
conn_card = tk.Frame(main_frame, bg=COLORS['card'], padx=20, pady=15)
conn_card.pack(fill=tk.X, pady=(0, 15))

conn_title = tk.Label(conn_card, text="🔌 Connection Settings", 
                      font=('Segoe UI', 11, 'bold'), bg=COLORS['card'], fg=COLORS['text'])
conn_title.pack(anchor=tk.W, pady=(0, 10))

# IP Entry
ip_row = tk.Frame(conn_card, bg=COLORS['card'])
ip_row.pack(fill=tk.X, pady=(0, 10))

ip_label = tk.Label(ip_row, text="ESP32 IP Address:", font=('Segoe UI', 10), 
                    bg=COLORS['card'], fg=COLORS['text_dim'])
ip_label.pack(anchor=tk.W)

ip_entry = tk.Entry(ip_row, font=('Consolas', 11), bg=COLORS['entry_bg'], fg=COLORS['text'],
                    insertbackground=COLORS['text'], relief=tk.FLAT, width=35)
ip_entry.pack(fill=tk.X, pady=(5, 0), ipady=8)

# Firmware Entry
fw_row = tk.Frame(conn_card, bg=COLORS['card'])
fw_row.pack(fill=tk.X)

fw_label = tk.Label(fw_row, text="Firmware File (.bin):", font=('Segoe UI', 10), 
                    bg=COLORS['card'], fg=COLORS['text_dim'])
fw_label.pack(anchor=tk.W)

fw_input_row = tk.Frame(fw_row, bg=COLORS['card'])
fw_input_row.pack(fill=tk.X, pady=(5, 0))

file_entry = tk.Entry(fw_input_row, font=('Consolas', 10), bg=COLORS['entry_bg'], fg=COLORS['text'],
                      insertbackground=COLORS['text'], relief=tk.FLAT, width=28)
file_entry.pack(side=tk.LEFT, ipady=8, expand=True, fill=tk.X)

def browse_file():
    path = filedialog.askopenfilename(filetypes=[("Binary files", "*.bin")])
    if path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, path)
        status_label.config(text=f"📁 File selected", fg=COLORS['success'])

browse_btn = tk.Button(fw_input_row, text="📂 Browse", font=('Segoe UI', 9), 
                       bg=COLORS['accent'], fg=COLORS['text'], relief=tk.FLAT,
                       cursor='hand2', padx=15, pady=6, command=browse_file)
browse_btn.pack(side=tk.RIGHT, padx=(10, 0))
browse_btn.bind('<Enter>', on_enter)
browse_btn.bind('<Leave>', lambda e: on_leave(e, COLORS['accent']))

# Card: Saved IPs
ips_card = tk.Frame(main_frame, bg=COLORS['card'], padx=20, pady=15)
ips_card.pack(fill=tk.X, pady=(0, 15))

ips_title = tk.Label(ips_card, text="📋 Saved IP Addresses", 
                     font=('Segoe UI', 11, 'bold'), bg=COLORS['card'], fg=COLORS['text'])
ips_title.pack(anchor=tk.W, pady=(0, 10))

# Listbox with scrollbar
list_container = tk.Frame(ips_card, bg=COLORS['card'])
list_container.pack(fill=tk.X)

ip_listbox = tk.Listbox(list_container, height=4, font=('Segoe UI', 10), 
                        bg=COLORS['listbox_bg'], fg=COLORS['text'],
                        selectbackground=COLORS['highlight'], selectforeground='white',
                        relief=tk.FLAT, highlightthickness=0, activestyle='none')
ip_listbox.pack(side=tk.LEFT, fill=tk.X, expand=True)

scrollbar = tk.Scrollbar(list_container, orient=tk.VERTICAL, command=ip_listbox.yview,
                         bg=COLORS['accent'], troughcolor=COLORS['card'])
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
ip_listbox.config(yscrollcommand=scrollbar.set)
ip_listbox.bind('<Double-1>', use_selected_ip)

# IP action buttons
ip_btn_row = tk.Frame(ips_card, bg=COLORS['card'])
ip_btn_row.pack(fill=tk.X, pady=(10, 0))

save_ip_btn = tk.Button(ip_btn_row, text="💾 Save IP", font=('Segoe UI', 9),
                        bg=COLORS['accent'], fg=COLORS['text'], relief=tk.FLAT,
                        cursor='hand2', padx=12, pady=5, command=save_current_ip)
save_ip_btn.pack(side=tk.LEFT, padx=(0, 8))
save_ip_btn.bind('<Enter>', on_enter)
save_ip_btn.bind('<Leave>', lambda e: on_leave(e, COLORS['accent']))

use_ip_btn = tk.Button(ip_btn_row, text="✅ Use Selected", font=('Segoe UI', 9),
                       bg=COLORS['accent'], fg=COLORS['text'], relief=tk.FLAT,
                       cursor='hand2', padx=12, pady=5, command=use_selected_ip)
use_ip_btn.pack(side=tk.LEFT, padx=(0, 8))
use_ip_btn.bind('<Enter>', on_enter)
use_ip_btn.bind('<Leave>', lambda e: on_leave(e, COLORS['accent']))

remove_ip_btn = tk.Button(ip_btn_row, text="🗑️ Remove", font=('Segoe UI', 9),
                          bg=COLORS['accent'], fg=COLORS['text'], relief=tk.FLAT,
                          cursor='hand2', padx=12, pady=5, command=remove_selected_ip)
remove_ip_btn.pack(side=tk.LEFT)
remove_ip_btn.bind('<Enter>', on_enter)
remove_ip_btn.bind('<Leave>', lambda e: on_leave(e, COLORS['accent']))

# Upload Button
upload_btn = tk.Button(main_frame, text="🚀 Upload Firmware", font=('Segoe UI', 12, 'bold'),
                       bg=COLORS['highlight'], fg='white', relief=tk.FLAT, borderwidth=2,
                       highlightbackground=COLORS['highlight'], highlightthickness=1,
                       cursor='hand2', padx=30, pady=30, command=upload_firmware)
upload_btn.pack(pady=(5, 5))
upload_btn.bind('<Enter>', lambda e: e.widget.config(bg='#ff6b6b', highlightbackground='#ff6b6b'))
upload_btn.bind('<Leave>', lambda e: e.widget.config(bg=COLORS['highlight'], highlightbackground=COLORS['highlight']))

# Progress bar (hidden initially)
progress_bar = ttk.Progressbar(main_frame, mode='indeterminate', length=300)

# Status bar
status_frame = tk.Frame(main_frame, bg=COLORS['accent'], padx=15, pady=10)
status_frame.pack(fill=tk.X)

status_label = tk.Label(status_frame, text="Ready to upload firmware.", 
                        font=('Segoe UI', 9), bg=COLORS['accent'], fg=COLORS['text_dim'])
status_label.pack()

# Initialize
refresh_ip_listbox()

root.mainloop()