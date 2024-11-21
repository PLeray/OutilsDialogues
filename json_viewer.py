import json
import tkinter as tk
from tkinter import filedialog, scrolledtext

def open_and_display_json():
    # Ouvrir une boîte de dialogue pour sélectionner un fichier JSON
    file_path = filedialog.askopenfilename(
        title="Sélectionnez un fichier JSON",
        filetypes=(("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*"))
    )
    if not file_path:
        return  # Si l'utilisateur annule, ne rien faire

    try:
        # Charger le fichier JSON
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Effacer le contenu précédent
        text_widget.delete(1.0, tk.END)

        # Afficher les données dans le widget de texte
        for key, value in data.items():
            text_widget.insert(tk.END, f"ID : {key}\n")
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    text_widget.insert(tk.END, f"  {sub_key}: {sub_value}\n")
            else:
                text_widget.insert(tk.END, f"  {value}\n")
            text_widget.insert(tk.END, "\n")  # Ligne vide pour la lisibilité

    except Exception as e:
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, f"Erreur : {e}")

# Créer la fenêtre principale
root = tk.Tk()
root.title("Visualisateur de JSON")

# Ajouter un bouton pour ouvrir un fichier JSON
open_button = tk.Button(root, text="Ouvrir un fichier JSON", command=open_and_display_json)
open_button.pack(pady=10)

# Ajouter une zone de texte défilante pour afficher les données
text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=30)
text_widget.pack(padx=10, pady=10)

# Lancer la boucle principale Tkinter
root.mainloop()
