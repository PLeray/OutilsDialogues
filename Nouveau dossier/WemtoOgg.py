# Script Python pour convertir tous les fichiers WEM en OGG de manière récursive
import os
import subprocess

# Définition des chemins de fichiers
input_dir =  r"D:\_CyberPunk-Creation\Dialogues-Multi\source\archive\base\localization\fr-fr"      # D:\_CyberPunk-Creation\Dialogues-Multi\source\archive\ep1\localization\fr-fr
output_dir = r"D:\_CyberPunk-Creation\Dialogues-Multi\source\raw\base\localization\fr-fr"       # D:\_CyberPunk-Creation\Dialogues-Multi\source\raw\ep1\localization\fr-fr
tools_dir = r"D:\_CyberPunk-Creation\TestConversion\Outils"
pcb_file = os.path.join(tools_dir, "packed_codebooks_aoTuV_603.bin")

# Vérifier si le dossier de sortie existe, sinon le créer
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Récupérer la liste de tous les fichiers WEM dans les sous-dossiers
wem_files = []
for root, _, files in os.walk(input_dir):
    for file_name in files:
        if file_name.endswith(".wem"):
            wem_files.append(os.path.join(root, file_name))

# Parcours de tous les fichiers WEM avec un compteur
total_files = len(wem_files)
for index, wem_file in enumerate(wem_files, start=1):
    relative_path = os.path.relpath(os.path.dirname(wem_file), input_dir)
    output_subdir = os.path.join(output_dir, relative_path)

    # Créer le sous-dossier de sortie s'il n'existe pas
    if not os.path.exists(output_subdir):
        os.makedirs(output_subdir)

    base_name = os.path.splitext(os.path.basename(wem_file))[0]
    ogg_file_intermediate = os.path.join(os.path.dirname(wem_file), f"{base_name}.ogg")
    ogg_file_final = os.path.join(output_subdir, f"{base_name}.ogg")

    # Afficher le compteur dans la console
    print(f"Conversion du fichier {index}/{total_files}")

    # Conversion du fichier WEM en OGG
    subprocess.run([os.path.join(tools_dir, "ww2ogg"), wem_file, "--pcb", pcb_file])

    # Optimisation du fichier OGG avec revorb
    subprocess.run([os.path.join(tools_dir, "revorb"), ogg_file_intermediate, ogg_file_final])

    # Suppression du fichier intermédiaire
    if os.path.exists(ogg_file_intermediate):
        os.remove(ogg_file_intermediate)

print("Conversion terminée pour tous les fichiers WEM.")
