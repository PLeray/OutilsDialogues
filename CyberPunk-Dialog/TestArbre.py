
import tkinter as tk
from CstepBlockApp import StepBlockApp

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x800")  # Largeur: 1200px, Hauteur: 800px
    app = StepBlockApp(root)
    root.mainloop()    