class Block:
    id_counter = 0  # Compteur global pour générer les identifiants

    """Représente un bloc dans une étape."""
    def __init__(self, etape_number, etape_position, identifiant, title="Bloc", comment="", playlist_lien="", parent_etape=None):
        self.etape_number = etape_number
        self.etape_position = etape_position
        self.identifiant = identifiant
        self.title = title
        self.comment = comment
        self.playlist_lien = playlist_lien
        self.blocs_precedents = []
        self.blocs_suivants = []
        self.x = 0
        self.y = 0
        self.parent_etape = parent_etape  # Référence à l'étape parente

    @classmethod
    def initialize_counter(cls, existing_ids):
        """
        Initialiser le compteur basé sur les identifiants existants.
        Args:            existing_ids (list): Liste des identifiants existants sous forme de chaînes.
        """
        if existing_ids:
            max_id = max(int(identifiant) for identifiant in existing_ids if identifiant.isdigit())
            cls.id_counter = max_id + 1
        else:
            cls.id_counter = 1  # Commence à 1 si aucune donnée
    
    @classmethod
    def create(cls, etape_number, etape_position, parent_etape=None):
        """Créer un nouveau bloc avec un identifiant unique basé sur le compteur."""
        identifiant = f"{cls.id_counter:08}"  # Formaté sur 8 chiffres
        cls.id_counter += 1
        return cls(etape_number, etape_position, identifiant, parent_etape=parent_etape)


    def draw(self, canvas, x, y, is_source=False, is_target=False, selected=False, tags=None):
        """
        Dessiner le bloc sur le canvas avec les couleurs appropriées et des tags.
        
        :param canvas: Canvas Tkinter sur lequel dessiner.
        :param x: Position X du centre du bloc.
        :param y: Position Y du centre du bloc.
        :param is_source: Si le bloc est sélectionné comme source (Ctrl).
        :param is_target: Si le bloc est sélectionné comme cible (Maj).
        :param selected: Si le bloc est sélectionné par clic gauche.
        :param tags: Tags à appliquer aux éléments dessinés pour identification.
        """
        color = "#90EE90"  # Couleur par défaut pour les blocs
        outline_color = ""

        # Déterminer la couleur de l'entourage
        if is_source:
            outline_color = "green"
        elif is_target:
            outline_color = "red"
        elif selected:
            outline_color = "orange"

        # Dessiner le rectangle du bloc
        canvas.create_rectangle(
            x - 50, y - 20, x + 50, y + 20,
            fill=color,
            outline=outline_color,
            width=3 if outline_color else 1,
            tags=tags
        )

        # Ajouter les textes (titre, commentaire, lien)
        text_y_offset = -10  # Décalage initial pour le premier texte
        canvas.create_text(
            x, y + text_y_offset, text=self.identifiant + " (" + self.title + ")", font=("Arial", 8), tags=tags
        )
        text_y_offset += 17  # Décalage pour le commentaire
        canvas.create_text(
            x, y + text_y_offset, text=self.comment, font=("Arial", 9), fill="gray", tags=tags
        )
        """        
        text_y_offset += 15  # Décalage pour le lien de playlist
        canvas.create_text(
            x, y + text_y_offset, text=self.playlist_lien, font=("Arial", 8), fill="blue", tags=tags
        )
        """

    def clear_connections(self):
        """Supprimer toutes les connexions (précédents et suivants)."""
        self.blocs_precedents.clear()
        self.blocs_suivants.clear()

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
        # Initialement vide, les listes seront remplies après reconstruction
        block.blocs_precedents = data.get("blocs_precedents", [])
        block.blocs_suivants = data.get("blocs_suivants", [])
        return block
