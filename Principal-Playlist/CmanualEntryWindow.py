import tkinter as tk

class ManualEntryWindow:
    def __init__(self, parent, playlist_tree, column_names=None):
        """
        Initialise une fenêtre pour saisir manuellement des données.

        :param parent: Fenêtre parente (Tkinter).
        :param playlist_tree: Treeview de la playlist à mettre à jour.
        :param column_names: Liste des colonnes à afficher pour la saisie.
        """
        self.parent = parent
        self.playlist_tree = playlist_tree
        self.column_names = column_names or [
            "ACTION Female * :", "ACTION Male :"
        ]
        self.entry_fields = {}  # Dictionnaire pour stocker les champs d'entrée

        self._create_window()

    def _create_window(self):
        """Crée la fenêtre de saisie manuelle."""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Add Playlist Row")

        # Ajouter des champs d'entrée pour chaque colonne
        for idx, column in enumerate(self.column_names):
            label = tk.Label(self.window, text=column)
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

            entry = tk.Entry(self.window, width=40)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            self.entry_fields[column] = entry

        # Ajouter le bouton de validation
        submit_button = tk.Button(self.window, text="Add Row", command=self._add_row)
        submit_button.grid(row=len(self.column_names), column=0, columnspan=2, pady=10)

    def _add_row(self):
        """Ajoute une nouvelle ligne dans le Treeview avec les valeurs saisies."""
        # Construire les valeurs pour la nouvelle ligne
        values = [
            "ID A GENERER",  # Identifiant généré
            self.entry_fields["ACTION Female * :"].get(),
            self.entry_fields["ACTION Male :"].get(),
            "",
            "",
            "QUEST PATH"  # Valeur par défaut pour le chemin de quête
        ]

        # Insérer les valeurs dans le Treeview
        self.playlist_tree.insert("", tk.END, values=values)

        # Mettre à jour le Treeview
        #self._update_playlist_view()

        # Fermer la fenêtre
        self.window.destroy()

    """
    def _update_playlist_view(self):
        #Met à jour les propriétés de la playlist après modification.
        # Mettre à jour le compteur de lignes
        count_playlist_rows(self.playlist_tree)

        # Mettre à jour les couleurs des lignes
        colorize_playlist_rows(self.playlist_tree)
    """

