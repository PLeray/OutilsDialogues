# fichier: launcher.py
import tkinter as tk
from tkinter import filedialog
import subprocess
from playlist import load_playlist_from_file
import global_vars
from tkinter import ttk

def launch_main_program():
    # Lancer le programme principal main.py
    subprocess.Popen(["python", "main.py"])

def load_playlist():
    # Créer une fenêtre temporaire pour la playlist
    temp_root = tk.Tk()
    temp_root.withdraw()  # Cacher la fenêtre principale temporaire
    
    # Charger la playlist en appelant la fonction existante
    playlist_tree = ttk.Treeview()  # Treeview temporaire
    load_playlist_from_file(playlist_tree, tk)

    # Afficher les données chargées (facultatif)
    for child in playlist_tree.get_children():
        print(playlist_tree.item(child, "values"))
    
    temp_root.destroy()

# Interface du programme de lancement
root = tk.Tk()
root.title("Launcher Program")
root.geometry("400x200")

# Ajouter les boutons
launch_button = tk.Button(root, text="Lancer main.py", command=launch_main_program)
launch_button.pack(pady=20)

load_playlist_button = tk.Button(root, text="Charger une playlist", command=load_playlist)
load_playlist_button.pack(pady=20)

root.mainloop()
