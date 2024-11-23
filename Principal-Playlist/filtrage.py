# fichier: filtrage.py

# Frame pour les filtres
def filter_tree(tree, column_index, filter_text):
    # Fonction pour filtrer les lignes du tableau principal en fonction du texte de filtre
    for item in tree.get_children():
        values = tree.item(item, "values")
        if filter_text.lower() in values[column_index].lower():
            tree.item(item, open=True)
        else:
            tree.detach(item)


# Fonction pour réinitialiser les filtres et restaurer toutes les lignes
def reset_filters(tree, filters, file_path):
    # Effacer les entrées des filtres
    for entry in filters:
        entry.delete(0, tk.END)
    # Recharger les données d'origine à partir du fichier JSON
    open_and_display_json(tree, file_path)

