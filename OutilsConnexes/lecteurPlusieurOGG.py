import os
import pygame

def lire_ogg_en_sequence(dossier):
    """
    Lit tous les fichiers audio .ogg dans un dossier un par un.
    :param dossier: Chemin du dossier contenant les fichiers .ogg
    """
    # Initialiser pygame mixer
    pygame.mixer.init()
    
    # Obtenir la liste des fichiers .ogg dans le dossier
    fichiers = [f for f in os.listdir(dossier) if f.endswith('.ogg')]
    fichiers.sort()  # Trier les fichiers pour les lire dans un ordre spécifique (optionnel)

    if not fichiers:
        print("Aucun fichier .ogg trouvé dans le dossier.")
        return

    print(f"Fichiers trouvés : {fichiers}")

    # Lire chaque fichier séquentiellement
    for fichier in fichiers:
        chemin_complet = os.path.join(dossier, fichier)
        try:
            print(f"Lecture de : {fichier}")
            pygame.mixer.music.load(chemin_complet)
            pygame.mixer.music.play()
            
            # Attendre que la lecture soit terminée
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier {fichier} : {e}")

    # Quitter pygame mixer
    pygame.mixer.quit()

# Exemple d'utilisation
chemin_dossier = "chemin/vers/votre/dossier"
chemin_dossier = r"D:\_CyberPunk-Creation\OutilsDialogues\OutilsConnexes\Ogg"
lire_ogg_en_sequence(chemin_dossier)
