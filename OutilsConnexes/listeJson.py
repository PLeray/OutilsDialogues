import os
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import platform

# Fonction pour lister tous les fichiers JSON dans un dossier et ses sous-dossiers
def list_json_files(directory: str):
    json_files = []
    for root, _, files in os.walk(directory):  # Parcourt récursivement les sous-dossiers
        for file in files:
            if file.endswith(".json"):  # Vérifie si le fichier a l'extension .json
                absolute_path = os.path.join(root, file)  # Chemin absolu
                relative_path = os.path.relpath(absolute_path, directory)  # Chemin relatif
                json_files.append((relative_path, absolute_path))  # Ajoute chemin relatif et absolu
    return json_files

# Fonction appelée lors du clic sur "Scanner"
def scan_directory():
    global json_file_paths
    directory = filedialog.askdirectory(title="Sélectionnez un dossier à scanner")
    if not directory:  # Aucun dossier sélectionné
        messagebox.showwarning("Avertissement", "Aucun dossier sélectionné !")
        return

    # Récupérer la liste des fichiers JSON
    json_files = list_json_files(directory)
    json_file_paths = json_files  # Stocker les chemins absolus pour ouverture

    # Si aucun fichier JSON n'est trouvé
    if not json_files:
        messagebox.showinfo("Résultat", "Aucun fichier JSON trouvé dans ce dossier.")
        listbox.delete(0, tk.END)
        label_count.config(text="Nombre total de fichiers JSON : 0")
        label_folder.config(text=f"Dossier scanné : {directory}")
        return

    # Afficher le dossier scanné et la liste des fichiers
    listbox.delete(0, tk.END)  # Effacer la liste précédente
    label_folder.config(text=f"Dossier scanné : {directory}")  # Afficher le dossier scanné
    for file in json_files:
        listbox.insert(tk.END, file[0])  # Afficher le chemin relatif uniquement

    # Afficher le nombre total de fichiers JSON trouvés
    label_count.config(text=f"Nombre total de fichiers JSON : {len(json_files)}")

# Fonction pour ouvrir un fichier JSON au double-clic
def open_selected_file(event):
    try:
        # Récupérer l'index de la ligne sélectionnée
        selected_index = listbox.curselection()[0]
        # Récupérer le chemin absolu correspondant
        _, absolute_path = json_file_paths[selected_index]

        # Ouvrir le fichier dans l'éditeur par défaut
        if platform.system() == "Windows":
            os.startfile(absolute_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", absolute_path])
        else:  # Linux
            subprocess.run(["xdg-open", absolute_path])

    except IndexError:
        messagebox.showwarning("Avertissement", "Aucun fichier sélectionné !")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'ouvrir le fichier : {e}")

# Création de la fenêtre principale
window = tk.Tk()
window.title("Scanner de fichiers JSON")
window.geometry("700x500")

# Étiquette pour afficher le dossier scanné
label_folder = tk.Label(window, text="Dossier scanné : Aucun", font=("Arial", 12))
label_folder.pack(pady=10)

# Bouton pour lancer le scan
button_scan = tk.Button(window, text="Scanner un dossier", command=scan_directory, font=("Arial", 12))
button_scan.pack(pady=10)

# Liste pour afficher les fichiers JSON trouvés
listbox = tk.Listbox(window, width=80, height=20, font=("Courier", 10))
listbox.pack(pady=10)

# Ajout de l'événement double-clic à la Listbox
listbox.bind("<Double-Button-1>", open_selected_file)

# Étiquette pour afficher le nombre total de fichiers JSON
label_count = tk.Label(window, text="Nombre total de fichiers JSON : 0", font=("Arial", 12))
label_count.pack(pady=10)

# Lancement de la boucle principale
window.mainloop()
