import configparser, os, json
from tkinter import filedialog, Tk
from threading import Thread
import global_variables  # Importer les variables globales



def initConfigGlobale():
    config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
    config = read_config(config_file_path)
    global_variables.ww2ogg_path = config['WW2OGG_PATH']
    global_variables.revorb_path = config['REVORB_PATH']
    global_variables.codebooks_path = config['CODEBOOKS_PATH']

# Lire les chemins depuis le fichier de configuration
def read_config(config_path):
    config = configparser.ConfigParser()
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Le fichier de configuration est introuvable : {config_path}")
    config.read(config_path)
    if 'Paths' not in config:
        raise configparser.NoSectionError('Paths')
    return {
        'WW2OGG_PATH': config.get('Paths', 'WW2OGG_PATH'),
        'REVORB_PATH': config.get('Paths', 'REVORB_PATH'),
        'CODEBOOKS_PATH': config.get('Paths', 'CODEBOOKS_PATH')
        #,'PROJECT_PATH': config.get('Paths', 'PROJECT_PATH')
    }

def find_localization_subfolders(project_path):
    """
    Recherche un dossier nommé "localization" dans les sous-dossiers d'un chemin donné,
    et retourne une liste de tous les sous-dossiers immédiats de "localization".
    """
    localization_path = None

    # Parcourir les sous-dossiers pour trouver "localization"
    for root, dirs, files in os.walk(project_path):
        if "localization" in dirs:
            localization_path = os.path.join(root, "localization")
            break  # On s'arrête dès qu'on trouve "localization"

    # Si "localization" n'est pas trouvé, retourner une liste vide
    if not localization_path:
        print(f"Dossier 'localization' non trouvé dans {project_path}")
        return []

    # Lister uniquement les sous-dossiers immédiats de "localization"
    subfolders = [
        name for name in os.listdir(localization_path)
        if os.path.isdir(os.path.join(localization_path, name))
    ]

    return subfolders

def extraire_localise_path(chemin_generic):  #pour recontruire chemin avec {}
    # Vérifier si chemin_generic est valide
    if chemin_generic == global_variables.pas_Info:
        return False

    # Reconstruire le chemin
    try:
        # Remplacer '{}' par le chemin de localisation completn'existe pas
        if "{}" in chemin_generic:
            chemin_generic = chemin_generic.replace("{}", global_variables.CheminLocalization + global_variables.CheminLangue)

        # Dans le cas des fichiers voix, Remplacer l'extension '.wem' par '.ogg'
        if chemin_generic.endswith(".wem"):
            chemin_generic = chemin_generic[:-4] + ".ogg"

        # Ajouter le chemin racine
        full_path = global_variables.project_path + chemin_generic
        #print(f"chemin du fichier localiser : {full_path}")
        return full_path
    except Exception as e:
        print(f"Erreur lors de la génération du chemin : {e}")
        return False

def get_SousTitres_by_id(file_path, string_id):
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

def get_Perso_from_Wem(value):
    last_part = value.split("/")[-1]  # Obtenir la partie après le dernier "/"
    personnage = last_part.split("_")[0]  # Obtenir la partie avant le premier "_"
    return personnage

def nom_playlist():    # Récupérer le texte du Label et le nom de la playlist sans extension
    texte_playlist = global_variables.playlist_name_label.cget("text")
    nom_playlist = texte_playlist.split(" : ")[1]  # Extraire le nom de la playlist
    nom_sans_extension = os.path.splitext(nom_playlist)[0] 
    #print(f"nom_sans_extension : {nom_sans_extension}.")
    return nom_sans_extension

