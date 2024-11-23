import json
import tkinter as tk
from tkinter import ttk, Menu
from typing import Optional, TypedDict, Dict

# Définition des types basés sur le fichier TypeScript
class Vo(TypedDict, total=False):
    main: Optional[str]

class Female(TypedDict, total=False):
    text: Optional[str]
    vo: Optional[Vo]

class Dialogue(TypedDict):
    id: str
    female: Optional[Female]
    _path: str

def open_and_display_json():
    try:
        file_path = r"D:\_CyberPunk-Creation\BDDDialogues\test.json"
        with open(file_path, "r", encoding="utf-8") as file:
            data: Dict[str, Dialogue] = json.load(file)  # Charger les données avec typage

        for item in tree.get_children():
            tree.delete(item)

        for key, value in data.items():
            female_text = value.get('female', {}).get('text', 'N/A')
            vo_path = value.get('female', {}).get('vo', {}).get('main', 'N/A')
            path = value.get('_path', 'N/A')

            path_parts = path.split("/")
            segment_1 = path_parts[0] if len(path_parts) > 0 else "N/A"
            segment_2 = path_parts[1] if len(path_parts) > 1 else "N/A"
            segment_3 = path_parts[2] if len(path_parts) > 2 else "N/A"
            segment_4 = path_parts[3] if len(path_parts) > 3 else "N/A"

            tree.insert("", tk.END, values=(key, female_text, vo_path, segment_1, segment_2, segment_3, segment_4))

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{file_path}' est introuvable.")
    except json.JSONDecodeError:
        print(f"Erreur : Le fichier '{file_path}' contient une erreur JSON.")
    except Exception as e:
        print(f"Une erreur inattendue s'est produite : {e}")

def copy_selected():
    try:
        selected_item = tree.selection()[0]
        selected_values = tree.item(selected_item, 'values')

        root.clipboard_clear()
        root.clipboard_append('\t'.join(selected_values))
        root.update()
    except IndexError:
        pass

def copy_cell(event):
    try:
        region = tree.identify("region", event.x, event.y)
        if region == "cell":
            row_id = tree.identify_row(event.y)
            column_id = tree.identify_column(event.x)
            
            col_index = int(column_id.replace("#", "")) - 1
            selected_value = tree.item(row_id)["values"][col_index]

            root.clipboard_clear()
            root.clipboard_append(selected_value)
            root.update()
    except IndexError:
        pass

def display_info(event):
    try:
        selected_item = tree.selection()[0]
        selected_values = tree.item(selected_item, 'values')

        for widget in info_frame.winfo_children():
            widget.destroy()

        labels = ["ID", "Text", "Vo Path", "Path Segment 1", "Path Segment 2", "Path Segment 3", "Path Segment 4"]
        for i, value in enumerate(selected_values):
            text = tk.Text(info_frame, height=1, wrap="none", borderwidth=0)
            text.insert("1.0", f"{labels[i]}: {value}")
            text.config(state="disabled")
            text.pack(fill="x", padx=5, pady=2)
    except IndexError:
        pass

root = tk.Tk()
root.title("Visualisateur de JSON en tableau avec copier-coller et panneau d'informations")
root.geometry("1200x600")

columns = ("ID", "Text", "Vo Path", "Path Segment 1", "Path Segment 2", "Path Segment 3", "Path Segment 4")
tree = ttk.Treeview(root, columns=columns, show="headings", height=20)

for column in columns:
    tree.heading(column, text=column)

for column in columns:
    tree.column(column, width=150, anchor="w")

scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

tree.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.BOTH, expand=True)

info_frame = tk.Frame(root, width=300, relief=tk.RAISED, borderwidth=1)
info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

open_and_display_json()

menu = Menu(root, tearoff=0)
menu.add_command(label="Copier la ligne", command=copy_selected)

def show_context_menu(event):
    menu.post(event.x_root, event.y_root)

tree.bind("<Button-3>", show_context_menu)
tree.bind("<Double-1>", copy_cell)
tree.bind("<<TreeviewSelect>>", display_info)

root.mainloop()
