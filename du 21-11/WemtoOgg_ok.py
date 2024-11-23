# Script Python pour convertir tous les fichiers WEM en OGG
import os
import subprocess

# Définition des chemins de fichiers
input_dir = r"D:\_CyberPunk-Creation\TestConversion\Origin-wem"
output_dir = r"D:\_CyberPunk-Creation\TestConversion\Dest-ogg"
tools_dir = r"D:\_CyberPunk-Creation\TestConversion\Outils"
pcb_file = os.path.join(tools_dir, "packed_codebooks_aoTuV_603.bin")

# Vérifier si le dossier de sortie existe, sinon le créer
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Boucle sur chaque fichier .wem dans le dossier d'origine
for file_name in os.listdir(input_dir):
    if file_name.endswith(".wem"):
        wem_file = os.path.join(input_dir, file_name)
        base_name = os.path.splitext(file_name)[0]
        ogg_file_intermediate = os.path.join(input_dir, f"{base_name}.ogg")
        ogg_file_final = os.path.join(output_dir, f"{base_name}.ogg")

        # Conversion du fichier WEM en OGG
        subprocess.run([os.path.join(tools_dir, "ww2ogg"), wem_file, "--pcb", pcb_file])

        # Optimisation du fichier OGG avec revorb
        subprocess.run([os.path.join(tools_dir, "revorb"), ogg_file_intermediate, ogg_file_final])

        # Suppression du fichier intermédiaire
        if os.path.exists(ogg_file_intermediate):
            os.remove(ogg_file_intermediate)

print("Conversion terminée pour tous les fichiers WEM.")