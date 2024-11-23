# fichier: main.py
import tkinter as tk
from tkinter import ttk
from gui_functions import open_and_display_json, apply_filters_to_tree, add_to_playlist, save_playlist_to_file
from data_loader import load_json

# Créer la fenêtre principale
root = tk.Tk()
root.title("Visualisateur de JSON et Playlist")
root.geometry("1500x800")
root.minsize(1100, 800)

# Variables globales pour les données
data = {}
file_path = r"D:\_CyberPunk-Creation\BDDDialogues\test.json"

# Frame principale
main_frame = tk.Frame(root)
main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Colonnes
columns = ["ID", "Sous-titres", "Origine A", "Audio", "Origine Q", "Quête"]

# Tableau principal
tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)
for column in columns:
    tree.heading(column, text=column)
    tree.column(column, width=150, anchor="w")
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Charger les données initiales
data = open_and_display_json(tree, file_path)

# Ajout des filtres
filter_frame = tk.Frame(root)
filter_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
filters = []

def create_filters():
    global filters
    for i, column in enumerate(columns):
        label = tk.Label(filter_frame, text=f"Filtre {column}")
        label.grid(row=0, column=i, padx=5)
        entry = tk.Entry(filter_frame)
        entry.grid(row=1, column=i, padx=5)
        filters.append(entry)

    filter_button = tk.Button(filter_frame, text="Appliquer", command=lambda: apply_filters_to_tree(
        tree=tree,
        data=data,
        filters=[entry.get() for entry in filters],
        columns=columns
    ))
    filter_button.grid(row=1, column=len(columns), padx=5)

    reset_button = tk.Button(filter_frame, text="Réinitialiser", command=lambda: open_and_display_json(tree, file_path))
    reset_button.grid(row=1, column=len(columns) + 1, padx=5)

create_filters()

# Frame pour la playlist
playlist_frame = tk.Frame(root)
playlist_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Tableau de playlist
playlist_columns = columns
playlist_tree = ttk.Treeview(playlist_frame, columns=playlist_columns, show="headings", height=10)
for column in playlist_columns:
    playlist_tree.heading(column, text=column)
    playlist_tree.column(column, width=150, anchor="w")
playlist_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Boutons pour la playlist
playlist_buttons_frame = tk.Frame(playlist_frame)
playlist_buttons_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)

add_button = tk.Button(playlist_buttons_frame, text="Ajouter à la Playlist", command=lambda: add_to_playlist(tree, playlist_tree))
add_button.pack(side=tk.TOP, pady=5)

save_button = tk.Button(playlist_buttons_frame, text="Sauvegarder la Playlist", command=lambda: save_playlist_to_file(playlist_tree))
save_button.pack(side=tk.TOP, pady=5)

clear_button = tk.Button(playlist_buttons_frame, text="Effacer la Playlist", command=lambda: clear_playlist(playlist_tree))
clear_button.pack(side=tk.TOP, pady=5)

# Lancer la boucle principale
root.mainloop()
