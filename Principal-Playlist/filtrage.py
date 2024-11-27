# fichier: filtrage.py
import tkinter as tk
from tkinter import ttk
from gui_functions import open_and_display_json

_pasAttribuer = "RIEN"

# Fonction pour réinitialiser les filtres et restaurer toutes les lignes
def reset_filters(tree, filters, file_path):
    """
    Réinitialise tous les filtres (champs de texte et combobox) et recharge les données.

    :param tree: Treeview contenant les données.
    :param filters: Liste des filtres sous forme (column_name, label_widget, entry_widget).
    :param file_path: Chemin du fichier contenant les données à afficher.
    """
    for _, _, widget in filters:  # Ignorer les labels et récupérer uniquement les widgets
        if isinstance(widget, tk.Entry):  # Vérifie si c'est un champ de texte
            widget.delete(0, tk.END)
        elif isinstance(widget, ttk.Combobox):  # Vérifie si c'est une Combobox
            widget.set("")  # Réinitialise la sélection

    # Recharge le contenu du Treeview avec le fichier JSON
    open_and_display_json(tree, file_path)

    # Réinitialise les listes déroulantes spécifiques
    initialize_quete_droplist(tree, 5)
    initialize_personnage_droplist(tree, 3)
    initialize_personnage_droplist(tree, 4)  # Pour V homme


def filter_tree_with_filters(tree, filters, file_path, label_count):
    """
    Filtre les lignes du Treeview en fonction des widgets de filtre dans la liste `filters`.
    Met également à jour un label pour afficher le nombre de lignes correspondantes.

    :param tree: Le Treeview contenant les données.
    :param filters: Une liste de tuples contenant les noms de colonnes, labels, et widgets de filtre.
    :param file_path: Le chemin du fichier source des données.
    :param label_count: Le label Tkinter pour afficher le nombre de lignes correspondantes.
    """
    open_and_display_json(tree, file_path)
    matching_count = 0  # Compteur de lignes correspondantes

    for item in tree.get_children():
        values = tree.item(item, "values")
        match = True  # Correspondance par défaut : True

        # Vérifier chaque filtre
        for column_name, _, widget in filters:  # On ignore le label dans ce cas
            filter_value = widget.get().strip()  # Récupère la valeur du widget

            # Identifier l'indice de colonne dans le Treeview
            try:
                column_index = tree["columns"].index(column_name)
            except ValueError:
                continue  # Si la colonne n'existe pas, ignorer le filtre

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

    :param tree: Treeview contenant les données.
    :param filters: Liste des filtres sous forme (column_name, label_widget, entry_widget).
    :param quete_column_index: Index de la colonne des quêtes dans le Treeview.
    :param personnage_column_index: Index de la colonne des personnages dans le Treeview.
    :param personnage_value: Valeur sélectionnée pour le personnage.
    """
    quete_combobox = None

    # Trouver la combobox associée aux quêtes
    for column_name, _, widget in filters:
        if column_name == "Quête" and isinstance(widget, ttk.Combobox):
            quete_combobox = widget
            break

    if not quete_combobox:  # Si aucun widget n'est trouvé, arrêter
        return

    current_selection = quete_combobox.get()  # Sauvegarder la sélection actuelle
    quetes = set()

    # Parcourir les lignes du Treeview
    for item in tree.get_children():
        values = tree.item(item, "values")
        if len(values) <= max(quete_column_index, personnage_column_index):
            continue  # Ignorer les lignes où les colonnes sont absentes

        # Obtenir les valeurs des colonnes de personnage et quête
        personnage_val = values[personnage_column_index].strip() if values[personnage_column_index] else ""
        quete_val = values[quete_column_index].strip() if values[quete_column_index] else ""

        # Ajouter les quêtes associées au personnage sélectionné
        if personnage_value in ["Tous", "Toutes", _pasAttribuer] or personnage_value.lower() in personnage_val.lower():
            quete_val = values[quete_column_index].split("/")[-1] if "/" in values[quete_column_index] else values[quete_column_index]
            quetes.add(quete_val)

    # Mettre à jour les options de la Combobox des quêtes
    quete_combobox["values"] = ["Toutes"] + sorted(quetes)

    # Rétablir la sélection précédente si elle est toujours valide
    if current_selection in quetes:
        quete_combobox.set(current_selection)
    else:
        quete_combobox.set("Toutes")


def update_personnage_based_on_quete(tree, filters, quete_column_index, personnage_column_indexes, quete_value):
    """
    Met à jour les options des listes déroulantes des personnages (voix féminine et masculine)
    en fonction de la quête sélectionnée, tout en préservant la sélection actuelle si elle est valide.

    :param tree: Treeview contenant les données.
    :param filters: Liste des filtres sous forme (column_name, label_widget, entry_widget).
    :param quete_column_index: Index de la colonne des quêtes dans le Treeview.
    :param personnage_column_indexes: Tuple contenant les indices des colonnes "(F) Voix" et "(M) Voix".
    :param quete_value: Valeur sélectionnée pour la quête.
    """
    # Obtenir les indices des colonnes pour "(F) Voix" et "(M) Voix"
    voix_f_index, voix_m_index = personnage_column_indexes

    # Trouver les comboboxes associées à "(F) Voix" et "(M) Voix"
    voix_f_combobox = None
    voix_m_combobox = None

    for column_name, _, widget in filters:
        if column_name == "(F) Voix" and isinstance(widget, ttk.Combobox):
            voix_f_combobox = widget
        elif column_name == "(M) Voix" and isinstance(widget, ttk.Combobox):
            voix_m_combobox = widget

    if not voix_f_combobox and not voix_m_combobox:
        print("Aucune combobox pour '(F) Voix' ou '(M) Voix' trouvée dans les filtres.")
        return

    # Sauvegarder les sélections actuelles
    current_selection_f = voix_f_combobox.get() if voix_f_combobox else None
    current_selection_m = voix_m_combobox.get() if voix_m_combobox else None

    voix_f_personnages = set()
    voix_m_personnages = set()

    # Parcourir les lignes du Treeview pour filtrer les personnages
    for item in tree.get_children():
        values = tree.item(item, "values")

        # Assurez-vous que les indices de colonnes sont valides
        if len(values) <= max(quete_column_index, voix_f_index, voix_m_index):
            continue

        # Obtenir les valeurs des colonnes de quête, voix féminine et masculine
        quete_val = values[quete_column_index].strip() if values[quete_column_index] else ""
        voix_f_val = values[voix_f_index].strip() if values[voix_f_index] else ""
        voix_m_val = values[voix_m_index].strip() if values[voix_m_index] else ""

        # Ajouter les personnages associés à la quête sélectionnée (avec extraction de la partie utile)
        if (
            quete_value in ["Tous", "Toutes"] or  # Toutes les quêtes
            quete_value.lower() in quete_val.lower()  # Quête correspondante
        ):
            voix_f_personnages.add(
                voix_f_val.split("/")[-1].split("_")[0] if "/" in voix_f_val else voix_f_val
            )
            voix_m_personnages.add(
                voix_m_val.split("/")[-1].split("_")[0] if "/" in voix_m_val else voix_m_val
            )

    # Mettre à jour la Combobox de "(F) Voix"
    if voix_f_combobox:
        if voix_f_personnages:
            voix_f_combobox["values"] = ["Tous"] + sorted(voix_f_personnages)
            if current_selection_f in voix_f_personnages:
                voix_f_combobox.set(current_selection_f)
            else:
                voix_f_combobox.set("Tous")
        else:
            voix_f_combobox["values"] = ["Tous"]
            voix_f_combobox.set("Tous")

    # Mettre à jour la Combobox de "(M) Voix"
    if voix_m_combobox:
        if voix_m_personnages:
            voix_m_combobox["values"] = ["Tous"] + sorted(voix_m_personnages)
            if current_selection_m in voix_m_personnages:
                voix_m_combobox.set(current_selection_m)
            else:
                voix_m_combobox.set("Tous")
        else:
            voix_m_combobox["values"] = ["Tous"]
            voix_m_combobox.set("Tous")



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

def toggle_columns(tree, playlist_tree, filters, gender_var):
    """
    Affiche ou masque les colonnes du Treeview et synchronise les filtres.
    Répartit les colonnes restantes de manière équitable après avoir fixé la largeur de la colonne ID.

    :param tree: Le Treeview principal.
    :param filters: Liste des filtres (nom_colonne, label_widget, entry_widget).
    :param gender_var: Variable de genre ("homme" ou "femme").
    """
    columns_homme = ["ID", "(M) Sous-titres", "(M) Voix", "Quête"]
    columns_femme = ["ID", "(F) Sous-titres", "(F) Voix", "Quête"]

    selected_gender = gender_var.get()
    visible_columns = columns_homme if selected_gender == "homme" else columns_femme
    tree["displaycolumns"] = visible_columns

    # Largeur totale du Treeview
    total_width = tree.winfo_width()

    # Largeur fixe pour la colonne ID
    id_column_width = 130

    # Largeur restante pour les colonnes visibles (sauf ID)
    remaining_width = total_width - id_column_width

    # Nombre de colonnes visibles, sauf la colonne ID
    remaining_columns_count = len(visible_columns) - 1
    column_width = remaining_width // remaining_columns_count if remaining_columns_count > 0 else 0

    # Ajuster les colonnes dans le Treeview
    for col in tree["columns"]:
        if col == "ID":
            tree.column(col, width=id_column_width, minwidth=100, stretch=False, anchor="w")
        elif col in visible_columns:
            tree.column(col, width=column_width, stretch=True)
        else:
            tree.column(col, width=0)

    # Ajuster les colonnes dans le playlist
    for col in tree["columns"]:
        if col == "ID":
            tree.column(col, width=id_column_width, minwidth=100, stretch=False, anchor="w")
        elif col in visible_columns:
            tree.column(col, width=column_width, stretch=True)
        else:
            tree.column(col, width=0)            

    # Synchroniser les filtres
    update_filters_visibility(filters, visible_columns)

def update_filters_visibility(filters, visible_columns):
    """
    Met à jour la visibilité des widgets de filtre et des labels associés en fonction des colonnes visibles.

    :param filters: Liste des filtres sous forme (nom_colonne, label_widget, entry_widget).
    :param visible_columns: Liste des colonnes actuellement visibles.
    """
    for column, label, widget in filters:
        if column in visible_columns:  # Si la colonne est visible
            if not widget.winfo_ismapped():
                label.grid()  # Afficher le label
                widget.grid()  # Afficher le widget
        else:  # Si la colonne est masquée
            if widget.winfo_ismapped():
                label.grid_remove()  # Masquer le label
                widget.grid_remove()  # Masquer le widget

                     

