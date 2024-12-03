import os
import subprocess

import tempfile
import shutil
import pygame

import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment

import global_vars  # Importer les variables globales

from general_functions import extraire_localise_path

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

"""
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
        #print(f"chemin du fichier localiser : {full_path}")
        return full_path
    except Exception as e:
        print(f"Erreur lors de la génération du chemin : {e}")
        return False
"""        



def JouerAudio(audio_value):
    #test_path = r"D:\_CyberPunk-Creation\Dialogues-Multi\source\raw\ep1\localization\fr-fr\vo\judy_q307_f_2e6b76cd023bc000.ogg"
    # Arrêter tout son en cours de lecture
    sound_Path = extraire_localise_path(audio_value)
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

        try:
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
        
        finally:
            # Supprimer le dossier temporaire à la fin
            if os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir)
                    print(f"Dossier temporaire supprimé : {temp_dir}")
                except Exception as e:
                    print(f"Erreur lors de la suppression du dossier temporaire : {e}")

        return ogg_path            

def nom_playlist():    # Récupérer le texte du Label et le nom de la playlist sans extension
    texte_playlist = global_vars.playlist_name_label.cget("text")
    nom_playlist = texte_playlist.split(" : ")[1]  # Extraire le nom de la playlist
    nom_sans_extension = os.path.splitext(nom_playlist)[0] 
    #print(f"nom_sans_extension : {nom_sans_extension}.")
    return nom_sans_extension

# Fonction pour fusionner les fichiers audio de la playlist
def fusionnerPlaylist(playlist_tree):
    # Liste des fichiers audio à fusionner
    fichiers_audio = []
    items = playlist_tree.get_children()

    if not items:
        print("La playlist est vide. Impossible de fusionner.")
        return

    for item in items:
        selected_values = playlist_tree.item(item, "values")
        selected_gender = global_vars.vSexe.get()
        
        if selected_gender == global_vars.vHomme:
            audio_value = selected_values[4]
        else:
            audio_value = selected_values[3]

        audio_value = extraire_localise_path(audio_value)
        #print(f"chemin audio {audio_value}.")
        if audio_value:
            fichiers_audio.append(audio_value)
        else:
            print(f"Aucun fichier audio trouvé pour l'élément {item}.")

    if not fichiers_audio:
        print("Aucun fichier audio valide trouvé pour fusionner.")
        return

    try:
        # Charger le premier fichier
        fusion_audio = AudioSegment.from_file(fichiers_audio[0], format="ogg")

        # Concaténer les fichiers restants
        for fichier in fichiers_audio[1:]:
            audio = AudioSegment.from_file(fichier, format="ogg")
            fusion_audio += audio

        # Demander où sauvegarder le fichier fusionné
        root = tk.Tk()
        root.withdraw()  # Masquer la fenêtre principale

        nom_sans_extension = nom_playlist()
        
        fichier_sauvegarde = filedialog.asksaveasfilename(
            title="Enregistrer le fichier fusionné",
            initialfile=f"{nom_sans_extension}.ogg",  # Nom par défaut basé sur la playlist
            defaultextension=".ogg",
            filetypes=[("Fichiers OGG", "*.ogg")],
        )
        root.destroy()  # Assurez-vous de détruire la fenêtre après utilisation
        if fichier_sauvegarde:
            # Exporter le fichier fusionné
            fusion_audio.export(fichier_sauvegarde, format="ogg")
            print(f"Fichier fusionné sauvegardé avec succès dans {fichier_sauvegarde}")
        else:
            print("Opération annulée. Aucun fichier sauvegardé.")
            return
        del fusion_audio  # Libérer les ressources AudioSegment

    except Exception as e:
        print(f"Erreur lors de la fusion des fichiers : {e}")

