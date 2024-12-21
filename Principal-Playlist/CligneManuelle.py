import os
import csv
import tkinter as tk
import time
import global_variables  # Importer les variables globales

class LigneManuelle:
    def __init__(self, parent, playlist_tree, column_names=None, file_path=None):
        self.parent = parent
        self.playlist_tree = playlist_tree
        self.file_path = file_path or "data/projet/projet_files/localization/fr-fr/projetDIC.csv"
        self.column_names = column_names or ["ACTION Female * :", "ACTION Male :"]
        self.entry_fields = {}
        self.data = []
        self._current_selected_index = None  # Suivre l'index de la ligne sélectionnée

        self._create_window()

    def _create_window(self):
        """Crée la fenêtre de saisie manuelle."""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Add/Edit Playlist Row")
        self.window.geometry("1500x400")

        # Cadre pour la liste et les champs
        left_frame = tk.Frame(self.window, width=500)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        right_frame = tk.Frame(self.window)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Ajouter une liste pour afficher les lignes
        self.line_listbox = tk.Listbox(left_frame, width=130, height=20)
        
        self.line_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.line_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.line_listbox.config(yscrollcommand=scrollbar.set)

        # Charger les lignes du fichier CSV dans la liste
        self._load_lines_from_csv()

        # Événement de sélection d'une ligne dans la liste
        self.line_listbox.bind("<<ListboxSelect>>", self._populate_fields_from_selection)

        
        
        # Ajouter le champ stringId en lecture seule
        """
        string_id_label = tk.Label(right_frame, text=global_variables.data_ID)
        string_id_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.string_id_var = tk.StringVar(value="NOTHING")
        string_id_entry = tk.Entry(right_frame, textvariable=self.string_id_var, state="readonly", width=40)
        string_id_entry.grid(row=0, column=1, padx=10, pady=5)        
        """
        

        

        # Label pour stringId
        string_id_label = tk.Label(right_frame, text=global_variables.data_ID)
        string_id_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")  # Réduisez padx et utilisez sticky="w"

        # Champ pour stringId
        self.string_id_var = tk.StringVar(value="NOTHING")
        string_id_entry = tk.Entry(right_frame, textvariable=self.string_id_var, state="readonly", width=40)
        string_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")  # Alignez à gauche avec sticky="w"




        # Ajouter des champs d'entrée pour chaque colonne
        for idx, column in enumerate(self.column_names):
            label = tk.Label(right_frame, text=column)
            label.grid(row=idx + 1, column=0, padx=10, pady=5, sticky="w")

            entry = tk.Entry(right_frame, width=80)
            entry.grid(row=idx + 1, column=1, padx=10, pady=5)
            self.entry_fields[column] = entry

        # Ajouter un cadre pour les boutons
        button_frame = tk.Frame(right_frame)
        button_frame.grid(row=len(self.column_names) + 2, column=0, columnspan=2, pady=10)

        self.new_line_button = tk.Button(button_frame, text="New Line", command=self._reset_form, state="disabled")
        self.new_line_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(button_frame, text="Save Line", command=self._save_selected_row, state="disabled")
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(button_frame, text="Delete Line", command=self._delete_selected_row, state="disabled")
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # Bouton pour insérer une ligne dans le Treeview
        self.insert_playlist_button = tk.Button(self.window, text="Insert Line in playlist", command=self._add_Line_In_Playlist, state="disabled")
        self.insert_playlist_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

        # Événement pour activer le bouton "Save Line" si le champ global_variables.data_F_SubTitle est rempli
        self.entry_fields["ACTION Female * :"].bind("<KeyRelease>", self._check_save_button_state)

    def _generate_unique_id(self):
        """Génère un identifiant unique."""
        return str(int(time.time() * 1_000_000))

    def _add_Line_In_Playlist(self):
        """Ajoute la ligne sélectionnée dans la Listbox au Treeview."""
        try:
            # Récupérer l'index de la ligne sélectionnée dans la Listbox
            selected_index = self.line_listbox.curselection()[0]
            selected_row = self.data[selected_index]  # Récupérer les données associées

            # Construire les valeurs à insérer dans le Treeview
            values = [
                selected_row[global_variables.data_ID],
                selected_row[global_variables.data_F_SubTitle],
                selected_row[global_variables.data_M_SubTitle],                
                selected_row[global_variables.data_F_Voice],
                selected_row[global_variables.data_M_Voice],
                selected_row[global_variables.data_Quest]
            ]
            # Insérer les valeurs dans le Treeview
            self.playlist_tree.insert("", tk.END, values=values)
            print(f"Ligne ajoutée au Treeview : {values}")
        except IndexError:
            print("Aucune ligne sélectionnée dans la Listbox.")
        self.window.destroy()

    def _populate_fields_from_selection(self, event=None):
        """Remplit les champs avec les valeurs de la ligne sélectionnée."""
        try:
            self._current_selected_index = self.line_listbox.curselection()[0]  # Mémoriser l'index
            print(f"Ligne selectionnee (self._current_selected_index) : {self._current_selected_index}")            
            #selected_index = self.line_listbox.curselection()[0]
            #self._current_selected_index = selected_index  # Mémoriser l'index            

            selected_row = self.data[self._current_selected_index]

            # Conserver le StringId existant
            self.string_id_var.set(selected_row[global_variables.data_ID])
            self.entry_fields["ACTION Female * :"].delete(0, tk.END)
            self.entry_fields["ACTION Female * :"].insert(0, selected_row[global_variables.data_F_SubTitle])
            self.entry_fields["ACTION Male :"].delete(0, tk.END)
            self.entry_fields["ACTION Male :"].insert(0, selected_row[global_variables.data_M_SubTitle])

            # Activer les boutons appropriés
            self.new_line_button.config(state="normal")
            self.delete_button.config(state="normal")
            self.save_button.config(state="disabled")  # Désactivé jusqu'à modification
            self.insert_playlist_button.config(state="normal")  # Activer le bouton d'insertion
        except IndexError:
            print(f"Aucune ligne sélectionnée (self._current_selected_index) : {self._current_selected_index}") # Ou ne faites rien

    def _reset_form(self):
        """Réinitialise le formulaire pour une nouvelle ligne."""
        self.string_id_var.set("NOTHING")  # StringId remis à NOTHING explicitement
        self.entry_fields["ACTION Female * :"].delete(0, tk.END)
        self.entry_fields["ACTION Male :"].delete(0, tk.END)

        # Désactiver les boutons sauf "Save Line"
        self.new_line_button.config(state="disabled")
        self.delete_button.config(state="disabled")
        self.save_button.config(state="normal")  # Permet d'enregistrer une nouvelle ligne
        self.insert_playlist_button.config(state="disabled")  # Activer le bouton d'insertion
        self._current_selected_index = None  # Plus aucune ligne sélectionnée


    def _delete_selected_row(self):
        """Supprime la ligne sélectionnée du fichier CSV."""
        try:
            selected_index = self.line_listbox.curselection()[0]
            del self.data[selected_index]

            file_path = self.file_path
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=[
                    global_variables.data_ID, 
                    global_variables.data_F_SubTitle, 
                    global_variables.data_M_SubTitle, 
                    global_variables.data_F_Voice, 
                    global_variables.data_M_Voice, 
                    global_variables.data_Quest
                    ])
                writer.writeheader()
                writer.writerows(self.data)

            self._load_lines_from_csv()
        except IndexError:
            print("Aucune ligne sélectionnée pour la suppression.")

    def _save_to_csv(self, values):
        """Ajoute une ligne dans le fichier CSV."""
        file_path = self.file_path
        row_data = {
            global_variables.data_F_SubTitle: values[0],
            global_variables.data_M_SubTitle: values[1],
            global_variables.data_ID: values[2],
            "female_vo_path": values[3],
            "male_vo_path": values[4],
            "quest_path": values[5]
        }
        file_exists = os.path.exists(file_path)

        with open(file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=row_data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(row_data)

    def _load_lines_from_csv(self):
        """Charge les lignes depuis le fichier CSV."""
        file_path = self.file_path
        if os.path.exists(file_path):
            with open(file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.data = []
                self.line_listbox.delete(0, tk.END)
                for idx, row in enumerate(reader):
                    self.data.append(row)
                    self.line_listbox.insert(tk.END, f"{row[global_variables.data_ID]} - {row[global_variables.data_F_SubTitle][:50]} - {row[global_variables.data_M_SubTitle][:50]}")

        else:
            self.data = []

    def _check_save_button_state(self, event):
        """Active ou désactive le bouton 'Save Line' selon les modifications."""
        if self.entry_fields["ACTION Female * :"].get():
            self.save_button.config(state="normal")
        else:
            self.save_button.config(state="disabled")

    def _save_selected_row(self):
        """Sauvegarde les modifications de la ligne sélectionnée ou crée une nouvelle ligne."""
        file_path = self.file_path

        
        # Déterminer si une ligne est sélectionnée ou si c'est une nouvelle ligne
        """
        try:
            #selected_index = self.line_listbox.curselection()[0]
            #self._current_selected_index = selected_index  # Assurez-vous que l'index est mis à jour
            string_id = self.string_id_var.get()
            isNew = False
        except IndexError:
            string_id = self._generate_unique_id()
            isNew = True        
        """
           
        string_id = self.string_id_var.get()
        isNew = (string_id == "NOTHING")            
        print(f"Ligne string_id & isNew: {string_id} & {isNew}")
        if isNew:  # Creation d'un ID
            string_id = self._generate_unique_id()

        # Construire les données de la ligne
        the_row = {
            global_variables.data_F_SubTitle: self.entry_fields["ACTION Female * :"].get(),
            global_variables.data_M_SubTitle: self.entry_fields["ACTION Male :"].get(),
            global_variables.data_ID: string_id,
            "female_vo_path": "",
            "male_vo_path": "",
            "quest_path": "projet_files/localization/fr-fr/projetDIC.csv"
        }

        
        if isNew:     # Si isNew ajouter une nouvelle ligne
            self.data.append(the_row)
            self._current_selected_index = len(self.data) - 1  # Sélectionner la nouvelle ligne
        else:         # Si une ligne est sélectionnée, mettre à jour
            self.data[self._current_selected_index] = the_row

        # Sauvegarder dans le fichier CSV
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=[global_variables.data_F_SubTitle, global_variables.data_M_SubTitle, global_variables.data_ID, "female_vo_path", "male_vo_path", "quest_path"])
            writer.writeheader()
            writer.writerows(self.data)

        # Recharger les données et sélectionner la ligne sauvegardée
        self._load_lines_from_csv()
        self.line_listbox.selection_clear(0, tk.END)
        self.line_listbox.selection_set(self._current_selected_index)
        self._populate_fields_from_selection()  # Mettre à jour le formulaire

        print(f"Ligne sauvegardée : {the_row}")


