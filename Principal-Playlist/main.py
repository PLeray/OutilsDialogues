# fichier: main.py
import tkinter as tk
from tkinter import ttk
import time

import global_variables  # Importer les variables globales
from general_functions import initConfigGlobale, find_localization_subfolders

from recherche_functions import open_and_display_json, SelectionLigne, setup_TableauPrincipal
from playlist_functions import select_and_add_to_playlist, setup_playlist
from filtrage import toggle_columns, filter_NA, reset_filters, filter_tree_with_filters, initialize_personnage_droplist, initialize_quete_droplist, update_quete_based_on_personnage, update_personnage_based_on_quete

from CuserConfig import UserConfig
from CstepBlockApp import StepBlockApp

def show_hello_world():
    # Créer une nouvelle fenêtre
    window = tk.Tk()
    window.title("Message")  # Titre de la fenêtre
    window.geometry("200x100")  # Dimensions de la fenêtre

    # Ajouter une étiquette avec le message
    label = tk.Label(window, text="Hello World!")
    label.pack(pady=20)  # Ajouter un peu d'espace autour

    # Ajouter un bouton pour fermer la fenêtre
    close_button = tk.Button(window, text="Fermer", command=window.destroy)
    close_button.pack(pady=10)

    # Lancer la boucle principale
    window.mainloop()


def ouvrir_projet(root):
    # Vérifier si la fenêtre est déjà ouverte
    if global_variables.fenetre_projet is not None:
        print("La fenêtre de projet est déjà ouverte.")
        return

    # Créer une nouvelle fenêtre
    global_variables.fenetre_projet = tk.Toplevel(root)
    global_variables.fenetre_projet.geometry("600x800")
    global_variables.fenetre_projet.title("Fenêtre Projet")

    # Associer un gestionnaire à la fermeture de cette fenêtre
    global_variables.fenetre_projet.protocol("WM_DELETE_WINDOW", fermer_fenetre_projet)

    # Lancer l'application de projet (utiliser StepBlockApp ou équivalent)
    app = StepBlockApp(global_variables.fenetre_projet)


def fermer_fenetre_projet():
    if global_variables.fenetre_projet is not None:
        global_variables.fenetre_projet.destroy()
        global_variables.fenetre_projet = None
        print("Fenêtre de projet fermée.")


def fermer_application_principale(root):
    # Fermer la fenêtre de projet si elle est ouverte
    if global_variables.fenetre_projet is not None:
        fermer_fenetre_projet()
    # Fermer la fenêtre principale
    root.destroy()
    print("Application principale fermée.")

def long_function():
    # Changer le curseur en icône d'attente
    root.config(cursor="wait")
    root.update_idletasks()  # Actualiser l'interface graphique
    
    # Simuler une opération longue
    time.sleep(5)
    
    # Rétablir le curseur par défaut
    root.config(cursor="")
    root.update_idletasks()

def maj_Langue(str_langue):
    global_variables.CheminLangue = str_langue
    global_variables.bdd_Localisation_Json = "data/BDDjson/Base_" + str_langue + ".json"


# Créer la fenêtre principale
root = tk.Tk()
root.title("Tool to assemble and test dialogue sequences for Cyberpung modding")
root.geometry("1600x800")
root.minsize(1100, 800)

initConfigGlobale()

global_variables.rootAccess = root #initialisation de la variable globale root pour y acceder dans les fonctions

global_variables.user_config = UserConfig("userconfig.ini")
global_variables.user_config.read_or_initialize()

#userconf_data = read_or_initialize_userconf()
#print(f"userconf_data : {userconf_data}")

# Récupérer le chemin du projet
"""
project_path = userconf_data["SETTINGS"].get("PROJECT_WOLVENKIT_PATH")
if not project_path:
    raise ValueError("Le chemin 'PROJECT_WOLVENKIT_PATH' est introuvable ou invalide dans userconf.ini.")

global_variables.project_path = project_path + "/source/raw/"
"""


global_variables.project_path = global_variables.user_config.get("SETTINGS", "PROJECT_WOLVENKIT_PATH") + "/source/raw/"

localization_languages = find_localization_subfolders(global_variables.project_path)

# Créer une frame pour le bouton au-dessus du tableau principal
button_frame = tk.Frame(root)
button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

# Ajouter un bouton "Projet" à gauche de la liste déroulante
project_button = tk.Button(
    button_frame,
    text="Projet",
    command=lambda: ouvrir_projet(root)
)
project_button.pack(side=tk.LEFT, padx=5, pady=5)

# Ajouter une liste déroulante (ComboBox)
language_var = tk.StringVar()
language_dropdown = ttk.Combobox(
    button_frame,
    textvariable=language_var,
    values=localization_languages,  # Langues récupérées par la fonction
    state="readonly",  # Lecture seule pour éviter la modification manuelle
    width=20
)

# Définir une valeur par défaut pour la liste déroulante
#maj_Langue(userconf_data["SETTINGS"].get("LANGUAGE"))

maj_Langue(global_variables.user_config.get("SETTINGS", "LANGUAGE"))


#global_variables.CheminLangue = userconf_data["SETTINGS"].get("LANGUAGE")
global_variables.CheminLangue = global_variables.user_config.get("SETTINGS", "LANGUAGE")

global_variables.bdd_Localisation_Json = "data/BDDjson/Base_" + global_variables.CheminLangue + ".json"
if global_variables.CheminLangue in localization_languages:
    language_dropdown.set(global_variables.CheminLangue)  # Définit la valeur par défaut
else:
    language_dropdown.set("Sélectionnez une langue")  # Définit une valeur par défaut générique

language_dropdown.pack(side=tk.LEFT, padx=5, pady=5)

# Ajouter un texte à droite de la liste déroulante
text_label = tk.Label(button_frame, text="Donner ici queles explications sur souris bouton usage ...", font=("Arial", 10))
text_label.pack(side=tk.LEFT, padx=5, pady=5)


# Ajouter une commande lors de la sélection
def on_language_selected(event):
    global_variables.dataSound = None
    maj_Langue(language_var.get())



    #update_language_userconf(global_variables.CheminLangue)

    global_variables.user_config.set("SETTINGS", "LANGUAGE", global_variables.CheminLangue)


    # mettre ca si on veut les langues des tableau synchro filter_tree_with_filters(tree, filters, global_variables.bdd_Localisation_Json)
    print(f"Langue sélectionnée : {global_variables.CheminLangue}")

language_dropdown.bind("<<ComboboxSelected>>", on_language_selected)

# Créer la frame pour les filtres et l'ajouter au-dessus du tableau principal
filter_frame = tk.Frame(root)  # <-- Correction : définition correcte
filter_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)


# Exemple d'initialisation du Treeview avec un thème compatible
style = ttk.Style()
style.theme_use("default")  # Changez le thème
style.configure("Treeview", rowheight=25)  # Augmentez la hauteur des lignes si nécessaire
style.map(
    "Treeview", 
    background=[("selected", global_variables.Couleur_BgSelectLigne)],  # Couleur pour les lignes sélectionnées
    foreground=[("selected", global_variables.Couleur_TxtSelectLigne)]   # Couleur du texte pour les lignes sélectionnées
)

# Créer une variable pour gérer l'état des boutons radio
global_variables.vSexe = tk.StringVar(value=global_variables.vHomme)  # Par défaut sur "homme"

#definition du Tableau Principal
tree = setup_TableauPrincipal(root, tk, global_variables.columns)

# Fonction pour configurer le tableau de playlist
global_variables.playlist_tree = setup_playlist(root, tree, tk, global_variables.columns)



# Ajouter le Label pour les lignes correspondantes
global_variables.principal_count = tk.Label(filter_frame, text="Nb de lignes : 0")
global_variables.principal_count.grid(row=1, column=9, padx=5)



# Bouton pour appliquer tous les filtres
apply_all_filters_button = tk.Button(
    filter_frame,
    text="Apply all filters ✔️",
    command=lambda: filter_tree_with_filters(tree, filters, global_variables.bdd_Localisation_Json)
    #command=lambda: apply_all_filters(tree, filters)
)
apply_all_filters_button.grid(row=1, column=7, padx=5)

root.bind('<Return>', lambda event: filter_tree_with_filters(tree, filters, global_variables.bdd_Localisation_Json))

# Ajouter un bouton pour réinitialiser les filtres
reset_filter_button = tk.Button(
    filter_frame,
    text="Reset filters ✖️",
    command=lambda: [
        reset_filters(tree, filters, global_variables.bdd_Localisation_Json)
    ]
    
)
reset_filter_button.grid(row=1, column=8, padx=5)

# Ajouter une case à cocher pour "Afficher N/A"
na_var = tk.BooleanVar(value=True)  # Initialiser à "coché" (True)

checkbox_na = tk.Checkbutton(
    filter_frame,
    text="keep lines with " + global_variables.pas_Info,
    variable=na_var,
    command=lambda: filter_NA(tree, na_var)  # Appeler le filtre quand l'état change
)
checkbox_na.grid(row=1, column=12, padx=5)

# Charger les données dans le tableau
open_and_display_json(tree, global_variables.bdd_Localisation_Json)

def on_personnage_selected(event):
    personnage_value = event.widget.get()
    update_quete_based_on_personnage(tree, filters, 5, 3, personnage_value)  # 5 = colonne Quête, 3 = colonne Personnage F
    update_quete_based_on_personnage(tree, filters, 5, 4, personnage_value)  # 5 = colonne Quête, 4 = colonne Personnage M

def on_quete_selected(event):
    quete_value = event.widget.get()
    update_personnage_based_on_quete(
        tree,
        filters,
        quete_column_index=5,
        personnage_column_indexes=(3, 4),  # Les indices des colonnes Voix"
        quete_value=quete_value
    )


def resize_columns(event):
    toggle_columns(tree, global_variables.playlist_tree,  filters)   

# Créer les champs de filtre uniquement pour les colonnes sélectionnées
filters = []  # Initialisation de la liste des filtres

width_mapping = {
    global_variables.titleCol_F_Voice: 15,
    global_variables.titleCol_M_Voice: 15,
    global_variables.titleCol_Quest: 40,
}
# Création des filtres avec labels explicites
for i, column in enumerate(global_variables.columns):
    label = tk.Label(filter_frame, text=f"{global_variables.filter_with}{column}")  #Filter with
    label.grid(row=0, column=i, padx=5)
    """
    if column in [global_variables.titleCol_F_Voice, global_variables.titleCol_M_Voice, global_variables.titleCol_Quest]:  # ComboBox
        entry = ttk.Combobox(filter_frame, state="readonly")
    """


    if column in width_mapping:  # Combobox avec largeur spécifique
        entry = ttk.Combobox(filter_frame, state="readonly", width=width_mapping[column])        
        if column == global_variables.titleCol_F_Voice:
            entry["values"] = initialize_personnage_droplist(tree, 3)
            entry.set(global_variables.setToAll)
            entry.bind("<<ComboboxSelected>>", on_personnage_selected)
        elif column == global_variables.titleCol_M_Voice:
            entry["values"] = initialize_personnage_droplist(tree, 4)
            entry.set(global_variables.setToAll)
            entry.bind("<<ComboboxSelected>>", on_personnage_selected)
        elif column == global_variables.titleCol_Quest:
            entry["values"] = initialize_quete_droplist(tree, 5)
            entry.set(global_variables.setToAll)
            entry.bind("<<ComboboxSelected>>", on_quete_selected)
    else:  # TextBox
        entry = tk.Entry(filter_frame)

    # Placer les widgets
    entry.grid(row=1, column=i, padx=5)
    filters.append((column, label, entry))  # Ajouter le label et le widget à la liste des filtres


# Bouton radio pour "Homme"
radio_homme = tk.Radiobutton(
    filter_frame,
    text=global_variables.vHomme,
    variable=global_variables.vSexe,
    value=global_variables.vHomme,
    command=lambda: toggle_columns(tree, global_variables.playlist_tree, filters)  # Appeler la fonction de mise à jour des colonnes
)
radio_homme.grid(row=1, column=10, padx=5)

# Bouton radio pour "Femme"
radio_femme = tk.Radiobutton(
    filter_frame,
    text=global_variables.vFemme,
    variable=global_variables.vSexe,
    value=global_variables.vFemme,
    command=lambda: toggle_columns(tree, global_variables.playlist_tree,  filters)  # Appeler la fonction de mise à jour des colonnes
)
radio_femme.grid(row=1, column=11, padx=5)

#filter_tree_with_filters(tree, filters, global_variables.bdd_Localisation_Json)




# Lier les événements du tableau principal
tree.bind("<Button-3>", lambda event: select_and_add_to_playlist(event, tree, global_variables.playlist_tree, tk))
tree.bind("<<TreeviewSelect>>", lambda event: SelectionLigne(event, tree))  # Sélectionner une ligne pour afficher les détails

# Lier l'événement de redimensionnement
root.bind("<Configure>", resize_columns)
#root.protocol("WM_DELETE_WINDOW", on_main_close)
# Associer la fermeture de la fenêtre principale
root.protocol("WM_DELETE_WINDOW", lambda: fermer_application_principale(root))

# Lancer la boucle principale de l'application
root.mainloop()

