import json

file_path = r"D:\_CyberPunk-Creation\BDDDialogues\test.json"
with open(file_path, "r", encoding="utf-8") as file:
    try:
        data = json.load(file)
        print("Fichier JSON valide.")
        print(data)
    except json.JSONDecodeError as e:
        print(f"Erreur dans le fichier JSON : {e}")