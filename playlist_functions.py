# fichier: playlist_functions.py
import json
from tkinter import filedialog

# Fonction pour ajouter une ligne sélectionnée à la playlist
def add_to_playlist(tree, playlist_tree):
    try:
        selected_item = tree.selection()[0]
        selected_values = tree.item(selected_item, 'values')
        playlist_tree.insert("", "end", values=selected_values)
    except IndexError:
        pass

# Fonction pour déplacer une ligne vers le haut dans la playlist
def move_up_playlist(playlist_tree):
    try:
        selected_item = playlist_tree.selection()[0]
        index = playlist_tree.index(selected_item)
        if index > 0:
            playlist_tree.move(selected_item, playlist_tree.parent(selected_item), index - 1)
    except IndexError:
        pass

# Fonction pour déplacer une ligne vers le bas dans la playlist
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

# Fonction pour effacer la playlist
def clear_playlist(playlist_tree):
    for item in playlist_tree.get_children():
        playlist_tree.delete(item)
