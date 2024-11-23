# fichier: gui_functions.py
import tkinter as tk
from tkinter import ttk, filedialog
from typing import Dict
from custom_types import Dialogue
from data_loader import load_json

# Fonction pour afficher les données dans le tableau
def open_and_display_json(tree, file_path: str):
    data: Dict[str, Dialogue] = load_json(file_path)

    for item in tree.get_children():
        tree.delete(item)

    if len(tree.get_children()) > 0:
        tree.selection_set(tree.get_children()[0])

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

        # Insérer la ligne dans le tableau
        item_id = tree.insert("", tk.END, values=(key, sous_titres, origine_2, vo_path, origine_2, quete))

        # Colorer en rouge le fond des lignes qui ont "N/A" dans la colonne Audio
        if vo_path == "N/A":
            tree.item(item_id, tags=('na_audio',))

    # Configurer le style pour colorer les lignes avec tag 'na_audio'
    tree.tag_configure('na_audio', background='red')

# Fonction pour ajouter les filtres et les boutons de contrôle au-dessus du premier tableau
def add_filters(frame, tree):
    filter_frame = tk.Frame(frame)
    filter_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

    columns = ["ID", "Sous-titres", "Origine", "Audio", "Origine", "Quête"]
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

        data: Dict[str, Dialogue] = load_json(file_path)
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

    reset_filter_button = tk.Button(filter_frame, text="Réinitialiser les filtres", command=lambda: reset_filters(tree, filters))
    reset_filter_button.grid(row=1, column=len(columns) + 1, padx=5)

# Fonction pour réinitialiser les filtres et restaurer toutes les lignes
def reset_filters(tree, filters):
    for entry in filters:
        entry.delete(0, tk.END)
    open_and_display_json(tree, file_path)

# Fonction pour copier une ligne sélectionnée
def copy_selected(tree, root):
    try:
        selected_item = tree.selection()[0]
        selected_values = tree.item(selected_item, 'values')

        root.clipboard_clear()
        root.clipboard_append('\t'.join(selected_values))
        root.update()
    except IndexError:
        pass

# Fonction pour copier une cellule
def copy_cell(event, tree, root):
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

# Fonction pour afficher les informations de la ligne sélectionnée
def display_info(event, tree, info_frame):
    info_frame.config(width=400)
    info_frame.pack_propagate(False)
    try:
        selected_item = tree.selection()[0]
        selected_values = tree.item(selected_item, 'values')

        for widget in info_frame.winfo_children():
            widget.destroy()

        labels = ["ID", "Sous-titres", "Origine", "Audio", "Origine", "Quête"]
        for i, value in enumerate(selected_values):
            text = tk.Text(info_frame, height=1, wrap="none", borderwidth=0)
            text.insert("1.0", f"{labels[i]}: {value}")
            text.config(state="disabled")
            text.pack(fill="x", padx=5, pady=2)
    except IndexError:
        pass

# Fonction pour ajouter une ligne sélectionnée au deuxième tableau
def add_to_playlist(tree, playlist_tree):
    try:
        selected_item = tree.selection()[0]
        selected_values = tree.item(selected_item, 'values')
        playlist_tree.insert("", tk.END, values=selected_values)
    except IndexError:
        pass

# Fonction pour ajouter une ligne au deuxième tableau via un clic droit
def add_to_playlist_context_menu(event, tree, playlist_tree):
    try:
        selected_item = tree.selection()[0]
        selected_values = tree.item(selected_item, 'values')
        playlist_tree.insert("", tk.END, values=selected_values)
    except IndexError:
        pass

# Fonction pour déplacer une ligne vers le haut dans le tableau de playlist
def move_up_playlist(playlist_tree):
    try:
        selected_item = playlist_tree.selection()[0]
        index = playlist_tree.index(selected_item)
        if index > 0:
            playlist_tree.move(selected_item, playlist_tree.parent(selected_item), index - 1)
    except IndexError:
        pass

# Fonction pour déplacer une ligne vers le bas dans le tableau de playlist
def move_down_playlist(playlist_tree):
    try:
        selected_item = playlist_tree.selection()[0]
        index = playlist_tree.index(selected_item)
        if index < len(playlist_tree.get_children()) - 1:
            playlist_tree.move(selected_item, playlist_tree.parent(selected_item), index + 1)
    except IndexError:
        pass

# Fonction pour sauvegarder la playlist dans un fichier texte
def save_playlist_to_file(playlist_tree):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            for child in playlist_tree.get_children():
                values = playlist_tree.item(child, "values")
                file.write("\t".join(values) + "\n")

# Fonction pour effacer le tableau de playlist
def clear_playlist(playlist_tree):
    for item in playlist_tree.get_children():
        playlist_tree.delete(item)

# Fonction pour supprimer une ligne de la playlist via un clic droit
def remove_selected_from_playlist(event, playlist_tree):
    try:
        selected_item = playlist_tree.selection()[0]
        playlist_tree.delete(selected_item)
    except IndexError:
        pass

# Fonction pour configurer le tableau de playlist
def setup_playlist(root, tree):
    main_frame = tk.Frame(root)
    main_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=10, pady=10)

    button_frame = tk.Frame(main_frame)
    button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

    playlist_frame = tk.Frame(main_frame, height=450, bg='lightgray')
    playlist_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

    playlist_columns = ("ID", "Sous-titres", "Origine", "Audio", "Origine", "Quête")
    playlist_tree = ttk.Treeview(playlist_frame, columns=playlist_columns, show="headings", height=10)

    for column in playlist_columns:
        playlist_tree.heading(column, text=column)
        playlist_tree.column(column, width=150, anchor="w")

    playlist_scrollbar = ttk.Scrollbar(playlist_frame, orient=tk.VERTICAL, command=playlist_tree.yview)
    playlist_tree.configure(yscroll=playlist_scrollbar.set)
    playlist_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    playlist_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Ajouter le clic droit pour supprimer une ligne dans la playlist
    playlist_tree.bind("<Button-3>", lambda event: remove_selected_from_playlist(event, playlist_tree))

    add_button = tk.Button(button_frame, text="Ajouter à la playlist", command=lambda: add_to_playlist(tree, playlist_tree))
    add_button.pack(side=tk.LEFT, padx=5)

    move_up_button = tk.Button(button_frame, text="Monter", command=lambda: move_up_playlist(playlist_tree))
    move_up_button.pack(side=tk.LEFT, padx=5)

    move_down_button = tk.Button(button_frame, text="Descendre", command=lambda: move_down_playlist(playlist_tree))
    move_down_button.pack(side=tk.LEFT, padx=5)

    save_button = tk.Button(button_frame, text="Sauvegarder la playlist", command=lambda: save_playlist_to_file(playlist_tree))
    save_button.pack(side=tk.LEFT, padx=5)

    clear_button = tk.Button(button_frame, text="Effacer la playlist", command=lambda: clear_playlist(playlist_tree))
    clear_button.pack(side=tk.LEFT, padx=5)

    return playlist_tree
