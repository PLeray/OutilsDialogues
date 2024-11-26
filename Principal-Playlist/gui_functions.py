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

    # Ajouter une barre de défilement verticale uniquement
    scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)

    # Configurer le tableau pour utiliser la barre de défilement verticale uniquement
    tree.configure(yscroll=scrollbar.set)

    # Positionner la barre de défilement verticale et le tableau principal dans la frame principale
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.BOTH, expand=True)

    return tree

# Fonction pour afficher les données dans le tableau
def open_and_display_json(tree, file_path):
    """
    Charge les données depuis un fichier JSON et les affiche dans un Treeview.
    Si (M) Sous-titres ou (M) Voix est vide, utilise les valeurs de (F) Sous-titres ou (F) Voix respectivement.
    
    :param tree: Le Treeview à remplir.
    :param file_path: Le chemin du fichier JSON.
    """
    # Charger les données JSON
    data = load_json(file_path)
    if not data:
        print("Aucune donnée chargée depuis le fichier JSON.")
        return

    # Supprimer les anciennes données du tableau
    tree.delete(*tree.get_children())

    # Traiter les données
    for key, entry in data.items():
        # ID
        _id = key

        # Récupérer la quête
        path = entry.get("_path", "N/A")
        quete = path.split('/', 1)[-1].split('{}', 1)[-1] if '/' in path else "N/A"

        # Récupérer les informations pour 'female'
        female_text = entry.get("female", {}).get("text", "N/A")
        female_vo = entry.get("female", {}).get("vo", {}).get("main", "N/A")

        # Récupérer les informations pour 'male'
        male_text = entry.get("male", {}).get("text", "N/A")
        male_vo = entry.get("male", {}).get("vo", {}).get("main", "N/A")

        # Remplacer les valeurs manquantes pour 'male' par celles de 'female'
        if not male_text or male_text == "N/A":
            male_text = female_text
        if not male_vo or male_vo == "N/A":
            male_vo = female_vo

        # Insérer une ligne dans le Treeview
        tree.insert("", tk.END, values=(
            _id,           # ID
            female_text,   # (F) Sous-titres
            male_text,     # (M) Sous-titres
            female_vo,     # (F) Voix
            male_vo,       # (M) Voix
            quete          # Quête
        ))

#Fonction pour la selection d'une ligne du tableau principal
def SelectionLigne(event, tree, gender_var):
    selected_item = tree.selection()[0]
    selected_values = tree.item(selected_item, 'values')

    selected_gender = gender_var.get()
    if selected_gender == "homme":
        audio_value = selected_values[4]
    else:
        audio_value = selected_values[3]

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


