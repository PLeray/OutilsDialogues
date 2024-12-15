import tkinter as tk
from tkinter import Menu, filedialog
import json

from Csequence import Sequence
from Cetape import Etape
from Cblock import Block  # Import de la classe Block



class StepBlockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Step and Block Manager")

        # Variables
        self.sequence = Sequence("Nouvelle Séquence")
        self.selected_etape = None
        self.selected_blocks = {"green": [], "red": []}

        # Frame principale
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Barre de boutons
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, side=tk.TOP)

        self.create_buttons()  # Créez les boutons dans la barre

        # Canvas pour afficher les séquences
        self.canvas_frame = tk.Frame(self.main_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Menu contextuel
        self.create_menu()

        # Événements
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<KeyPress>", self.on_key_press)
        self.canvas.bind("<Shift-Button-1>", self.on_shift_click)
        self.canvas.bind("<Control-Button-1>", self.on_ctrl_click)
        self.canvas.focus_set()

        # Ajouter une première étape
        self.add_etape()

        # Redimensionnement
        self.root.bind("<Configure>", self.on_resize)


    def create_buttons(self):
        """Créer les boutons Load, Save, Ajouter Étape, Ajouter Bloc et Connect."""
        tk.Button(self.button_frame, text="Save", command=self.save_to_file).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.button_frame, text="Load", command=self.load_from_file).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.button_frame, text="Ajouter Étape", command=self.add_etape).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.button_frame, text="Ajouter Bloc", command=self.add_block).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.button_frame, text="Connect", command=self.create_connections).pack(side=tk.LEFT, padx=5, pady=5)


    def create_menu(self):
        """Créer le menu contextuel."""
        self.menu = tk.Menu(self.root, tearoff=0)
        # Ajouter des commandes au menu
        self.menu.add_command(label="Supprimer les liaisons", command=self.delete_connections)
        self.menu.add_command(label="Supprimer le Bloc", command=self.delete_block)
        self.menu.add_command(label="Supprimer l'Étape", command=self.delete_etape)


    def on_key_press(self, event):
        """Gérer les pressions de touches pour déplacer les blocs dans une étape."""
        if self.selected_blocks["green"]:
            block_to_move = self.selected_blocks["green"][0]
            etape_idx = block_to_move.etape_number
            etape = self.sequence.etapes[etape_idx]

            # Déterminer la direction du déplacement
            direction = None
            if event.keysym == "Left":
                direction = "left"
            elif event.keysym == "Right":
                direction = "right"

            if direction and etape.move_block_laterally(block_to_move, direction):
                # Réorganiser les positions des blocs après le déplacement
                etape.reorganize_blocks()

                # Mettre à jour les connexions
                self.sequence.update_connections()

                # Redessiner la séquence
                self.draw_sequence()
        else:
            print("Aucun bloc sélectionné pour déplacement.")


    def add_etape(self):
        """Ajouter une nouvelle étape après l'étape sélectionnée."""
        if self.selected_etape is not None:
            # Ajouter après l'étape sélectionnée
            new_index = self.sequence.etapes.index(self.selected_etape) #+ 1
        else:
            # Ajouter à la fin si aucune étape n'est sélectionnée
            new_index = len(self.sequence.etapes)
        # Créer une nouvelle étape
        y = new_index * 100 + 50
        
        print(Etape)
        new_etape = Etape(numero=new_index, y=y, width=self.canvas.winfo_width())

        self.sequence.etapes.insert(new_index, new_etape)
        # Réajuster les positions et numéros des étapes suivantes
        for idx, etape in enumerate(self.sequence.etapes):
            etape.numero = idx
            etape.y = idx * 100 + 50
        # Redessiner la séquence
        self.draw_sequence()

    def delete_etape(self):
        """Supprimer l'étape sélectionnée."""
        if self.selected_etape:
            self.sequence.remove_etape(self.selected_etape)  # Appel à Sequence.remove_etape
            self.selected_etape = None
            self.draw_sequence()
            print("Étape supprimée.")

    def add_block(self):
        """Ajouter un bloc dans l'étape sélectionnée."""
        if not self.selected_etape:
            print("Aucune étape sélectionnée pour ajouter un bloc.")
            return

        self.selected_etape.add_block()
        self.draw_sequence()
        print(f"Bloc ajouté à l'étape {self.selected_etape.numero}.")



    def delete_block(self):
        """Supprimer le bloc sélectionné."""
        if self.selected_block:
            etape = self.selected_block.parent_etape  # Utiliser parent_etape
            etape.remove_block(self.selected_block)  # Supprimer le bloc de l'étape
            self.selected_block = None
            self.draw_sequence()
            print("Bloc supprimé.")


    def draw_sequence(self):
        """Dessiner toute la séquence sur le canvas."""
        self.canvas.delete("all")

        # Dessiner chaque étape et ses blocs
        for etape in self.sequence.etapes:
            etape.draw(
                self.canvas,
                selected_blocks=self.selected_blocks,
                selected_etape=(etape == self.selected_etape)
            )
        # Dessiner les connexions entre les blocs
        print("Dessiner les connexions :")
        for conn in self.sequence.connections:
            start = conn["start"]
            end = conn["end"]
            if start and end:
                print(f"Dessiner connexion : {start.identifiant} -> {end.identifiant}")
                self.canvas.create_line(
                    start.x, start.y + 20,  # Position de départ
                    end.x, end.y - 20,      # Position de fin
                    fill="blue", width=4
                )
            else:
                print(f"Connexion invalide : {conn}")


    def create_connections(self):
        """Créer des connexions entre les blocs sélectionnés."""
        if not self.selected_blocks["green"] or not self.selected_blocks["red"]:
            print("Sélectionnez des blocs sources et cibles pour créer une connexion.")
            return
        for source in self.selected_blocks["green"]:
            for target in self.selected_blocks["red"]:
                self.sequence.add_connection(source, target)
        # Réinitialiser les sélections
        self.selected_blocks = {"green": [], "red": []}
        # Redessiner après validation
        self.draw_sequence()

    def delete_connections(self):
        """Supprimer toutes les connexions du bloc sélectionné."""
        if self.selected_block:
            self.selected_block.clear_connections()  # Appel à Bloc.clear_connections
            self.draw_sequence()
            print("Connexions supprimées.")


    def on_left_click(self, event):
        """Gérer les clics gauche pour sélectionner un bloc ou une étape."""
        clicked = self.canvas.find_closest(event.x, event.y)
        tags = self.canvas.gettags(clicked)

        if "block" in tags:
            # Get the block by indices from tags
            etape_idx, block_idx = int(tags[1]), int(tags[2])
            block = self.sequence.etapes[etape_idx].blocs[block_idx]

            # Select the block (orange outline)
            self.selected_blocks = {"green": [], "red": []}  # Reset source/target selections
            self.selected_block = block  # Track selected block
            self.selected_etape = None  # Clear étape selection
            print(f"Bloc sélectionné : {block.title} Rang {block.etape_position} (Étape {etape_idx}).")

        elif "etape" in tags:
            # Select the étape
            etape_idx = int(tags[1])
            self.selected_etape = self.sequence.etapes[etape_idx]
            self.selected_block = None  # Clear block selection
            self.selected_blocks = {"green": [], "red": []}  # Reset source/target selections
            print(f"Étape sélectionnée : {etape_idx}.")

        else:
            # No valid selection
            print("Aucun élément valide sélectionné.")
            self.selected_block = None
            self.selected_etape = None

        # Redraw to reflect the selection changes
        self.draw_sequence()




    def on_shift_click(self, event):
        """Gérer les clics avec Maj pour sélectionner les blocs cibles."""
        clicked = self.canvas.find_closest(event.x, event.y)
        tags = self.canvas.gettags(clicked)

        if "block" in tags:
            etape_idx, block_idx = int(tags[1]), int(tags[2])
            block = self.sequence.etapes[etape_idx].blocs[block_idx]

            # Ajouter le bloc à la liste rouge (cibles) s'il n'y est pas déjà
            if block not in self.selected_blocks["red"]:
                self.selected_blocks["red"].append(block)
                print(f"Bloc cible ajouté : {block.title} (Étape {etape_idx}).")
            else:
                print(f"Bloc déjà dans les cibles : {block.title}")
        else:
            print("Aucun bloc valide pour la sélection de cibles.")

        # Redessiner après la sélection
        self.draw_sequence()



    def on_ctrl_click(self, event):
        """Gérer les clics avec Ctrl pour sélectionner les blocs sources."""
        clicked = self.canvas.find_closest(event.x, event.y)
        tags = self.canvas.gettags(clicked)

        if "block" in tags:
            etape_idx, block_idx = int(tags[1]), int(tags[2])
            block = self.sequence.etapes[etape_idx].blocs[block_idx]

            # Ajouter le bloc à la liste verte (sources) s'il n'y est pas déjà
            if block not in self.selected_blocks["green"]:
                self.selected_blocks["green"].append(block)
                print(f"Bloc source ajouté : {block.title} (Étape {etape_idx}).")
            else:
                print(f"Bloc déjà dans les sources : {block.title}")
        else:
            print("Aucun bloc valide pour la sélection des sources.")

        # Redessiner après la sélection
        self.draw_sequence()



    def on_right_click(self, event):
        """Gérer le clic droit pour afficher le menu contextuel."""
        clicked = self.canvas.find_closest(event.x, event.y)
        tags = self.canvas.gettags(clicked)

        if "block" in tags:
            etape_idx, block_idx = int(tags[1]), int(tags[2])
            self.selected_block = self.sequence.etapes[etape_idx].blocs[block_idx]

            # Configurer le menu contextuel pour les blocs
            self.menu = Menu(self.root, tearoff=0)
            self.menu.add_command(label="Supprimer le Bloc", command=self.delete_block)
            self.menu.add_command(label="Supprimer les Connexions", command=self.delete_connections)
            self.menu.post(event.x_root, event.y_root)
            print(f"Menu pour le bloc {self.selected_block.title} ouvert.")

        elif "etape" in tags:
            etape_idx = int(tags[1])
            self.selected_etape = self.sequence.etapes[etape_idx]

            # Configurer le menu contextuel pour les étapes
            self.menu = Menu(self.root, tearoff=0)
            self.menu.add_command(label="Supprimer l'Étape", command=self.delete_etape)
            self.menu.post(event.x_root, event.y_root)
            print(f"Menu pour l'étape {self.selected_etape.numero} ouvert.")



    def on_resize(self, event):
        """Mettre à jour les tailles et recentrer les blocs après redimensionnement."""
        new_width = event.width
        for etape in self.sequence.etapes:
            etape.width = new_width
            etape.reorganize_blocks()
        self.draw_sequence()




    def save_to_file(self):
        """Sauvegarder les étapes et blocs dans un fichier JSON.
        filename = filedialog.asksaveasfilename(filetypes=[("JSON Files", "*.json")])
        if not filename:
            return
        """
        filename = "data/projet/projet.json"

        # Construire la structure de données pour la sauvegarde
        data = {
            "name": self.sequence.name,
            "etapes": [
                {
                    "numero": etape.numero,
                    "y": etape.y,
                    "width": etape.width,
                    "blocs": [block.to_dict() for block in etape.blocs]
                }
                for etape in self.sequence.etapes
            ]
        }

        # Écrire dans le fichier JSON
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Sauvegardé dans {filename}")

    def validate_json(data):
        """Valider que le JSON ne contient pas de doublons dans les connexions."""
        for etape in data.get("etapes", []):
            for block in etape.get("blocs", []):
                block["blocs_precedents"] = list(set(block["blocs_precedents"]))
                block["blocs_suivants"] = list(set(block["blocs_suivants"]))
        return data
        
    def load_from_file(self):
        """Charger les étapes, blocs et connexions depuis un fichier JSON.
        filename = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not filename:
            return
        """
        filename = "data/projet/projet.json"

        with open(filename, "r") as f:
            data = json.load(f)

        # Charger la séquence depuis les données du fichier
        self.sequence = Sequence.from_dict(data)

        # Collecter tous les identifiants des blocs
        existing_ids = [
            block["identifiant"]
            for etape in data["etapes"]
            for block in etape["blocs"]
        ]

        # Initialiser le compteur global pour les blocs
        Block.initialize_counter(existing_ids)

        # Reconstruire les connexions entre les blocs
        for etape in self.sequence.etapes:
            for block in etape.blocs:
                print(f"Reconstruire les connexions pour le bloc {block.identifiant}:")
                blocs_precedents = []
                blocs_suivants = []
                block.parent_etape = etape  # Associer le bloc à son étape

                # Ajouter uniquement des blocs uniques
                for prev_id in block.blocs_precedents:
                    bloc = self.sequence.find_block({"identifiant": prev_id})
                    if bloc and bloc not in blocs_precedents:
                        blocs_precedents.append(bloc)

                for next_id in block.blocs_suivants:
                    bloc = self.sequence.find_block({"identifiant": next_id})
                    if bloc and bloc not in blocs_suivants:
                        blocs_suivants.append(bloc)

                block.blocs_precedents = blocs_precedents
                block.blocs_suivants = blocs_suivants

                print(f"  Précédents: {[b.identifiant for b in block.blocs_precedents]}")
                print(f"  Suivants: {[b.identifiant for b in block.blocs_suivants]}")

        # Redessiner la séquence
        self.draw_sequence()
        print(f"Chargé depuis {filename}")

    def to_dict(self):
        """Convertir le bloc en dictionnaire pour sauvegarde."""
        return {
            "etape_number": self.etape_number,
            "etape_position": self.etape_position,
            "identifiant": self.identifiant,
            "title": self.title,
            "comment": self.comment,
            "playlist_lien": self.playlist_lien,
            "blocs_precedents": [bloc.identifiant for bloc in self.blocs_precedents],
            "blocs_suivants": [bloc.identifiant for bloc in self.blocs_suivants],
        }

    @staticmethod
    def from_dict(data):
        """Créer un bloc depuis un dictionnaire."""
        block = Block(
            etape_number=data["etape_number"],
            etape_position=data["etape_position"],
            identifiant=data["identifiant"],
            title=data.get("title", ""),
            comment=data.get("comment", ""),
            playlist_lien=data.get("playlist_lien", ""),
        )
        # Initialement vide, à lier après reconstruction
        block.blocs_precedents = []
        block.blocs_suivants = []
        return block



