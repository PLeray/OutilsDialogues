# fichier: filtrage.py
import tkinter as tk
from tkinter import ttk
from gui_functions import open_and_display_json

_pasAttribuer = "RIEN"

# Fonction pour réinitialiser les filtres et restaurer toutes les lignes
def reset_filters(tree, filters, file_path):
    for _, widget in filters:
        if isinstance(widget, tk.Entry):  # Vérifie si c'est un champ de texte
            widget.delete(0, tk.END)
        elif isinstance(widget, ttk.Combobox):  # Vérifie si c'est une Combobox
            widget.set("")  # Réinitialise la sélection
    open_and_display_json(tree, file_path)
    initialize_quete_droplist(tree, 5)
    initialize_personnage_droplist(tree, 3)
    initialize_personnage_droplist(tree, 4) # pour V homme


def filter_tree_with_filters(tree, filters, file_path, label_count):
    """
    Filtre les lignes du Treeview en fonction des widgets de filtre dans la liste `filters`.
    Met également à jour un label pour afficher le nombre de lignes correspondantes.

    :param tree: Le Treeview contenant les données.
    :param filters: Une liste de tuples contenant les indices de colonnes et les widgets de filtre.
    :param file_path: Le chemin du fichier source des données.
    :param label_count: Le label Tkinter pour afficher le nombre de lignes correspondantes.
    """
    open_and_display_json(tree, file_path)
    matching_count = 0  # Compteur de lignes correspondantes

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
            matching_count += 1  # Incrémenter le compteur si la ligne correspond
        else:
            tree.detach(item)

    # Mettre à jour le label avec le nombre de lignes correspondantes
    label_count.config(text=f"Lignes correspondantes : {matching_count}")


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
        if value == _pasAttribuer:
            quetes.add(_pasAttribuer)  # Ajouter directement _pasAttribuer sans modification
        elif value:
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
        if personnage_value in ["Tous", "Toutes", _pasAttribuer] or personnage_value.lower() in values[personnage_column_index].lower():
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
        quete_val = values[quete_column_index] if len(values) > quete_column_index else ""

        # Normaliser quete_val pour éviter les erreurs avec lower()
        quete_val = quete_val if quete_val else ""  # Remplacer None par chaîne vide

        # Ajouter les personnages associés à la quête sélectionnée
        if (
            quete_value in ["Tous", "Toutes"]  # Cas général : Toutes les quêtes
            or quete_value == _pasAttribuer and (quete_val == _pasAttribuer or not quete_val)  # Cas spécifique pour _pasAttribuer
            or (quete_val and quete_value.lower() in quete_val.lower())  # Cas où quete_value correspond
        ):
            personnage = (
                values[personnage_column_index].split("/")[-1].split("_")[0]
                if "/" in values[personnage_column_index]
                else values[personnage_column_index]
            )
            personnages.add(personnage)

    personnage_combobox["values"] = ["Tous"] + sorted(personnages)

    # Rétablir la sélection précédente si elle est toujours valide
    if current_selection in personnages:
        personnage_combobox.set(current_selection)
    else:
        personnage_combobox.set("Tous")





def filter_NA(tree, na_var):
    """
    Filtre les lignes du Treeview pour exclure celles dont la 4ᵉ colonne contient 'N/A',
    en fonction de l'état de la case à cocher.

    :param tree: Le Treeview contenant les données.
    :param na_var: La variable associée à la case à cocher 'Afficher N/A'.
    """
    # Obtenir l'état de la case à cocher
    show_na = na_var.get()

    for item in tree.get_children():
        values = tree.item(item, "values")  # Récupère les valeurs de la ligne

        # Vérifier si la 4ᵉ colonne contient 'N/A'
        if not show_na and values[3] == _pasAttribuer:
            tree.detach(item)  # Masquer la ligne
        else:
            tree.item(item, open=True)  # Afficher la ligne

def toggle_columns(tree, playlist_tree, gender_var):
    """
    Affiche ou masque les colonnes du Treeview et ajuste leurs largeurs pour remplir l'espace disponible.
    :param tree: Le Treeview à modifier.
    :param gender_var: La variable liée aux boutons radio ("homme" ou "femme").
    """
    columnsHomme = ("ID", "(M) Sous-titres", "(M) Voix", "Quête")
    columnsFemme = ("ID", "(F) Sous-titres", "(F) Voix", "Quête")
    # Récupérer la sélection actuelle
    selected_gender = gender_var.get()
    # Configuration des colonnes selon le genre sélectionné
    if selected_gender == "homme":
        tree["displaycolumns"] = columnsHomme
    else:
        tree["displaycolumns"] = columnsFemme

    # Ajuster dynamiquement la largeur des colonnes visibles
    total_width = tree.winfo_width()  # Largeur totale du Treeview
    visible_columns = tree["displaycolumns"]
    largeur_ColID = 130

    column_width = (total_width - largeur_ColID)  // (len(visible_columns)-1)   # Largeur égale pour chaque colonne

    for col in tree["columns"]:
        if col == "ID":
            tree.column(col, width=largeur_ColID, minwidth=100, stretch=False, anchor="w")
        else:
            if col in visible_columns:
                tree.column(col, width=column_width, stretch=True)  # Ajuster la largeur
            else:
                tree.column(col, width=0, stretch=False)  # Cacher les colonnes


    # Configuration des colonnes pour playlist_tree selon le genre sélectionné
    if selected_gender == "homme":
        playlist_tree["displaycolumns"] = columnsHomme
    elif selected_gender == "femme":
        playlist_tree["displaycolumns"] = columnsFemme

    column_width = (total_width - largeur_ColID)  // (len(visible_columns)-1)   # Largeur égale pour chaque colonne

    for col in playlist_tree["columns"]:
        if col == "ID":
            playlist_tree.column(col, width=largeur_ColID, minwidth=100, stretch=False, anchor="w")
        else:
            if col in visible_columns:
                playlist_tree.column(col, width=column_width, stretch=True)  # Ajuster la largeur
            else:
                playlist_tree.column(col, width=0, stretch=False)  # Cacher les colonnes                
    """        
    """
