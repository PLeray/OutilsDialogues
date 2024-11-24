import pygame

# Variables globales
CheminRacine = "D:\_CyberPunk-Creation\DialogueFR/source/raw/"
CheminLocalization = "localization/"
CheminLangue = "fr-fr"

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
    if audio_value == "N/A":
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
    if sound_Path:
        play_ogg_file(sound_Path)
    else:
        pygame.mixer.init()
        # Arrêter tout son en cours de lecture
        stop_sound()