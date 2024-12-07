import tkinter as tk
import time
from threading import Thread


def change_cursor(value):
    # Changer le curseur en icône d'attente >> Setcursor("wait")  Rétablir le curseur par défaut  >> Setcursor("")
    root.config(cursor=value)
    root.update_idletasks()  # Actualiser l'interface graphique

def Setcursor(value):
    # Lancer curseur
    Thread(target=change_cursor(value)).start()


def long_function():
    # Fonction qui effectue une tâche longue
    Setcursor("wait")
    time.sleep(3)  # Simuler une tâche longue
    Setcursor("")


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

