# Variables globlaes du projet

playlist_name_label = None  # Définition initiale
playlist_count_label = None  # Définition initiale
principal_count = None  # Définition initiale

vSexe  = None  # Définition initiale

nombre_Ligne = "number of lines"

setToAll = "ALL"
pas_Info = "NOTHING" # Définition initiale

filter_with = "Filter with "

vHomme = "V as man"
vFemme = "V as woman"

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

bdd_Localisation_Json="data/BDDjson/Base_fr-fr.json"

#bdd_Zhincore = r"D:\_CyberPunk-Creation\BDDDialogues\testReduit.json"
#bdd_Zhincore = r"D:\_CyberPunk-Creation\BDDDialogues\subtitles.DIVQuO_-.json"
bdd_Zhincore = "data/BDDjson/subtitles.DIVQuO_-.json"

ww2ogg_path = ""
revorb_path = ""
codebooks_path = ""

project_path = ""

# Variables globales
#CheminRacine = "D:\_CyberPunk-Creation\DialogueFR/source/raw/" # A suprimer
CheminLocalization = "localization/"
CheminLangue = "fr-fr"
