import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import requests
import json
import os
import threading
import socket
import hashlib
from datetime import datetime

# ============= CONFIGURATION & CONSTANTS =============
IPS_FILE = os.path.join(os.path.dirname(__file__), "ips.json")
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "upload_history.json")
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "app_config.json")
VERSION_CACHE_FILE = os.path.join(os.path.dirname(__file__), "device_versions.json")

# Color schemes
THEMES = {
    'dark': {
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
    },
    'light': {
        'bg': '#f5f5f5',
        'card': '#ffffff',
        'accent': '#3498db',
        'highlight': '#e74c3c',
        'text': '#2c3e50',
        'text_dim': '#7f8c8d',
        'success': '#27ae60',
        'entry_bg': '#ecf0f1',
        'listbox_bg': '#ecf0f1',
        'button_hover': '#e67e22',
    }
}

# ============= UTILITY FUNCTIONS =============
def load_config():
    """Load app configuration."""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {'theme': 'dark', 'verify_checksum': True}

def save_config(config):
    """Save app configuration."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
    except Exception:
        pass

def calculate_checksum(file_path):
    """Calculate SHA256 checksum of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def load_device_versions():
    """Load cached device versions."""
    try:
        if os.path.exists(VERSION_CACHE_FILE):
            with open(VERSION_CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def save_device_versions(versions):
    """Save device versions cache."""
    try:
        with open(VERSION_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(versions, f, indent=2)
    except Exception:
        pass

def load_history():
    """Load upload history."""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
    except Exception:
        pass
    return []

def save_history(history):
    """Save upload history."""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
    except Exception:
        pass

def log_upload(ip, status, file_name, error=None, checksum=None):
    """Log an upload attempt."""
    history = load_history()
    entry = {
        'timestamp': datetime.now().isoformat(),
        'ip': ip,
        'status': status,
        'file': file_name,
        'checksum': checksum,
        'error': error
    }
    history.append(entry)
    save_history(history)

def check_device_online(ip):
    """Check if device is online via status endpoint."""
    try:
        r = requests.get(f"http://{ip}/status", timeout=3)
        return r.status_code == 200
    except Exception:
        return False

def get_device_info(ip):
    """Get device info (version, name, etc.)."""
    try:
        r = requests.get(f"http://{ip}/info", timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

def scan_network_for_devices():
    """Scan local network for ESP32 devices."""
    devices = []
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        base_ip = ".".join(local_ip.split(".")[:-1])
        
        for i in range(1, 255):
            ip = f"{base_ip}.{i}"
            if check_device_online(ip):
                info = get_device_info(ip)
                devices.append({'ip': ip, 'info': info})
    except Exception:
        pass
    return devices

def update_status(text, color):
    """Update status label."""
    status_label.config(text=text, fg=color)
    root.update()

# ============= UPLOAD & CORE FUNCTIONS =============
def upload_firmware():
    """Upload firmware to ESP32."""
    ip = ip_entry.get().strip()
    file_path = file_entry.get().strip()

    if not ip or not file_path:
        update_status("⚠️ Enter ESP32 IP and select firmware file.", COLORS['highlight'])
        return

    if not os.path.exists(file_path):
        update_status("❌ Firmware file not found.", COLORS['highlight'])
        return

    upload_btn.config(state=tk.DISABLED, text="⏳ Uploading...", bg='#666')
    progress_bar.pack(pady=(5, 0))
    progress_bar.start(10)
    update_status("⏳ Uploading firmware...", COLORS['text'])
    root.update()

    thread = threading.Thread(target=_upload_firmware_thread, args=(ip, file_path))
    thread.daemon = True
    thread.start()

def _upload_firmware_thread(ip, file_path):
    """Thread function for uploading firmware."""
    url = f"http://{ip}/update"
    file_name = os.path.basename(file_path)
    checksum = None
    
    try:
        if app_config.get('verify_checksum', True):
            update_status("📊 Calculating checksum...", COLORS['text'])
            checksum = calculate_checksum(file_path)
        
        if not check_device_online(ip):
            raise Exception("Device is offline")

        with open(file_path, "rb") as f:
            files = {"file": f}
            r = requests.post(url, files=files, timeout=120)

        if r.status_code == 200:
            update_status("✅ Firmware uploaded! ESP32 rebooting...", COLORS['success'])
            log_upload(ip, "success", file_name, checksum=checksum)
        else:
            error_msg = f"Status: {r.status_code}"
            update_status(f"❌ Upload failed. {error_msg}", COLORS['highlight'])
            log_upload(ip, "failed", file_name, error=error_msg)

    except Exception as e:
        error_msg = str(e)[:50]
        update_status(f"❌ Error: {error_msg}", COLORS['highlight'])
        log_upload(ip, "failed", file_name, error=error_msg)

    finally:
        upload_btn.config(state=tk.NORMAL, text="🚀 Upload Firmware", bg=COLORS['highlight'])
        progress_bar.stop()
        progress_bar.pack_forget()
        root.update()

def refresh_ip_tree():
    """Refresh IP Treeview."""
    ips = load_ips()
    for i in ip_tree.get_children():
        ip_tree.delete(i)
    versions = load_device_versions()
    for ip in ips:
        ver = versions.get(ip, {}).get('version', '')
        ip_tree.insert('', 'end', values=(ip, ver))

def save_current_ip():
    """Save current IP to list."""
    ip = ip_entry.get().strip()
    if not ip:
        update_status("⚠️ Enter an IP to save.", COLORS['highlight'])
        return
    ips = load_ips()
    if ip in ips:
        update_status("ℹ️ IP already saved.", COLORS['text_dim'])
        return
    ips.append(ip)
    save_ips(ips)
    refresh_ip_tree()
    update_status(f"✅ IP {ip} saved!", COLORS['success'])

def remove_selected_ip():
    """Remove selected IP."""
    selection = ip_tree.selection()
    if not selection:
        update_status("⚠️ Select an IP to remove.", COLORS['highlight'])
        return
    item = selection[0]
    ip = ip_tree.item(item, 'values')[0]
    ips = load_ips()
    try:
        ips.remove(ip)
        save_ips(ips)
        refresh_ip_tree()
        update_status(f"🗑️ IP removed.", COLORS['text_dim'])
    except Exception:
        pass

def use_selected_ip(event=None):
    """Use selected IP from list."""
    selection = ip_tree.selection()
    if not selection:
        return
    item = selection[0]
    ip = ip_tree.item(item, 'values')[0]
    ip_entry.delete(0, tk.END)
    ip_entry.insert(0, ip)
    update_status(f"✅ IP loaded: {ip}", COLORS['success'])

def load_ips():
    """Load saved IPs from file."""
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
    """Save IPs to file."""
    try:
        with open(IPS_FILE, "w", encoding="utf-8") as f:
            json.dump(ips, f, indent=2)
    except Exception:
        pass

def browse_file():
    """Browse for firmware file."""
    path = filedialog.askopenfilename(filetypes=[("Binary files", "*.bin"), ("All files", "*.*")])
    if path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, path)
        update_status(f"📁 File selected", COLORS['success'])

def scan_devices_thread():
    """Scan for devices in background thread."""
    scan_btn.config(state=tk.DISABLED, text="🔍 Scanning...")
    update_status("🔍 Scanning network for ESP32 devices...", COLORS['text_dim'])
    root.update()
    
    devices = scan_network_for_devices()
    
    if devices:
        device_list = "\n".join([f"  📡 {d['ip']}" + (f" ({d['info'].get('name', 'Unknown')})" if d['info'] else "") for d in devices])
        update_status(f"✅ Found {len(devices)} device(s):\n{device_list}", COLORS['success'])
    else:
        update_status("❌ No devices found", COLORS['highlight'])
    
    scan_btn.config(state=tk.NORMAL, text="🔍 Scan Network")

def scan_devices():
    """Start network scan in separate thread."""
    thread = threading.Thread(target=scan_devices_thread)
    thread.daemon = True
    thread.start()

def check_device_version():
    """Check device firmware version."""
    ip = ip_entry.get().strip()
    if not ip:
        update_status("⚠️ Enter ESP32 IP address.", COLORS['highlight'])
        return
    
    check_btn.config(state=tk.DISABLED, text="⏳ Checking...")
    update_status("⏳ Checking device version...", COLORS['text_dim'])
    root.update()
    
    thread = threading.Thread(target=_check_version_thread, args=(ip,))
    thread.daemon = True
    thread.start()

def _check_version_thread(ip):
    """Thread function for checking version."""
    try:
        info = get_device_info(ip)
        if info:
            version = info.get('version', 'Unknown')
            name = info.get('name', 'ESP32')
            versions = load_device_versions()
            versions[ip] = {'version': version, 'name': name, 'checked': datetime.now().isoformat()}
            save_device_versions(versions)
            update_status(f"✅ {name} v{version} @ {ip}", COLORS['success'])
        else:
            update_status(f"❌ Could not connect to {ip}", COLORS['highlight'])
    except Exception as e:
        update_status(f"❌ Error: {str(e)[:50]}", COLORS['highlight'])
    finally:
        check_btn.config(state=tk.NORMAL, text="ℹ️ Check Version")

def show_upload_history():
    """Display upload history in a new window."""
    history = load_history()
    
    if not history:
        messagebox.showinfo("Upload History", "No uploads recorded yet.")
        return
    
    hist_window = tk.Toplevel(root)
    hist_window.title("📋 Upload History")
    hist_window.geometry("700x400")
    hist_window.configure(bg=COLORS['bg'])
    
    text_widget = scrolledtext.ScrolledText(hist_window, wrap=tk.WORD, bg=COLORS['card'], fg=COLORS['text'], font=('Consolas', 9))
    text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    for entry in reversed(history[-50:]):
        timestamp = entry.get('timestamp', 'Unknown')
        ip = entry.get('ip', 'Unknown')
        status = entry.get('status', 'Unknown')
        file_name = entry.get('file', 'Unknown')
        
        status_icon = "✅" if status == "success" else "❌"
        text_widget.insert(tk.END, f"{status_icon} [{timestamp}] {ip} - {file_name}\n")
    
    text_widget.config(state=tk.DISABLED)

def show_device_versions():
    """Display cached device versions."""
    versions = load_device_versions()
    
    if not versions:
        messagebox.showinfo("Device Versions", "No device versions cached yet.")
        return
    
    ver_window = tk.Toplevel(root)
    ver_window.title("ℹ️ Device Versions")
    ver_window.geometry("500x300")
    ver_window.configure(bg=COLORS['bg'])
    
    text_widget = scrolledtext.ScrolledText(ver_window, wrap=tk.WORD, bg=COLORS['card'], fg=COLORS['text'], font=('Consolas', 9))
    text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    for ip, data in versions.items():
        name = data.get('name', 'ESP32')
        version = data.get('version', 'Unknown')
        checked = data.get('checked', 'Unknown')
        text_widget.insert(tk.END, f"📡 {ip}\n   Device: {name}\n   Version: {version}\n   Checked: {checked}\n\n")
    
    text_widget.config(state=tk.DISABLED)

def toggle_theme():
    """Toggle between dark and light theme."""
    current_theme = app_config.get('theme', 'dark')
    new_theme = 'light' if current_theme == 'dark' else 'dark'
    app_config['theme'] = new_theme
    save_config(app_config)
    messagebox.showinfo("Theme", f"Theme changed to {new_theme.upper()}. Please restart the application.")

def export_config_window():
    """Export configuration."""
    save_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if save_path:
        try:
            config_data = {
                'ips': load_ips(),
                'history': load_history(),
                'versions': load_device_versions(),
                'settings': app_config
            }
            with open(save_path, "w") as f:
                json.dump(config_data, f, indent=2)
            messagebox.showinfo("Success", f"Configuration exported to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")

def import_config_window():
    """Import configuration."""
    load_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if load_path:
        try:
            with open(load_path, "r") as f:
                config_data = json.load(f)
            
            if 'ips' in config_data:
                save_ips(config_data['ips'])
            if 'history' in config_data:
                save_history(config_data['history'])
            if 'versions' in config_data:
                save_device_versions(config_data['versions'])
            if 'settings' in config_data:
                app_config.update(config_data['settings'])
                save_config(app_config)
            
            refresh_ip_listbox()
            messagebox.showinfo("Success", "Configuration imported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import: {str(e)}")

def on_enter(e):
    """Hover enter effect."""
    e.widget.config(bg=COLORS['button_hover'], fg='white')

def on_leave(e, original_bg):
    """Hover leave effect."""
    e.widget.config(bg=original_bg, fg=COLORS['text'])

# ============= MAIN GUI SETUP =============
app_config = load_config()
COLORS = THEMES[app_config.get('theme', 'dark')]

root = tk.Tk()
root.title("⚡ OTA Uploader Pro")
root.geometry("1000x700")
root.minsize(900, 600)
root.configure(bg=COLORS['bg'])

# Use ttk styles for a modern look
style = ttk.Style(root)
try:
    style.theme_use('clam')
except Exception:
    pass
style.configure('Card.TFrame', background=COLORS['card'])
style.configure('Accent.TButton', background=COLORS['accent'], foreground=COLORS['text'], borderwidth=0, focusthickness=0)
style.map('Accent.TButton', background=[('active', COLORS['button_hover'])])
style.configure('Primary.TButton', background=COLORS['highlight'], foreground='white')
style.configure('TLabel', background=COLORS['bg'], foreground=COLORS['text'])

# Layout: Sidebar (left), Main (center), Details (right)
PADDING = 16
INNER_PADDING = 12
SPACING = 8

container = tk.Frame(root, bg=COLORS['bg'])
container.pack(fill=tk.BOTH, expand=True, padx=PADDING, pady=PADDING)

sidebar = tk.Frame(container, bg=COLORS['card'], width=260)
sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, PADDING), pady=0)
sidebar.pack_propagate(False)

main_area = tk.Frame(container, bg=COLORS['bg'])
main_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, PADDING), pady=0)

details = tk.Frame(container, bg=COLORS['card'], width=260)
details.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 0), pady=0)
details.pack_propagate(False)

# Sidebar: Header + saved devices
sb_header = tk.Label(sidebar, text="Saved Devices", font=('Segoe UI', 14, 'bold'), bg=COLORS['card'], fg=COLORS['text'])
sb_header.pack(anchor='w', padx=INNER_PADDING, pady=(INNER_PADDING, SPACING))

ip_tree = ttk.Treeview(sidebar, columns=('ip','version'), show='headings', selectmode='browse', height=16)
ip_tree.heading('ip', text='IP')
ip_tree.heading('version', text='Version')
ip_tree.column('ip', width=130, anchor='w')
ip_tree.column('version', width=80, anchor='center')
ip_tree.pack(fill=tk.BOTH, expand=True, padx=INNER_PADDING, pady=(0, SPACING))
ip_tree.bind('<Double-1>', lambda e: use_selected_ip())

sb_btn_frame = tk.Frame(sidebar, bg=COLORS['card'])
sb_btn_frame.pack(fill=tk.X, padx=INNER_PADDING, pady=(0, SPACING))

ttk.Button(sb_btn_frame, text='Add IP', style='Accent.TButton', command=save_current_ip).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, SPACING//2))
ttk.Button(sb_btn_frame, text='Remove', style='Accent.TButton', command=remove_selected_ip).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(SPACING//2, 0))

ttk.Separator(sidebar, orient='horizontal').pack(fill=tk.X, padx=INNER_PADDING, pady=(SPACING, SPACING))
ttk.Button(sidebar, text='📋 History', style='Accent.TButton', command=show_upload_history).pack(fill=tk.X, padx=INNER_PADDING, pady=(0, SPACING))
ttk.Button(sidebar, text='ℹ️ Versions', style='Accent.TButton', command=show_device_versions).pack(fill=tk.X, padx=INNER_PADDING, pady=(0, SPACING))

# Main Area: Toolbar + Card for upload
toolbar = tk.Frame(main_area, bg=COLORS['bg'])
toolbar.pack(fill=tk.X, pady=(0, SPACING))

ttk.Button(toolbar, text='🔍 Scan', style='Accent.TButton', command=scan_devices).pack(side=tk.LEFT, padx=(0, SPACING))
ttk.Button(toolbar, text='🎨 Theme', style='Accent.TButton', command=toggle_theme).pack(side=tk.LEFT, padx=(0, SPACING))
ttk.Button(toolbar, text='💾 Export', style='Accent.TButton', command=export_config_window).pack(side=tk.LEFT, padx=(0, SPACING))
ttk.Button(toolbar, text='📂 Import', style='Accent.TButton', command=import_config_window).pack(side=tk.LEFT, padx=(0, 0))

card = ttk.Frame(main_area, style='Card.TFrame', padding=(INNER_PADDING, INNER_PADDING))
card.pack(fill=tk.BOTH, expand=True)

# Center all card elements
title = tk.Label(card, text='⚡ OTA Uploader', font=('Segoe UI', 16, 'bold'), bg=COLORS['card'], fg=COLORS['text'])
title.pack(anchor='center')

desc = tk.Label(card, text='Upload firmware to ESP32 devices with ease', font=('Segoe UI', 10), bg=COLORS['card'], fg=COLORS['text_dim'])
desc.pack(anchor='center', pady=(SPACING, INNER_PADDING))

form = tk.Frame(card, bg=COLORS['card'])
form.pack(anchor='center', pady=(SPACING, 0))

tk.Label(form, text='Device IP', bg=COLORS['card'], fg=COLORS['text_dim']).grid(row=0, column=0, sticky='w')
ip_entry = ttk.Entry(form, width=36)
ip_entry.grid(row=1, column=0, sticky='we', pady=(SPACING, INNER_PADDING))

tk.Label(form, text='Firmware (.bin)', bg=COLORS['card'], fg=COLORS['text_dim']).grid(row=2, column=0, sticky='w')
file_frame = tk.Frame(form, bg=COLORS['card'])
file_frame.grid(row=3, column=0, sticky='we', pady=(SPACING, INNER_PADDING))
file_entry = ttk.Entry(file_frame)
file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
ttk.Button(file_frame, text='Browse', command=browse_file).pack(side=tk.LEFT, padx=(SPACING, 0))

action_row = tk.Frame(card, bg=COLORS['card'])
action_row.pack(anchor='center', pady=(SPACING, INNER_PADDING))
scan_btn = ttk.Button(action_row, text='🔍 Scan Network', command=scan_devices)
scan_btn.pack(side=tk.LEFT)
check_btn = ttk.Button(action_row, text='ℹ️ Check Version', command=check_device_version)
check_btn.pack(side=tk.LEFT, padx=(SPACING, 0))

upload_btn = ttk.Button(card, text='🚀 Upload Firmware', style='Primary.TButton', command=upload_firmware)
upload_btn.pack(anchor='center', pady=(INNER_PADDING, SPACING))

progress_bar = ttk.Progressbar(card, mode='indeterminate')
progress_bar.pack(fill=tk.X, pady=(SPACING, 0))

# Details panel
dt_title = tk.Label(details, text='Device Details', font=('Segoe UI', 14, 'bold'), bg=COLORS['card'], fg=COLORS['text'])
dt_title.pack(anchor='w', padx=INNER_PADDING, pady=(INNER_PADDING, SPACING))

details_text = scrolledtext.ScrolledText(details, height=16, bg=COLORS['card'], fg=COLORS['text'], bd=0, font=('Consolas', 9), wrap=tk.WORD)
details_text.pack(fill=tk.BOTH, expand=True, padx=INNER_PADDING, pady=(0, INNER_PADDING))
details_text.insert(tk.END, 'Select a device or enter an IP and click "Check Version".')
details_text.config(state=tk.DISABLED)

# Status bar at bottom
status_frame = tk.Frame(root, bg=COLORS['bg'])
status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=PADDING, pady=(0, PADDING))
status_label = tk.Label(status_frame, text='Ready', bg=COLORS['bg'], fg=COLORS['text_dim'])
status_label.pack(anchor='w', padx=0, pady=(SPACING, 0))

# Populate sidebar list from saved IPs
refresh_ip_tree()

root.mainloop()
