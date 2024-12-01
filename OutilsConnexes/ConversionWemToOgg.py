import os
import subprocess
import configparser
import tempfile
import shutil

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

# Exemple d'utilisation
# Définir le chemin du fichier config.ini au même endroit que le script
# config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")

try:
    #config = read_config_conversionWem(config_file_path)
    ogg_file_path = r"D:\_CyberPunk-Creation\DialogueEN\source\raw\base\localization\en-us\vo\alt_q108_f_173f906f62351000.ogg"

    result_path = convert_wem_to_ogg_if_needed(ogg_file_path)
    print(f"Fichier .ogg disponible : {result_path}")
except FileNotFoundError as e:
    print(e)
except configparser.NoSectionError as e:
    print(f"Erreur de configuration : {e}")
except RuntimeError as e:
    print(e)
