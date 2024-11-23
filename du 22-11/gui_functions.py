# fichier: gui_functions.py
import tkinter as tk
from tkinter import ttk
from typing import Dict, List
from custom_types import Dialogue
from data_loader import load_json

# Fonction pour afficher les données dans le tableau
def open_and_display_json(tree, file_path: str):
    """
    Charge les données JSON à partir d'un fichier et les affiche dans le TreeView.
    """
    data = load_json(file_path)

    # Vérification du type de données (liste ou dictionnaire)
    if isinstance(data, list):
        # Si c'est une liste, convertir en dictionnaire avec des clés uniques
        data = {str(i): item for i, item in enumerate(data)}

    for item in tree.get_children():
        tree.delete(item)

    for key, value in data.items():
        sous_titres = value.get('female', {}).get('text', 'N/A')
        vo_path = value.get('female', {}).get('vo', {}).get('main', 'N/A')
        path = value.get('_path', 'N/A')
        path_parts = path.split('/', 1)
        origine_a = path_parts[0] if len(path_parts) > 0 else 'N/A'
        quete = path_parts[1].split('{}', 1)[-1] if len(path_parts) > 1 else 'N/A'

        item_id = tree.insert("", "end", values=(key, sous_titres, origine_a, vo_path, origine_a, quete))
        if vo_path == "N/A":
            tree.item(item_id, tags=('na_audio',))

    tree.tag_configure('na_audio', background='red')
    return data


# Fonction pour appliquer les filtres
def apply_filters_to_tree(tree, data: Dict[str, Dialogue], filters: List[str], columns: List[str]):
    """
    Applique des filtres sur un TreeView en fonction des valeurs saisies dans les champs de filtre.
    """
    for item in tree.get_children():
        tree.delete(item)

    for key, value in data.items():
        sous_titres = value.get('female', {}).get('text', 'N/A')
        vo_path = value.get('female', {}).get('vo', {}).get('main', 'N/A')
        path = value.get('_path', 'N/A')
        path_parts = path.split('/', 1)
        origine_a = path_parts[0] if len(path_parts) > 0 else 'N/A'
        quete = path_parts[1].split('{}', 1)[-1] if len(path_parts) > 1 else 'N/A'

        row_data = (key, sous_titres, origine_a, vo_path, origine_a, quete)

        match = True
        for i, filter_text in enumerate(filters):
            if filter_text and filter_text.lower() not in str(row_data[i]).lower():
                match = False
                break

        if match:
            item_id = tree.insert("", "end", values=row_data)
            if vo_path == "N/A":
                tree.item(item_id, tags=('na_audio',))
    tree.tag_configure('na_audio', background='red')
