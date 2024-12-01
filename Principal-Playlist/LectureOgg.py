import os, json
import subprocess

import tempfile
import shutil
import pygame

import global_vars  # Importer les variables globales



import global_vars  # Importer les variables globales

def stop_sound():
    #"""Arrête le son en cours de lecture."""
    pygame.mixer.music.stop()


def play_ogg_file(file_path):
    # """Joue un fichier .ogg, en arrêtant le son précédent."""
    try:
        # Initialiser pygame
        pygame.mixer.init()
        
        # Arrêter tout son en cours de lecture
        stop_sound()

        # Charger le fichier .ogg
        pygame.mixer.music.load(file_path)
        #print(f"Lecture de : {file_path}")

        # Jouer le fichier audio
        pygame.mixer.music.play()

    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")

def generate_audio_path(audio_value):
    # Vérifier si audio_value est valide
    if audio_value == global_vars.pas_Info:
        return False

    # Reconstruire le chemin
    try:
        # Remplacer '{}' par le chemin de localisation completn'existe pas
        if "{}" in audio_value:
            audio_value = audio_value.replace("{}", global_vars.CheminLocalization + global_vars.CheminLangue)

        # Remplacer l'extension '.wem' par '.ogg'
        if audio_value.endswith(".wem"):
            audio_value = audio_value[:-4] + ".ogg"

        # Ajouter le chemin racine
        full_path = global_vars.project_path + audio_value
        print(f"chemin du son : {full_path}")
        return full_path
    except Exception as e:
        print(f"Erreur lors de la génération du chemin : {e}")
        return False

def JouerAudio(audio_value):
    #test_path = r"D:\_CyberPunk-Creation\Dialogues-Multi\source\raw\ep1\localization\fr-fr\vo\judy_q307_f_2e6b76cd023bc000.ogg"
    # Arrêter tout son en cours de lecture
    sound_Path = generate_audio_path(audio_value)
    sound_Path = convert_wem_to_ogg_if_needed(sound_Path)
    if sound_Path:
        play_ogg_file(sound_Path)
    else:
        pygame.mixer.init()
        # Arrêter tout son en cours de lecture
        stop_sound()


# Définir la fonction de conversion
def convert_wem_to_ogg_if_needed(ogg_path):
    # Vérifier si le fichier .ogg existe déjà
    if os.path.exists(ogg_path):
        return ogg_path
    else :
        # Construire le chemin du fichier .wem correspondant
        print(f"chemin du ogg_path : {ogg_path}")
        wem_path = ogg_path.replace("/raw/", "/archive/").replace(".ogg", ".wem")
        print(f"chemin du wem_path : {wem_path}")
        # Vérifier si le fichier .wem existe
        if not os.path.exists(wem_path):
            raise FileNotFoundError(f"Le xxx fichier .wem correspondant n'existe pas : {wem_path}")

        # Créer les dossiers nécessaires pour le fichier .ogg s'ils n'existent pas
        ogg_dir = os.path.dirname(ogg_path)
        if not os.path.exists(ogg_dir):
            os.makedirs(ogg_dir)

        # Créer un répertoire temporaire spécifique à côté du script
        temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # Convertir le fichier .wem en .ogg
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg", dir=temp_dir) as temp_ogg_file:
            temp_ogg_path = temp_ogg_file.name

        conversion_command = [
            global_vars.ww2ogg_path,
            wem_path,
            "--pcb",
            global_vars.codebooks_path,
            "-o",
            temp_ogg_path
        ]
        try:
            subprocess.run(conversion_command, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Erreur lors de la conversion du fichier .wem en .ogg : {e}")

        # Fermer le fichier temporaire avant d'utiliser revorb
        temp_ogg_file.close()

        # Appliquer revorb directement au fichier temporaire .ogg généré
        revorb_command = [
            global_vars.revorb_path,
            temp_ogg_path
        ]
        try:
            subprocess.run(revorb_command, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Erreur lors de l'application de revorb : {e}")

        # Déplacer le fichier revorb .ogg à l'emplacement souhaité
        shutil.move(temp_ogg_path, ogg_path)

        return ogg_path
    

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