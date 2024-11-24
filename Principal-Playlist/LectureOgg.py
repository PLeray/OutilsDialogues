import pygame

# Variables globales
CheminRacine = "D:\_CyberPunk-Creation\DialogueFR/source/raw/"
CheminLocalization = "localization/"
CheminLangue = "fr-fr"

def stop_sound():
    #"""Arrête le son en cours de lecture."""
    pygame.mixer.music.stop()


def play_ogg_file(file_path, on_end_callback=None):
    """
    Joue un fichier audio et appelle un callback à la fin.
    :param file_path: Chemin vers le fichier audio.
    :param on_end_callback: Fonction à appeler à la fin du morceau.
    """
    try:
        initialize_audio()  # Initialiser le module audio

        # Arrêter tout son en cours de lecture
        stop_sound()

        pygame.mixer.music.load(file_path)  # Charger le fichier audio
        pygame.mixer.music.play()  # Jouer le fichier audio

        # Ajouter un événement pour détecter la fin de la musique
        if on_end_callback:
            pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Déclenche un événement à la fin
            pygame.event.post(pygame.event.Event(pygame.USEREVENT))
    except pygame.error as e:
        print(f"Erreur lors de la lecture de l'audio : {e}")        


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

def JouerAudio(audio_value, on_end_callback=None):
    #test_path = r"D:\_CyberPunk-Creation\Dialogues-Multi\source\raw\ep1\localization\fr-fr\vo\judy_q307_f_2e6b76cd023bc000.ogg"
    # Arrêter tout son en cours de lecture
    sound_Path = generate_audio_path(audio_value)
    if sound_Path:
        print(f"Lecture de : {audio_value}")
        play_ogg_file(sound_Path,on_end_callback)
    else:
        initialize_audio()
        # Arrêter tout son en cours de lecture
        stop_sound()


def initialize_audio():
    """
    Initialise le système audio de pygame si ce n'est pas déjà fait.
    """
    if not pygame.mixer.get_init():
        pygame.mixer.init()        