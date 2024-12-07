import tkinter as tk
import time
from threading import Thread

def long_function():
    # Fonction qui effectue une tâche longue
    root.config(cursor="wait")
    root.update_idletasks()  # Actualiser le curseur immédiatement
    time.sleep(5)  # Simuler une tâche longue
    root.config(cursor="")  # Rétablir le curseur par défaut
    root.update_idletasks()

def run_long_function():
    # Lancer la tâche longue dans un thread séparé
    Thread(target=long_function).start()

# Configuration de la fenêtre Tkinter
root = tk.Tk()
root.title("Changer le curseur")
root.geometry("300x150")

# Bouton pour lancer la fonction longue
button = tk.Button(root, text="Lancer une opération longue", command=run_long_function)
button.pack(pady=20)

# Démarrer l'interface Tkinter
root.mainloop()

