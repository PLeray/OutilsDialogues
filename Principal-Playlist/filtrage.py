# fichier: filtrage.py
import tkinter as tk
from tkinter import ttk
from gui_functions import open_and_display_json

"""
# Frame pour les filtres A SUPRIMER 
def filter_tree(tree, column_index, filter_text):
    # Fonction pour filtrer les lignes du tableau principal en fonction du texte de filtre
    for item in tree.get_children():
        values = tree.item(item, "values")
        if filter_text.lower() in values[column_index].lower():
            tree.item(item, open=True)
        else:
            tree.detach(item)

"""

# Fonction pour réinitialiser les filtres et restaurer toutes les lignes
def reset_filters(tree, filters, file_path):
    for entry in filters:
        entry.delete(0, tk.END)
    open_and_display_json(tree, file_path)
    initialize_quete_droplist(tree, 5)
    initialize_personnage_droplist(tree, 3)



def filter_tree_with_filters(tree, filters, file_path):
    """
    Filtre les lignes du Treeview en fonction des widgets de filtre dans la liste `filters`.

    :param tree: Le Treeview contenant les données.
    :param filters: Une liste de tuples contenant les indices de colonnes et les widgets de filtre.
    """
    open_and_display_json(tree, file_path)

    for item in tree.get_children():
        values = tree.item(item, "values")
        match = True  # Correspondance par défaut : True

        # Vérifier chaque filtre
        for column_index, widget in filters:
            filter_value = widget.get().strip()  # Récupère la valeur du widget

            # Filtrage via Combobox
            if isinstance(widget, ttk.Combobox):
                if filter_value in ["Tous", "Toutes"]:
                    continue  # Ignorer les valeurs par défaut

                # Extraire la valeur pertinente
                if column_index == 5:  # Colonne des quêtes
                    cell_value = values[column_index].split("/")[-1] if "/" in values[column_index] else values[column_index]
                else:  # Colonne des personnages ou autre
                    cell_value = values[column_index].split("/")[-1].split("_")[0] if "/" in values[column_index] else values[column_index]

                if filter_value.lower() != cell_value.lower():
                    match = False
                    break

            # Filtrage via Entrée texte
            elif isinstance(widget, tk.Entry):
                if filter_value and filter_value.lower() not in values[column_index].lower():
                    match = False
                    break

        # Gérer la ligne en fonction de la correspondance
        if match:
            tree.item(item, open=True)
        else:
            tree.detach(item)

def initialize_personnage_droplist(tree, column_index):
    """
    Remplit une liste de valeurs uniques pour une liste déroulante en fonction des fichiers dans une colonne.

    :param tree: Le Treeview contenant les données.
    :param column_index: L'index de la colonne "Personnage" à analyser.
    :return: Une liste triée des noms de personnages uniques avec "Tous" ajouté en premier.
    """
    personnages = set()
    for item in tree.get_children():
        # Récupérer la valeur de la colonne
        value = tree.item(item, "values")[column_index]
        if value and "/" in value and "_" in value:
            last_part = value.split("/")[-1]  # Obtenir la partie après le dernier "/"
            personnage = last_part.split("_")[0]  # Obtenir la partie avant le premier "_"
            personnages.add(personnage)

    sorted_personnages = sorted(personnages)  # Trier les personnages
    return ["Tous"] + sorted_personnages  # Ajouter "Tous" au début


def initialize_quete_droplist(tree, column_index):
    """
    Remplit une liste de valeurs uniques pour une liste déroulante en fonction des quêtes dans une colonne.

    :param tree: Le Treeview contenant les données.
    :param column_index: L'index de la colonne "Quête" à analyser.
    :return: Une liste triée des noms de quêtes uniques avec "Toutes" ajouté en premier.
    """
    quetes = set()
    for item in tree.get_children():
        # Récupérer la valeur de la colonne
        value = tree.item(item, "values")[column_index]
        if value:
            # Extraire la partie après le dernier "/"
            quete = value.split("/")[-1]
            quetes.add(quete)

    sorted_quetes = sorted(quetes)  # Trier les quêtes
    return ["Toutes"] + sorted_quetes  # Ajouter "Toutes" au début


def update_quete_based_on_personnage(tree, filters, quete_column_index, personnage_column_index, personnage_value):
    """
    Met à jour les options de la liste déroulante des quêtes en fonction du personnage sélectionné,
    tout en préservant la sélection actuelle si elle est valide.
    """
    quete_combobox = None
    for index, widget in filters:
        if index == quete_column_index and isinstance(widget, ttk.Combobox):
            quete_combobox = widget
            break

    if not quete_combobox:
        return

    current_selection = quete_combobox.get()  # Sauvegarder la sélection actuelle
    quetes = set()

    for item in tree.get_children():
        values = tree.item(item, "values")

        # Ajouter les quêtes associées au personnage sélectionné
        if personnage_value in ["Tous", "Toutes"] or personnage_value.lower() in values[personnage_column_index].lower():
            quete = values[quete_column_index].split("/")[-1] if "/" in values[quete_column_index] else values[quete_column_index]
            quetes.add(quete)

    quete_combobox["values"] = ["Toutes"] + sorted(quetes)

    # Rétablir la sélection précédente si elle est toujours valide
    if current_selection in quetes:
        quete_combobox.set(current_selection)
    else:
        quete_combobox.set("Toutes")


def update_personnage_based_on_quete(tree, filters, quete_column_index, personnage_column_index, quete_value):
    """
    Met à jour les options de la liste déroulante des personnages en fonction de la quête sélectionnée,
    tout en préservant la sélection actuelle si elle est valide.
    """
    personnage_combobox = None
    for index, widget in filters:
        if index == personnage_column_index and isinstance(widget, ttk.Combobox):
            personnage_combobox = widget
            break

    if not personnage_combobox:
        return

    current_selection = personnage_combobox.get()  # Sauvegarder la sélection actuelle
    personnages = set()

    for item in tree.get_children():
        values = tree.item(item, "values")

        # Ajouter les personnages associés à la quête sélectionnée
        if quete_value in ["Tous", "Toutes"] or quete_value.lower() in values[quete_column_index].lower():
            personnage = values[personnage_column_index].split("/")[-1].split("_")[0] if "/" in values[personnage_column_index] else values[personnage_column_index]
            personnages.add(personnage)

    personnage_combobox["values"] = ["Tous"] + sorted(personnages)

    # Rétablir la sélection précédente si elle est toujours valide
    if current_selection in personnages:
        personnage_combobox.set(current_selection)
    else:
        personnage_combobox.set("Tous")
