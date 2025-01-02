import tkinter as tk

class Application:
    def __init__(self, root):
        left_frame = tk.Frame(root)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Ajouter une liste pour afficher les lignes avec une police plus grande
        self.line_listbox = tk.Listbox(left_frame, width=130, height=20, font=("Helvetica", 14))
        self.line_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Ajouter une barre de défilement
        scrollbar = tk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.line_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.line_listbox.config(yscrollcommand=scrollbar.set)

        # Charger les lignes du fichier CSV dans la liste
        self._load_lines_from_csv()

    def _load_lines_from_csv(self):
        # Exemple de données pour tester l'affichage
        for i in range(50):
            self.line_listbox.insert(tk.END, f"Ligne {i+1}")

# Initialisation de l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
