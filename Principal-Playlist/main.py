# fichier: main.py
import tkinter as tk

from tkinter import ttk
from gui_functions import open_and_display_json, SelectionLigne, sort_tree, setup_TableauPrincipal
from playlist_functions import select_and_add_to_playlist, setup_playlist, add_to_playlist, move_up_playlist, move_down_playlist, save_playlist_to_file, clear_playlist
from filtrage import toggle_columns, filter_NA, reset_filters, filter_tree_with_filters, initialize_personnage_droplist, initialize_quete_droplist, update_quete_based_on_personnage, update_personnage_based_on_quete


#from custom_types import Dialogue
#from data_loader import load_json

# Charger les données dans le tableau principal à partir du fichier JSON
file_path = r"D:\_CyberPunk-Creation\BDDDialogues\testReduit.json"
#file_path = r"D:\_CyberPunk-Creation\BDDDialogues\subtitles.DIVQuO_-.json"

# Créer la fenêtre principale
root = tk.Tk()
root.title("Visualisateur de JSON en tableau avec copier-coller et panneau d'informations")
root.geometry("1500x800")
root.minsize(1100, 800)

# Créer une frame pour le bouton au-dessus du tableau principal
button_frame = tk.Frame(root)
button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

# Ajouter un bouton au-dessus du tableau principal
action_button = tk.Button(button_frame, text="Action Bouton", command=lambda: print("Bouton cliqué !"))
action_button.pack(side=tk.LEFT, padx=5, pady=5)


# Créer la frame pour les filtres et l'ajouter au-dessus du tableau principal
filter_frame = tk.Frame(root)  # <-- Correction : définition correcte
filter_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)


"""
# Frame principale pour contenir le tableau principal et le panneau d'informations
main_frame = tk.Frame(root)
main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Configuration du tableau principal (tree)
tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15, selectmode="extended")
"""

# Colonnes du tableau principal
#columns = ("ID", "Sous-titres", "Origine", "Personnage", "Origine 2", "Quête")  # Remplacement de "Audio" par "Personnage"
columns = (
    "ID",
    "(F) Sous-titres",
    "(M) Sous-titres",
    "(F) Voix",
    "(M) Voix",
    "Quête"
)

# Créer une variable pour gérer l'état des boutons radio
gender_var = tk.StringVar(value="homme")  # Par défaut sur "homme"

#definition du Tableau Principal
tree = setup_TableauPrincipal(root, tk, columns)

# Fonction pour configurer le tableau de playlist
playlist_tree = setup_playlist(root, tree, tk, columns, gender_var)

# Bouton pour appliquer tous les filtres
apply_all_filters_button = tk.Button(
    filter_frame,
    text="Appliquer tous les filtres",
    command=lambda: filter_tree_with_filters(tree, filters, file_path, label_count)
    #command=lambda: apply_all_filters(tree, filters)
)
apply_all_filters_button.grid(row=1, column=7, padx=5)

# Ajouter un bouton pour réinitialiser les filtres
reset_filter_button = tk.Button(
    filter_frame,
    text="Réinitialiser les filtres",
    command=lambda: [
        #open_and_display_json(tree, file_path)
        reset_filters(tree, filters, file_path)
    ]
    
)
reset_filter_button.grid(row=1, column=8, padx=5)

# Ajouter le Label pour les lignes correspondantes
label_count = tk.Label(filter_frame, text="Lignes correspondantes : 0")
label_count.grid(row=1, column=9, padx=5)




# Ajouter une case à cocher pour "Afficher N/A"
na_var = tk.BooleanVar(value=True)  # Initialiser à "coché" (True)

checkbox_na = tk.Checkbutton(
    filter_frame,
    text="Afficher N/A",
    variable=na_var,
    command=lambda: filter_NA(tree, na_var)  # Appeler le filtre quand l'état change
)
checkbox_na.grid(row=1, column=12, padx=5)

# Charger les données dans le tableau
open_and_display_json(tree, file_path)

def on_personnage_selected(event):
    personnage_value = event.widget.get()
    update_quete_based_on_personnage(tree, filters, 5, 3, personnage_value)  # 5 = colonne Quête, 3 = colonne Personnage

def on_quete_selected(event):
    quete_value = event.widget.get()
    update_personnage_based_on_quete(
        tree,
        filters,
        quete_column_index=5,
        personnage_column_indexes=(3, 4),  # Les indices des colonnes "(F) Voix" et "(M) Voix"
        quete_value=quete_value
    )


def resize_columns(event):
    toggle_columns(tree, playlist_tree,  filters, gender_var)   

# Créer les champs de filtre uniquement pour les colonnes sélectionnées
filters = []  # Initialisation de la liste des filtres
# Colonnes pour lesquelles les filtres seront activés
#filterable_columns = columns # ca fait planter la gestion homme femme
# Initialisation explicite des filtres
# Initialisation des filtres avec labels et widgets
filters = []

# Colonnes configurables
columns = ["ID", "(F) Sous-titres", "(M) Sous-titres", "(F) Voix", "(M) Voix", "Quête"]

# Création des filtres avec labels explicites
for i, column in enumerate(columns):
    label = tk.Label(filter_frame, text=f"Filtre {column}")
    label.grid(row=0, column=i, padx=5)

    if column in ["(F) Voix", "(M) Voix", "Quête"]:  # ComboBox
        entry = ttk.Combobox(filter_frame, state="readonly")
        if column == "(F) Voix":
            entry["values"] = initialize_personnage_droplist(tree, 3)
            entry.set("Tous")
            entry.bind("<<ComboboxSelected>>", on_personnage_selected)
        elif column == "(M) Voix":
            entry["values"] = initialize_personnage_droplist(tree, 4)
            entry.set("Tous")
            entry.bind("<<ComboboxSelected>>", on_personnage_selected)
        elif column == "Quête":
            entry["values"] = initialize_quete_droplist(tree, 5)
            entry.set("Toutes")
            entry.bind("<<ComboboxSelected>>", on_quete_selected)
    else:  # TextBox
        entry = tk.Entry(filter_frame)

    # Placer les widgets
    entry.grid(row=1, column=i, padx=5)
    filters.append((column, label, entry))  # Ajouter le label et le widget à la liste des filtres




# Bouton radio pour "Homme"
radio_homme = tk.Radiobutton(
    filter_frame,
    text="Homme",
    variable=gender_var,
    value="homme",
    command=lambda: toggle_columns(tree, playlist_tree, filters, gender_var)  # Appeler la fonction de mise à jour des colonnes
)
radio_homme.grid(row=1, column=10, padx=5)

# Bouton radio pour "Femme"
radio_femme = tk.Radiobutton(
    filter_frame,
    text="Femme",
    variable=gender_var,
    value="femme",
    command=lambda: toggle_columns(tree, playlist_tree,  filters, gender_var)  # Appeler la fonction de mise à jour des colonnes
)
radio_femme.grid(row=1, column=11, padx=5)

filter_tree_with_filters(tree, filters, file_path, label_count)




# Lier les événements du tableau principal
tree.bind("<Button-3>", lambda event: select_and_add_to_playlist(event, tree, playlist_tree, tk))
tree.bind("<<TreeviewSelect>>", lambda event: SelectionLigne(event, tree, gender_var))  # Sélectionner une ligne pour afficher les détails

# Lier l'événement de redimensionnement
root.bind("<Configure>", resize_columns)

# Lancer la boucle principale de l'application
root.mainloop()
