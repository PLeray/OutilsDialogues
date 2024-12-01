import os
import subprocess
import configparser
import tempfile
import shutil
import pygame

# Variables globales
CheminRacine = "D:\_CyberPunk-Creation\DialogueFR/source/raw/"
CheminLocalization = "localization/"
CheminLangue = "fr-fr"

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
        # Remplacer '{}' par le chemin de localisation complet
        if "{}" in audio_value:
            audio_value = audio_value.replace("{}", CheminLocalization + CheminLangue)

        # Remplacer l'extension '.wem' par '.ogg'
        if audio_value.endswith(".wem"):
            audio_value = audio_value[:-4] + ".ogg"

        # Ajouter le chemin racine
        full_path = CheminRacine + audio_value
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
        config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
        config = read_config_conversionWem(config_file_path)
        ww2ogg_path = config['WW2OGG_PATH']
        revorb_path = config['REVORB_PATH']
        codebooks_path = config['CODEBOOKS_PATH']

        # Construire le chemin du fichier .wem correspondant
        wem_path = ogg_path.replace("\\raw\\", "\\archive\\").replace(".ogg", ".wem")

        # Vérifier si le fichier .wem existe
        if not os.path.exists(wem_path):
            raise FileNotFoundError(f"Le fichier .wem correspondant n'existe pas : {wem_path}")

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
            ww2ogg_path,
            wem_path,
            "--pcb",
            codebooks_path,
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
            revorb_path,
            temp_ogg_path
        ]
        try:
            subprocess.run(revorb_command, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Erreur lors de l'application de revorb : {e}")

        # Déplacer le fichier revorb .ogg à l'emplacement souhaité
        shutil.move(temp_ogg_path, ogg_path)

        return ogg_path
    

# Lire les chemins depuis le fichier de configuration
def read_config_conversionWem(config_path):
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
    }