import tkinter as tk
from tkinter import filedialog, messagebox
import requests

def upload_firmware():
    ip = ip_entry.get().strip()
    file_path = file_entry.get().strip()

    if not ip or not file_path:
        messagebox.showerror("Error", "Enter ESP32 IP and select firmware file.")
        return

    url = f"http://{ip}/update"

    try:
        with open(file_path, "rb") as f:
            files = {"file": f}
            r = requests.post(url, files=files, timeout=60)

        if r.status_code == 200:
            messagebox.showinfo("Success", "Firmware uploaded successfully.\nESP32 is rebooting.")
        else:
            messagebox.showerror("Failed", f"Upload failed.\nStatus: {r.status_code}")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------------- GUI ----------------
root = tk.Tk()
root.title("ESP32 OTA Uploader")

tk.Label(root, text="ESP32 IP Address").grid(row=0, column=0, padx=5, pady=5)
ip_entry = tk.Entry(root, width=25)
ip_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Firmware (.bin)").grid(row=1, column=0, padx=5, pady=5)
file_entry = tk.Entry(root, width=25)
file_entry.grid(row=1, column=1, padx=5, pady=5)

def browse_file():
    path = filedialog.askopenfilename(filetypes=[("Binary files", "*.bin")])
    if path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, path)

tk.Button(root, text="Browse", command=browse_file).grid(row=1, column=2, padx=5)

tk.Button(root, text="Upload Firmware", command=upload_firmware,
          width=25).grid(row=2, column=0, columnspan=3, pady=10)

root.mainloop()
