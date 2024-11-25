# fichier: gui_functions.py
import tkinter as tk
from tkinter import ttk, Menu
from typing import Dict
from custom_types import Dialogue
from data_loader import load_json

from LectureOgg import JouerAudio

#definition du Tableau Principal
def setup_TableauPrincipal(root, tk, columns):
    # Frame principale pour contenir le tableau principal et le panneau d'informations
    main_frame = tk.Frame(root)
    main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Configuration du tableau principal (tree)
    tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15, selectmode="extended")
    
    
    # Configurer les en-têtes de colonnes avec la possibilité de trier les données
    for column in columns:
        tree.heading(column, text=column, command=lambda c=column: sort_tree(tree, c, False))

    # Configurer les colonnes (largeur, alignement, etc.)
    for column in columns:
        if column == "ID":
            tree.column(column, width=130, minwidth=100, stretch=False, anchor="w")
        elif column == "Origine":
            tree.column(column, width=70, minwidth=200, stretch=False, anchor="w")
        elif column == "Origine 2":
            tree.column(column, width=70, minwidth=200, stretch=False, anchor="w")
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
 
    return tree

# Fonction pour afficher les données dans le tableau
def open_and_display_json(tree, file_path):
    data = load_json(file_path)
    if not data:
        print("Aucune donnée chargée depuis le fichier JSON.")
        return

    # Supprimer les anciennes données du tableau
    for item in tree.get_children():
        tree.delete(item)

    # Vérifiez si les données sont une liste
    if isinstance(data, list):
        for entry in data:
            sous_titres = entry.get('female', {}).get('text', 'N/A')
            vo_path = entry.get('female', {}).get('vo', {}).get('main', 'N/A')
            path = entry.get('_path', 'N/A')

            path_parts = path.split('/', 1)
            origine_2 = path_parts[0] if len(path_parts) > 0 else 'N/A'
            quete = path_parts[1].split('{}', 1)[-1] if len(path_parts) > 1 else 'N/A'

            tree.insert("", tk.END, values=(
                entry.get('ID', 'N/A'), 
                entry.get('Sous-titres', 'N/A'),
                entry.get('Origine', 'N/A'),
                entry.get('Personnage', 'N/A'),
                entry.get('Origine 2', 'N/A'),
                entry.get('Quête', 'N/A')
            ))
    # Vérifiez si les données sont un dictionnaire
    elif isinstance(data, dict):
        for key, value in data.items():
            sous_titres = value.get('female', {}).get('text', 'N/A')
            vo_path = value.get('female', {}).get('vo', {}).get('main', 'N/A')
            path = value.get('_path', 'N/A')

            path_parts = path.split('/', 1)
            origine_2 = path_parts[0] if len(path_parts) > 0 else 'N/A'
            quete = path_parts[1].split('{}', 1)[-1] if len(path_parts) > 1 else 'N/A'

            tree.insert("", tk.END, values=(key, sous_titres, origine_2, vo_path, origine_2, quete))

    else:
        print("Erreur : Le type de données JSON est inconnu.")

#Fonction pour la selection d'une ligne du tableau principal
def SelectionLigne(event, tree):
    selected_item = tree.selection()[0]
    selected_values = tree.item(selected_item, 'values')
    audio_value = selected_values[3]  # 4ème colonne (indice 3) pour "Personnage"    
    print(f"Lecture de : {audio_value}")   
    JouerAudio(audio_value)

# Fonction pour trier le tableau principal
def sort_tree(tree, col, reverse):
    # Récupérer toutes les lignes et les trier en fonction de la colonne spécifiée
    l = [(tree.set(k, col), k) for k in tree.get_children('')]
    l.sort(reverse=reverse)

    # Réorganiser les lignes dans l'ordre trié
    for index, (val, k) in enumerate(l):
        tree.move(k, '', index)

    # Mettre à jour le titre de la colonne pour indiquer le sens du tri
    tree.heading(col, command=lambda: sort_tree(tree, col, not reverse))    