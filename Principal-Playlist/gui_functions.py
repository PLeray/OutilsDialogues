# fichier: gui_functions.py
import tkinter as tk
from tkinter import ttk, Menu
from typing import Dict
from custom_types import Dialogue
from data_loader import load_json

from LectureOgg import JouerAudio

    
# Fonction pour afficher les données dans le tableau
def open_and_display_json(tree, file_path: str):
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


#Fonction pour la selection d'une ligne
def SelectionLigne(event, tree, info_frame):
    display_info(event, tree, info_frame)

# Fonction pour afficher les informations de la ligne sélectionnée
def display_info(event, tree, info_frame):
    info_frame.config(width=400)
    info_frame.pack_propagate(False)
    try:
        selected_item = tree.selection()[0]
        selected_values = tree.item(selected_item, 'values')

        for widget in info_frame.winfo_children():
            widget.destroy()

        labels = ["ID2", "Sous-titres", "Origine", "Personnage", "Origine", "Quête"]
        for i, value in enumerate(selected_values):
            text = tk.Text(info_frame, height=1, wrap="none", borderwidth=0)
            text.insert("1.0", f"{labels[i]}: {value}")
            text.config(state="disabled")
            text.pack(fill="x", padx=5, pady=2)
        
        # Ajouter l'information supplémentaire "Son"
        audio_value = selected_values[3]  # 4ème colonne (indice 3) pour "Personnage"       
        JouerAudio(audio_value)

    except IndexError:
        pass

# Fonction pour ajouter les filtres et les boutons de contrôle au-dessus du premier tableau
def add_filters(frame, tree):
    filter_frame = tk.Frame(frame)
    filter_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

    columns = ["ID", "Sous-titres", "Origine", "Personnage", "Origine", "Quête"]
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