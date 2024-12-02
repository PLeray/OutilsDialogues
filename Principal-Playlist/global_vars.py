import configparser, os

playlist_count_label = None  # Définition initiale

playlist_name_label = None  # Définition initiale

principal_count = None  # Définition initiale

vSexe  = None  # Définition initiale

nombre_Ligne = "number of lines"

setToAll = "ALL"

filter_with = "Filter with "

vHomme = "V as man"
vFemme = "V as woman"

pas_Info = "NOTHING" # Définition initiale

titleCol_ID = "ID"
titleCol_F_SubTitle = "(F) Subtitles"
titleCol_M_SubTitle = "(M) Subtitles"
titleCol_F_Voice = "(F) Voice"
titleCol_M_Voice = "(M) Voice"
titleCol_Quest = "Quest"

columns = (titleCol_ID, titleCol_F_SubTitle, titleCol_M_SubTitle, titleCol_F_Voice, titleCol_M_Voice, titleCol_Quest)
columns_homme = [titleCol_ID, titleCol_M_SubTitle, titleCol_M_Voice, titleCol_Quest]
columns_femme = [titleCol_ID, titleCol_F_SubTitle, titleCol_F_Voice, titleCol_Quest]

#utilisé dans la sauvegarde et BDD .json Attention !
data_ID = "stringId"
data_F_SubTitle = "femaleVariant"
data_M_SubTitle = "maleVariant"
data_F_Voice = "female_vo_path"
data_M_Voice = "male_vo_path"
data_Quest = "quest_path"

bdd_Localisation_Json="D:\\_CyberPunk-Creation\\BDDDialogues\\BDDjson\\Base_fr-fr.json"

#bdd_Zhincore = r"D:\_CyberPunk-Creation\BDDDialogues\testReduit.json"
bdd_Zhincore = r"D:\_CyberPunk-Creation\BDDDialogues\subtitles.DIVQuO_-.json"

ww2ogg_path = ""
revorb_path = ""
codebooks_path = ""
project_path = ""

# Variables globales
#CheminRacine = "D:\_CyberPunk-Creation\DialogueFR/source/raw/" # A suprimer
CheminLocalization = "localization/"
CheminLangue = "fr-fr"

def initConfigGlobale():
    config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
    config = read_config(config_file_path)
    global ww2ogg_path
    global revorb_path
    global codebooks_path
    global project_path
    ww2ogg_path = config['WW2OGG_PATH']
    revorb_path = config['REVORB_PATH']
    codebooks_path = config['CODEBOOKS_PATH']
    project_path = config['PROJECT_PATH'] + "/source/raw/"

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
        'CODEBOOKS_PATH': config.get('Paths', 'CODEBOOKS_PATH'),
        'PROJECT_PATH': config.get('Paths', 'PROJECT_PATH')
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


"""
# Chemin de votre projet
project_path = r"D:\_CyberPunk-Creation\DialogueFR"

# Rechercher les sous-dossiers sous "localization"
localization_subfolders = find_localization_subfolders(project_path)

print("Sous-dossiers trouvés sous 'localization' :")
for folder in localization_subfolders:
    print(f"- {folder}")
"""

