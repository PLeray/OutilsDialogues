# fichier: filtrage.py

from gui_functions import open_and_display_json

# Frame pour les filtres
def filter_tree(tree, column_index, filter_text):
    # Fonction pour filtrer les lignes du tableau principal en fonction du texte de filtre
    for item in tree.get_children():
        values = tree.item(item, "values")
        if filter_text.lower() in values[column_index].lower():
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


def update_personnage_droplist(tree, combobox, column_index):
    """
    Met à jour la liste déroulante avec les valeurs uniques des préfixes des fichiers .ogg.

    :param tree: Le Treeview contenant les données.
    :param combobox: La Combobox à mettre à jour.
    :param column_index: L'index de la colonne à analyser pour extraire les préfixes.
    """
    prefixes = set()
    for item in tree.get_children():
        file_name = tree.item(item, "values")[column_index]
        if file_name.endswith(".ogg"):  # Vérifie si le fichier a l'extension .ogg
            prefix = file_name.split("_")[0]  # Récupère le préfixe avant le premier "_"
            prefixes.add(prefix)
    
    combobox["values"] = sorted(prefixes)  # Met à jour les valeurs de la Combobox avec les préfixes triés

def filter_by_droplist(tree, column_index, selected_value):
    """
    Filtrer les lignes d'un Treeview en fonction de la valeur sélectionnée dans la liste déroulante.

    :param tree: Le Treeview à filtrer.
    :param column_index: L'index de la colonne à analyser.
    :param selected_value: La valeur sélectionnée dans la liste déroulante.
    """
    for item in tree.get_children():
        values = tree.item(item, "values")
        if selected_value in values[column_index]:  # Vérifie si la valeur sélectionnée correspond
            tree.item(item, tags="match")
        else:
            tree.item(item, tags="nomatch")

    # Configure les couleurs des lignes correspondantes et non correspondantes
    tree.tag_configure("match", foreground="black")
    tree.tag_configure("nomatch", foreground="gray")