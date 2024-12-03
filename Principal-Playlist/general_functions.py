import configparser, os, json
from tkinter import filedialog, Tk

import global_vars  # Importer les variables globales

def initConfigGlobale():
    config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
    config = read_config(config_file_path)
    global_vars.ww2ogg_path = config['WW2OGG_PATH']
    global_vars.revorb_path = config['REVORB_PATH']
    global_vars.codebooks_path = config['CODEBOOKS_PATH']
    #global_vars.project_path = config['PROJECT_PATH'] + "/source/raw/"

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
    if chemin_generic == global_vars.pas_Info:
        return False

    # Reconstruire le chemin
    try:
        # Remplacer '{}' par le chemin de localisation completn'existe pas
        if "{}" in chemin_generic:
            chemin_generic = chemin_generic.replace("{}", global_vars.CheminLocalization + global_vars.CheminLangue)

        # Dans le cas des fichiers voix, Remplacer l'extension '.wem' par '.ogg'
        if chemin_generic.endswith(".wem"):
            chemin_generic = chemin_generic[:-4] + ".ogg"

        # Ajouter le chemin racine
        full_path = global_vars.project_path + chemin_generic
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

# _userconf ################
def read_userconf(file_path="userconf.ini"):
    """
    Lit les informations du fichier userconf.ini et retourne les variables sous forme de dictionnaire.

    :param file_path: Chemin du fichier userconf.ini (par défaut dans le répertoire courant).
    :return: Dictionnaire contenant les paramètres du fichier.
    """
    config = configparser.ConfigParser()
    config.optionxform = str  # Respecte la casse des clés

    if os.path.exists(file_path):
        config.read(file_path)
        return {section: dict(config[section]) for section in config.sections()}
    else:
        raise FileNotFoundError(f"Le fichier {file_path} est introuvable.")

    

def read_or_initialize_userconf(file_path="userconf.ini"):
    """
    Lit les informations depuis un fichier userconf.ini ou initialise ce fichier
    si celui-ci n'existe pas. Si le fichier est créé, il demande à l'utilisateur
    le chemin de son projet Wolvenkit via une boîte de dialogue.

    :param file_path: Chemin du fichier userconf.ini (par défaut dans le répertoire courant).
    :return: Dictionnaire contenant les données du fichier ini.
    """
    # Vérifier si le fichier userconf.ini existe
    if os.path.exists(file_path):
        return read_userconf(file_path)
    else:
        # Le fichier n'existe pas : demander le chemin du projet Wolvenkit
        root = Tk()
        root.withdraw()  # Masquer la fenêtre principale de tkinter
        project_path = filedialog.askdirectory(title="Sélectionnez le chemin du projet Wolvenkit where you extracted the localization files (the .wem audios and the subtitle files)")
        root.destroy()

        if not project_path:
            raise ValueError("Aucun chemin sélectionné. Impossible de continuer sans définir PROJECT_WOLVENKIT_PATH.")

        # Initialiser les données
        data = {
            "SETTINGS": {
                "PROJECT_WOLVENKIT_PATH": project_path ,
                "LANGUAGE": "en-us"
            }
        }

        # Sauvegarder les données dans userconf.ini
        save_userconf(data, file_path)

        # Retourner les données initialisées
        return data

def save_userconf(data, file_path="userconf.ini"):
    """
    Sauvegarde les informations dans un fichier userconf.ini, en mettant à jour les sections existantes.
    :param data: Dictionnaire contenant les données à sauvegarder.
                 Format attendu : {"SECTION": {"key": "value", ...}, ...}.
    :param file_path: Chemin du fichier userconf.ini (par défaut dans le répertoire courant).
    """
    config = configparser.ConfigParser()
    config.optionxform = str  # Respecte la casse des clés

    # Lire le fichier existant s'il existe
    if os.path.exists(file_path):
        config.read(file_path)

    # Mettre à jour ou ajouter les nouvelles données
    for section, values in data.items():
        if not config.has_section(section):
            config.add_section(section)
        for key, value in values.items():
            config.set(section, key, str(value))  # Convertir les valeurs en chaînes

    # Écrire les données dans le fichier
    with open(file_path, "w") as configfile:
        config.write(configfile)
    print(f"Les données ont été sauvegardées dans {file_path}.")


def update_language_userconf(new_language, file_path="userconf.ini"):
    """
    Met à jour uniquement la clé LANGUAGE dans le fichier userconf.ini
    tout en préservant les autres paramètres.
    :param new_language: Nouvelle valeur pour LANGUAGE.
    :param file_path: Chemin du fichier userconf.ini (par défaut dans le répertoire courant).
    """
    try:
        # Lire les paramètres existants ou les initialiser s'ils n'existent pas
        settings = read_userconf(file_path)
    except FileNotFoundError:
        # Si le fichier n'existe pas, créer une configuration par défaut
        print(f"{file_path} introuvable. Création d'un fichier par défaut...")
        settings = {"SETTINGS": {"PROJECT_WOLVENKIT_PATH": "/default/path", "LANGUAGE": "en-us"}}
        save_userconf(settings, file_path)

    # Mettre à jour uniquement LANGUAGE
    if "SETTINGS" not in settings:
        settings["SETTINGS"] = {}
    settings["SETTINGS"]["LANGUAGE"] = new_language

    # Sauvegarder les paramètres mis à jour
    save_userconf(settings, file_path)
    print(f"LANGUAGE mis à jour dans {file_path} : {new_language}")


