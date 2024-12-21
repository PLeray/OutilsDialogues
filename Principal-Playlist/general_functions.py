import configparser, os, json, csv
#from tkinter import filedialog, Tk
#from threading import Thread
import global_variables  # Importer les variables globales



def initConfigGlobale():
    config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
    config = read_config(config_file_path)
    global_variables.ww2ogg_path = config['WW2OGG_PATH']
    global_variables.revorb_path = config['REVORB_PATH']
    global_variables.codebooks_path = config['CODEBOOKS_PATH']
    global_variables.path_dernier_projet = global_variables.user_config.get("SETTINGS", "PROJECT")

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

def localise_path(chemin_generic):    
    # Remplacer '{}' par le chemin de localisation completn'existe pas
    chemin_vrai = chemin_generic
    if "{}" in chemin_generic:
        chemin_vrai = chemin_generic.replace("{}", global_variables.CheminLocalization + global_variables.CheminLangue)
    return chemin_vrai
        
def Delocalise_project_path(Project_path):
    nomProject = os.path.splitext(os.path.basename(Project_path))[0]
    directory_path = os.path.dirname(Project_path)

    #chemin_generic =  nomProject + "_files/{{}}/" + nomProject + "DIC.csv" 
    #chemin_generic = "{}_files/{{}}/{}DIC.csv".format(nomProject, nomProject)
    chemin_generic = f"{directory_path}/{nomProject}_files/{{}}/{nomProject}DIC.csv"
    print(f"chemin chemin_generic : {chemin_generic}")  
    return chemin_generic
    
def get_SousTitres_from_csv(file_path, string_id):
    """
    Retourne femaleVariant et maleVariant pour un stringId donné dans un fichier CSV.
    :param file_path: Chemin vers le fichier CSV.
    :param string_id: Identifiant unique (stringId) à rechercher.
    :return: Dictionnaire avec femaleVariant et maleVariant ou None si non trouvé.
    """
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row[global_variables.data_ID] == string_id: 
                    return {
                        global_variables.data_F_SubTitle: row.get(global_variables.data_F_SubTitle, ""),
                        global_variables.data_M_SubTitle: row.get(global_variables.data_M_SubTitle, ""),
                        global_variables.data_F_Voice: row.get(global_variables.data_F_Voice, ""),
                        global_variables.data_M_Voice: row.get(global_variables.data_M_Voice, "")
                    }
        print(f"Aucun résultat trouvé pour stringId : {string_id}")
        return None
    except FileNotFoundError:
        print(f"Le fichier csv {file_path} n'existe pas.")
        return None
    except KeyError as e:
        print(f"Colonne manquante dans le fichier CSV : {e}")
        return None


def get_SousTitres_by_id(file_path, string_id):
    try:
        # Charger le fichier JSON
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Parcourir les entrées dans le fichier JSON
        entries = data["Data"]["RootChunk"]["root"]["Data"]["entries"]
        for entry in entries:
            if entry["stringId"] == str(string_id):  # Vérification du stringId
                return {
                    global_variables.data_F_SubTitle: entry.get(global_variables.data_F_SubTitle, ""),
                    global_variables.data_M_SubTitle: entry.get(global_variables.data_M_SubTitle, "")
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


def charger_sous_titres_from_JSON_playlist(file_path, first_entry_only=False):
    sous_titres = []  # Liste pour stocker tous les sous-titres
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            playlist_data = json.load(file)

            if len(playlist_data) > 0:  # Vérifier si le fichier contient des données
                for index, entry in enumerate(playlist_data):
                    prefix = ""
                    recup_Quete = entry[global_variables.data_Quest]
                    fichierQuete = ""
                    if recup_Quete.lower().endswith(".csv"):
                        fichierQuete = "data/projet/" + localise_path(recup_Quete)
                        result = get_SousTitres_from_csv(fichierQuete, entry[global_variables.data_ID])
                        if result: prefix = result[global_variables.data_F_Voice]
                    else:
                        quete_path = extraire_localise_path(recup_Quete)
                        if isinstance(quete_path, str):  # Vérifie si c'est une chaîne
                            fichierQuete = quete_path + ".json.json"
                        result = get_SousTitres_by_id(fichierQuete, entry[global_variables.data_ID])

                    if result:
                        female_text = result[global_variables.data_F_SubTitle]
                        male_text = result[global_variables.data_M_SubTitle]
                    else:
                        female_text = "(NO TRADUCTION)"
                        male_text = "(NO TRADUCTION)"  

                    if not male_text or male_text == global_variables.pas_Info:
                        male_text = female_text
                    if not female_text or female_text == global_variables.pas_Info:
                        female_text = male_text

                    selected_gender = global_variables.vSexe.get()
                    if selected_gender == global_variables.vHomme:
                        perso = get_Perso_from_Wem(entry[global_variables.data_F_Voice])  # Valeur pour homme
                        sous_titre = male_text
                    else:
                        perso = get_Perso_from_Wem(entry[global_variables.data_M_Voice])  # Valeur pour femme
                        sous_titre = female_text
                    
                    # Ajouter le sous-titre et le perso comme objet
                    sous_titres.append({global_variables.data_ID: entry[global_variables.data_ID], "perso": perso, "sous_titre": sous_titre, "type": prefix})

                    # Si l'option est activée, ne traiter que la première entrée
                    if first_entry_only:
                        break

            else:
                print("Le fichier est vide ou mal formaté.")
    else:
        print("Pas de fichier playlist fourni.")
    
    
    return sous_titres

