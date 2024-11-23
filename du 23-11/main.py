# fichier: main.py
import tkinter as tk
from tkinter import ttk, filedialog
import json
from gui_functions import open_and_display_json, add_to_playlist, move_up_playlist, move_down_playlist, save_playlist_to_file, clear_playlist, copy_cell, display_info

# Fonction pour charger les données JSON
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Fonction pour sauvegarder la playlist en JSON
def save_playlist_to_json(playlist_tree):
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        playlist_data = []
        for child in playlist_tree.get_children():
            values = playlist_tree.item(child, "values")
            playlist_data.append({
                "ID": values[0],
                "Sous-titres": values[1],
                "Origine": values[2],
                "Audio": values[3],
                "Origine 2": values[4],
                "Quête": values[5]
            })
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(playlist_data, file, ensure_ascii=False, indent=4)

# Fonction principale
if __name__ == "__main__":
    # Initialiser la fenêtre principale
    root = tk.Tk()
    root.title("Gestionnaire de Dialogues")
    root.geometry("1200x800")

    # Définir le chemin du fichier JSON (à modifier selon vos besoins)
    file_path = r"D:\_CyberPunk-Creation\BDDDialogues\testReduit.json"

    # Créer la zone des filtres
    filter_frame = tk.Frame(root)
    filter_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

    columns = ["ID", "Sous-titres", "Origine ", "Audio", "Origine", "Quête Q"]
    filters = []
    for i, column in enumerate(columns):
        label = tk.Label(filter_frame, text=f"Filtre {column}")
        label.grid(row=0, column=i, padx=5)
        entry = tk.Entry(filter_frame)
        entry.grid(row=1, column=i, padx=5)
        filters.append(entry)

    def apply_filters():
        for item in tree.get_children():
            tree.delete(item)

        data = load_json(file_path)
        for key, value in data.items():
            sous_titres = value.get('female', {}).get('text', 'N/A')
            vo_path = value.get('female', {}).get('vo', {}).get('main', 'N/A')
            if '{}' in vo_path:
                vo_path = vo_path.split('{}', 1)[-1]
            path = value.get('_path', 'N/A')

            # Découper le chemin en "Origine" et "Quête"
            path_parts = path.split('/', 1)
            origine_2 = path_parts[0] if len(path_parts) > 0 else 'N/A'
            quete = path_parts[1].split('{}', 1)[-1] if len(path_parts) > 1 else 'N/A'

            # Appliquer les filtres
            match = True
            for i, entry in enumerate(filters):
                if entry.get() and entry.get().lower() not in str((key, sous_titres, origine_2, vo_path, origine_2, quete)[i]).lower():
                    match = False
                    break

            if match:
                item_id = tree.insert("", tk.END, values=(key, sous_titres, origine_2, vo_path, origine_2, quete))
                if vo_path == "N/A":
                    tree.item(item_id, tags=('na_audio',))

    filter_button = tk.Button(filter_frame, text="Appliquer les filtres", command=apply_filters)
    filter_button.grid(row=1, column=len(columns), padx=5)

    reset_filter_button = tk.Button(filter_frame, text="Réinitialiser les filtres", command=lambda: reset_filters(tree, filters, file_path))
    reset_filter_button.grid(row=1, column=len(columns) + 1, padx=5)

    # Créer le tableau principal des dialogues
    main_frame = tk.Frame(root)
    main_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10)

    tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=150, anchor="w")

    scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Charger les données initiales dans le tableau principal
    open_and_display_json(tree, file_path)

    # Créer la zone des boutons de gestion de la playlist
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

    add_button = tk.Button(button_frame, text="Ajouter à la playlist", command=lambda: add_to_playlist(tree, playlist_tree))
    add_button.pack(side=tk.LEFT, padx=5)

    move_up_button = tk.Button(button_frame, text="Monter", command=lambda: move_up_playlist(playlist_tree))
    move_up_button.pack(side=tk.LEFT, padx=5)

    move_down_button = tk.Button(button_frame, text="Descendre", command=lambda: move_down_playlist(playlist_tree))
    move_down_button.pack(side=tk.LEFT, padx=5)

    save_button = tk.Button(button_frame, text="Sauvegarder la playlist", command=lambda: save_playlist_to_file(playlist_tree))
    save_button.pack(side=tk.LEFT, padx=5)

    save_json_button = tk.Button(button_frame, text="Sauvegarder la playlist en JSON", command=lambda: save_playlist_to_json(playlist_tree))
    save_json_button.pack(side=tk.LEFT, padx=5)

    clear_button = tk.Button(button_frame, text="Effacer la playlist", command=lambda: clear_playlist(playlist_tree))
    clear_button.pack(side=tk.LEFT, padx=5)

    # Créer le tableau de la playlist
    playlist_frame = tk.Frame(root, height=200, bg='lightgray')
    playlist_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10)

    playlist_columns = ("ID", "Sous-titres", "Origine", "Audio", "Origine", "Quête")
    playlist_tree = ttk.Treeview(playlist_frame, columns=playlist_columns, show="headings", height=10)

    for column in playlist_columns:
        playlist_tree.heading(column, text=column)
        playlist_tree.column(column, width=150, anchor="w")

    playlist_scrollbar = ttk.Scrollbar(playlist_frame, orient=tk.VERTICAL, command=playlist_tree.yview)
    playlist_tree.configure(yscroll=playlist_scrollbar.set)
    playlist_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    playlist_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Lancer l'application
    root.mainloop()

# Fonction pour réinitialiser les filtres et restaurer toutes les lignes
def reset_filters(tree, filters, file_path):
    for entry in filters:
        entry.delete(0, tk.END)
    open_and_display_json(tree, file_path)
