# fichier: gui_functions.py
import tkinter as tk

import json

from tkinter import ttk
#from typing import Dict
#from custom_types import Dialogue
from data_loader import load_json

from LectureOgg import JouerAudio, generate_audio_path

_pasAttribuer = "RIEN"

#definition du Tableau Principal
def setup_TableauPrincipal(root, tk, columns):
    # Frame principale pour contenir le tableau principal et le panneau d'informations
    main_frame = tk.Frame(root)
    main_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)  # Remplacez fill=tk.BOTH par fill=tk.X

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
        id = key

        #TRADUCTION !
        # Récupérer la quête
        quete = entry.get("_path", _pasAttribuer)
        audio_path = generate_audio_path(quete)

        fichierQuete = ""        
        if isinstance(audio_path, str):  # Vérifie si c'est une chaîne
            fichierQuete = audio_path + ".json.json"

        result = get_variants_by_id(fichierQuete, id)
        if result:
            #print(f"Female Variant: {result['femaleVariant']}")
            #print(f"Male Variant: {result['maleVariant']}")
            female_text = result['femaleVariant']
            male_text = result['maleVariant']
        else:
            #print("String ID non trouvé.")
            female_text = ""
            male_text = ""

        # Récupérer les informations pour 'female'
        """
        female_text = entry.get("female", {}).get("text", _pasAttribuer)
        """
        female_vo = entry.get("female", {}).get("vo", {}).get("main", _pasAttribuer)

        # Récupérer les informations pour 'male'
        """
        male_text = entry.get("male", {}).get("text", _pasAttribuer)        
        """
        male_vo = entry.get("male", {}).get("vo", {}).get("main", _pasAttribuer)

        # Vérifier si 'male_vo' ou 'female_vo' contient "v_"
        isV = "v_" in (male_vo or "") or "v_" in (female_vo or "")         
        
        if not male_text or male_text == _pasAttribuer:
            male_text = female_text        
        if not female_text or female_text == _pasAttribuer:
            female_text = male_text # a Confirmer si ca existe !?
       
        if not male_vo or male_vo == _pasAttribuer:       
            if isV :
                male_vo = female_vo.replace("_f_", "_m_")  
                # peut etre que le son n'existe pas -->  verifier si fichier existe avec generate_audio_path(male_vo)
            else :
                male_vo = female_vo
      
        # Insérer une ligne dans le Treeview
        tree.insert("", tk.END, values=(
            id,           # ID
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


def get_variants_by_id(file_path, string_id):
    """
    Cherche les variantes (femaleVariant et maleVariant) correspondant à un stringId donné dans un fichier JSON.

    :param file_path: Chemin du fichier JSON.
    :param string_id: stringId à rechercher.
    :return: Un dictionnaire contenant "femaleVariant" et "maleVariant", ou None si le stringId n'est pas trouvé.
    """
    try:
        # Charger le fichier JSON
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Parcourir les entrées dans le fichier JSON
        entries = data["Data"]["RootChunk"]["root"]["Data"]["entries"]
        for entry in entries:
            if entry["stringId"] == str(string_id):  # Vérification du stringId
                return {
                    "femaleVariant": entry.get("femaleVariant", ""),
                    "maleVariant": entry.get("maleVariant", "")
                }
        
        # Si le stringId n'est pas trouvé
        return None

    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        #print(f"Erreur lors du traitement du fichier : {e}")
        return None