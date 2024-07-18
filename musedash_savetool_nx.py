import tkinter as tk
from tkinter import filedialog, messagebox
import json
import re

def unlock_all_master_charts(data):
    if 'Account' in data:
        account_data = json.loads(data['Account'])
        account_data['IsUnlockAllMaster'] = True
        data['Account'] = json.dumps(account_data, separators=(',', ':'))
    return data

def unlock_just_as_planned(data):
    if 'IAP' in data:
        iap_data = json.loads(data['IAP'])
        for key in iap_data.keys():
            if key.startswith("music_package_"):
                iap_data[key] = True
        data['IAP'] = json.dumps(iap_data, separators=(',', ':'))
    return data

def set_exp_to_lv100(data):
    if 'Account' in data:
        account_data = json.loads(data['Account'])
        account_data['Exp'] = 9999
        data['Account'] = json.dumps(account_data, separators=(',', ':'))
    return data

def modify_save_file(data):
    data = unlock_all_master_charts(data)
    data = unlock_just_as_planned(data)
    data = set_exp_to_lv100(data)
    return data

def load_file():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    with open(file_path, 'rb') as file:
        file_contents = file.read()

    json_pattern = re.compile(b'({.*})')
    json_match = json_pattern.search(file_contents)
    if not json_match:
        messagebox.showerror("Error", "No JSON data found in the file.")
        return

    json_data = json.loads(json_match.group().decode('utf-8'))
    modified_data = modify_save_file(json_data)

    modified_json_bytes = json.dumps(modified_data, separators=(',', ':')).encode('utf-8')
    modified_file_contents = file_contents[:json_match.start()] + modified_json_bytes + file_contents[json_match.end():]
    modified_file_contents = modified_file_contents.ljust(524288, b'\x00')[:524288]

    save_path = filedialog.asksaveasfilename(defaultextension=".dat")
    if not save_path:
        return
    with open(save_path, 'wb') as file:
        file.write(modified_file_contents)
    
    messagebox.showinfo("Success", "Save file modified successfully!")

def create_gui():
    root = tk.Tk()
    root.title("Save File Modifier")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    btn_load = tk.Button(frame, text="Load Save File", command=load_file)
    btn_load.pack(pady=5)

    root.mainloop()

create_gui()
