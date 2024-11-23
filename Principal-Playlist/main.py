# fichier: main.py
import tkinter as tk
import json

from tkinter import ttk, Menu
from gui_functions import add_to_playlist, open_and_display_json, display_info, sort_tree
from playlist_functions import move_up_playlist, move_down_playlist, save_playlist_to_file, clear_playlist
from filtrage import filter_tree

from custom_types import Dialogue
from data_loader import load_json

# Créer la fenêtre principale
root = tk.Tk()
root.title("Visualisateur de JSON en tableau avec copier-coller et panneau d'informations")
root.geometry("1500x800")
root.minsize(1100, 800)

# Frame principale pour contenir le tableau principal et le panneau d'informations
main_frame = tk.Frame(root)
main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Définition des colonnes du tableau principal
#columns = ("ID", "Sous-titres", "Origine A", "Audio", "Origine Q", "Quête")
columns = ("ID", "Sous-titres", "Origine", "Audio", "Origine 2", "Quête")

# Créer la frame pour les filtres et l'ajouter au-dessus du tableau principal
filter_frame = tk.Frame(root)
filter_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

# Créer les champs de filtre pour chaque colonne
filters = []
for i, column in enumerate(columns):
    label = tk.Label(filter_frame, text=f"Filtre {column}")
    label.grid(row=0, column=i, padx=5)
    entry = tk.Entry(filter_frame)
    entry.grid(row=1, column=i, padx=5)
    filters.append(entry)

# Ajouter un bouton pour appliquer les filtres
filter_button = tk.Button(filter_frame, text="Appliquer les filtres", command=lambda: [filter_tree(tree, i, entry.get()) for i, entry in enumerate(filters)])
filter_button.grid(row=1, column=len(columns), padx=5)

# Ajouter un bouton pour réinitialiser les filtres
reset_filter_button = tk.Button(filter_frame, text="Réinitialiser les filtres", command=lambda: reset_filters(tree, filters, file_path))
reset_filter_button.grid(row=1, column=len(columns) + 1, padx=5)

# Configuration du tableau principal (tree)
tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)

# Configurer les en-têtes de colonnes avec la possibilité de trier les données
for column in columns:
    tree.heading(column, text=column, command=lambda c=column: sort_tree(tree, c, False))

# Configurer les colonnes (largeur, alignement, etc.)
for column in columns:
    if column == "ID":
        tree.column(column, width=130, minwidth=100, stretch=False, anchor="w")
    elif column == "Origine":
        tree.column(column, width=70, minwidth=200, stretch=True, anchor="w")
    elif column == "Origine 2":
        tree.column(column, width=70, minwidth=200, stretch=True, anchor="w")
    else:
        tree.column(column, width=200, anchor="w")

# Ajouter les barres de défilement au tableau principal
scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
h_scrollbar = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=tree.xview)

# Configurer le tableau pour utiliser les barres de défilement
tree.configure(yscroll=scrollbar.set, xscroll=h_scrollbar.set)

# Positionner les barres de défilement et le tableau principal dans la frame principale
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
tree.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.BOTH, expand=True)

# Panneau d'informations pour afficher les détails de la ligne sélectionnée
info_frame = tk.Frame(main_frame, width=300, relief=tk.RAISED, borderwidth=1)
info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

# Charger les données dans le tableau principal à partir du fichier JSON
file_path = r"D:\_CyberPunk-Creation\BDDDialogues\testReduit.json"
open_and_display_json(tree, file_path)

###### A METTRE DANS PLAYLIST ? #############
# Frame pour les boutons et la playlist
bottom_frame = tk.Frame(root)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

# Configurer les boutons entre les tableaux (playlist)
button_frame = tk.Frame(bottom_frame)
button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

# Ajouter les boutons pour gérer la playlist
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

load_button = tk.Button(button_frame, text="Charger la playlist", command=lambda: load_playlist_from_file(playlist_tree))
load_button.pack(side=tk.LEFT, padx=5)

# Configurer la playlist en dessous du tableau principal et du panneau d'informations
playlist_info_frame = tk.Frame(bottom_frame, width=300, relief=tk.RAISED, borderwidth=1)
playlist_info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
playlist_columns = ("ID", "Sous-titres", "Origine", "Audio", "Origine 2", "Quête")
playlist_tree = ttk.Treeview(bottom_frame, columns=playlist_columns, show="headings", height=10)

# Configurer les en-têtes et colonnes de la playlist
for column in playlist_columns:
    playlist_tree.heading(column, text=column)
    if column == "ID":
        playlist_tree.column(column, width=130, minwidth=100, stretch=False, anchor="w")
    elif column == "Origine":
        playlist_tree.column(column, width=70, minwidth=200, stretch=True, anchor="w")
    elif column == "Origine 2":
        playlist_tree.column(column, width=70, minwidth=200, stretch=True, anchor="w")
    else:
        playlist_tree.column(column, width=150, anchor="w")

# Ajouter la barre de défilement pour la playlist
playlist_scrollbar = ttk.Scrollbar(bottom_frame, orient=tk.VERTICAL, command=playlist_tree.yview)
playlist_tree.configure(yscroll=playlist_scrollbar.set)
playlist_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

playlist_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
########################

# Menu contextuel pour le tableau principal
def show_context_menu(event):
    menu = Menu(root, tearoff=0)
    menu.add_command(label="Ajouter à la playlist", command=lambda: add_to_playlist(tree, playlist_tree))
    menu.post(event.x_root, event.y_root) 

# Lier les événements du tableau principal
tree.bind("<Button-3>", show_context_menu)  # Clic droit pour afficher le menu contextuel
tree.bind("<Double-1>", lambda event: copy_cell(event, tree, root))  # Double clic pour copier une cellule
tree.bind("<<TreeviewSelect>>", lambda event: display_info(event, tree, info_frame))  # Sélectionner une ligne pour afficher les détails

# Lancer la boucle principale de l'application
root.mainloop()
