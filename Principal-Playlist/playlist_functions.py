# fichier: playlist_functions.py
import json, threading, pygame

from tkinter import ttk, filedialog, Menu
from LectureOgg import JouerAudio

import global_vars  # Accéder au Label global

def select_and_add_to_playlist(event, tree, playlist_tree, tk):
    # Identifier la ligne sous le curseur
    item = tree.identify_row(event.y)
    if item:  # Si une ligne est détectée
        tree.selection_set(item)  # Sélectionner cette ligne
        # Appeler la fonction pour ajouter à la playlist
        add_to_playlist(tree, playlist_tree, tk)

        # Mettre à jour le compteur
        count_playlist_rows(playlist_tree)
        colorize_playlist_rows(playlist_tree)

 # Fonction pour ajouter une/des ligne sélectionnée(s) au tableau playlist
def add_to_playlist(tree, playlist_tree, tk):
    # Ajouter toutes les lignes sélectionnées
    selected_items = tree.selection()  # Obtenir toutes les lignes sélectionnées
    for item in selected_items:
        selected_values = tree.item(item, 'values')  # Obtenir les valeurs de la ligne
        playlist_tree.insert("", tk.END, values=selected_values)  # Ajouter à la playlist

    # Mettre à jour le compteur
    count_playlist_rows(playlist_tree)
    colorize_playlist_rows(playlist_tree)        

#definition de la playlist
def setup_playlist(root, tree, tk, columns):
    main_frame = tk.Frame(root)
    main_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)  # Ajoutez expand=True ici

    button_frame = tk.Frame(main_frame)
    button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

    playlist_frame = tk.Frame(main_frame, height=450, bg='lightgray')
    playlist_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)  # Ajoutez expand=True ici


    playlist_columns = columns
    playlist_tree = ttk.Treeview(playlist_frame, columns=playlist_columns, show="headings", height=10)

    # Configurer les colonnes (largeur, alignement, etc.)

    for column in playlist_columns:
        playlist_tree.heading(column, text=column)

    playlist_scrollbar = ttk.Scrollbar(playlist_frame, orient=tk.VERTICAL, command=playlist_tree.yview)
    playlist_tree.configure(yscroll=playlist_scrollbar.set)
    playlist_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    playlist_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Ajouter le clic droit pour supprimer une ligne dans la playlist
    playlist_tree.bind("<Button-3>", lambda event: show_context_menu_Playlist(event, playlist_tree, root))
    # lecture ligne
    playlist_tree.bind("<<TreeviewSelect>>", lambda event: SelectionLignePlayliste(event, playlist_tree))  # Sélectionner une ligne pour afficher les détails


    add_button = tk.Button(button_frame, text="Ajouter selection à la playlist", command=lambda: add_to_playlist(tree, playlist_tree, tk))
    add_button.pack(side=tk.LEFT, padx=5)

    move_up_button = tk.Button(button_frame, text="Monter", command=lambda: move_up_playlist(playlist_tree))
    move_up_button.pack(side=tk.LEFT, padx=5)

    move_down_button = tk.Button(button_frame, text="Descendre", command=lambda: move_down_playlist(playlist_tree))
    move_down_button.pack(side=tk.LEFT, padx=5)

    play_button = tk.Button(button_frame, text="Ecouter la playlist", command=lambda: ecouterPlaylist(playlist_tree))
    play_button.pack(side=tk.LEFT, padx=(20, 5))
    
    stop_button = tk.Button(button_frame, text="Stop", command=lambda: stopperPlaylist())
    stop_button.pack(side=tk.LEFT, padx=(5, 20))

    load_button = tk.Button(button_frame, text="Charger la playlist", command=lambda: load_playlist_from_file(playlist_tree, tk))
    load_button.pack(side=tk.LEFT, padx=5)

    save_button = tk.Button(button_frame, text="Sauvegarder la playlist", command=lambda: save_playlist_to_file(playlist_tree))
    save_button.pack(side=tk.LEFT, padx=5)

    clear_button = tk.Button(button_frame, text="Effacer la playlist", command=lambda: clear_playlist(playlist_tree))
    clear_button.pack(side=tk.LEFT, padx=5)

    # Ajouter le Label pour afficher le nombre de lignes, à droite de clear_button
    global_vars.playlist_count_label = tk.Label(button_frame, text="Lignes dans la playlist : 0")
    global_vars.playlist_count_label.pack(side=tk.LEFT, padx=(10, 0))  # Alignez sur le côté gauche avec un petit espace

    return playlist_tree

#Fonction pour la selection d'une ligne de la playlist
def SelectionLignePlayliste(event, playlist_tree):
    selected_item = playlist_tree.selection()[0]
    selected_values = playlist_tree.item(selected_item, 'values')

    selected_gender = global_vars.vSexe.get()
    if selected_gender == "homme":
        audio_value = selected_values[4]
    else:
        audio_value = selected_values[3]

    JouerAudio(audio_value)

def show_context_menu_Playlist(event, playlist_tree, root):
    # Sélectionner la ligne sous le curseur
    item = playlist_tree.identify_row(event.y)  # Identifie la ligne sous le clic
    if item:  # Si une ligne est détectée
        playlist_tree.selection_set(item)  # Sélectionne cette ligne

        # Créer et afficher le menu contextuel
        menu = Menu(root, tearoff=0)
        menu.add_command(label="Supprimer de la playlist", command=lambda: remove_selected_from_playlist(playlist_tree))
        menu.post(event.x_root, event.y_root)  # Affiche le menu à l'emplacement du clic
    else:
        # Si aucune ligne n'est détectée, ne rien faire ou désélectionner
        playlist_tree.selection_remove(playlist_tree.selection())

# Fonction pour supprimer une ligne de la playlist via un clic droit
def remove_selected_from_playlist(playlist_tree):
    try:
        selected_item = playlist_tree.selection()[0]
        playlist_tree.delete(selected_item)
    except IndexError:
        pass
    
# Fonction pour déplacer une ligne vers le haut dans le tableau de playlist
def move_up_playlist(playlist_tree):
    try:
        selected_item = playlist_tree.selection()[0]
        index = playlist_tree.index(selected_item)
        if index > 0:
            playlist_tree.move(selected_item, playlist_tree.parent(selected_item), index - 1)
    except IndexError:
        pass

# Fonction pour déplacer une ligne vers le bas dans le tableau de playlist
def move_down_playlist(playlist_tree):
    try:
        selected_item = playlist_tree.selection()[0]
        index = playlist_tree.index(selected_item)
        if index < len(playlist_tree.get_children()) - 1:
            playlist_tree.move(selected_item, playlist_tree.parent(selected_item), index + 1)
    except IndexError:
        pass

# Fonction pour effacer le tableau de playlist
def clear_playlist(playlist_tree):
    for item in playlist_tree.get_children():
        playlist_tree.delete(item)

# Fonction pour sauvegarder la playlist dans un fichier JSON
def save_playlist_to_file(playlist_tree):
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        playlist_data = []
        # Récupérer les données de chaque ligne de la playlist
        for child in playlist_tree.get_children():
            values = playlist_tree.item(child, "values")
            playlist_data.append(values)
        # Sauvegarder les données dans un fichier JSON
        with open(file_path, "w") as file:
            json.dump(playlist_data, file, indent=4)

# Fonction pour charger la playlist à partir d'un fichier JSON
def load_playlist_from_file(playlist_tree,tk):
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, "r") as file:
            playlist_data = json.load(file)
            # Effacer l'ancienne playlist avant de charger la nouvelle
            clear_playlist(playlist_tree)
            # Ajouter les nouvelles données dans la playlist
            for values in playlist_data:
                playlist_tree.insert("", tk.END, values=values)

            # Mettre à jour le compteur
            count_playlist_rows(playlist_tree)
            colorize_playlist_rows(playlist_tree)

# Fonction pour lire la Playlist
def ecouterPlaylist(playlist_tree):
    #    Lance la lecture de la playlist dans un thread séparé.
    global is_playlist_playing  # Utiliser la variable globale
    is_playlist_playing = True  # Activer l'état de lecture

    def lecture_playlist():
        global is_playlist_playing
        selected_items = playlist_tree.selection()
        items = playlist_tree.get_children()

        if not items:
            print("La playlist est vide.")
            is_playlist_playing = False
            return

        start_index = 0
        if selected_items:
            start_index = items.index(selected_items[0])

        for item in items[start_index:]:
            if not is_playlist_playing:  # Vérification pour stopper la lecture
                #print("Lecture de la playlist interrompue.")
                break

            # Mettre à jour la sélection de l'élément en cours de lecture
            playlist_tree.selection_set(item)  # Sélectionner l'élément
            playlist_tree.see(item)  # Faire défiler pour afficher l'élément
            playlist_tree.update_idletasks()  # Rafraîchir l'affichage du Treeview
            
            selected_values = playlist_tree.item(item, "values")

            selected_gender = global_vars.vSexe.get()
            if selected_gender == "homme":
                audio_value = selected_values[4]
            else:
                audio_value = selected_values[3]

            if audio_value:
                #print(f"Lecture de : {audio_value}")
                try:
                    JouerAudio(audio_value)
                except Exception as e:
                    print(f"Erreur lors de la lecture de {audio_value} : {e}")
            else:
                print(f"Aucun fichier audio pour la ligne {item}.")

            while is_playlist_playing and pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        is_playlist_playing = False  # Réinitialiser l'état de lecture après la fin

    # Démarrage du thread
    thread = threading.Thread(target=lecture_playlist, daemon=True)
    thread.start()



# Fonction pour stopper Playlist
def stopperPlaylist():
    """
    Stoppe complètement la lecture de la playlist.
    """
    global is_playlist_playing
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()  # Arrête l'audio en cours
        is_playlist_playing = False  # Stoppe la progression dans la playlist
        #print("Lecture de la playlist complètement arrêtée.")
    except Exception as e:
        print(f"Erreur lors de l'arrêt de la lecture : {e}")

def count_playlist_rows(playlist_tree):
    """
    Compte et affiche le nombre de lignes dans le Treeview de la playlist.
    """
    row_count = len(playlist_tree.get_children())
    if global_vars.playlist_count_label:  # Mettre à jour le Label global
        global_vars.playlist_count_label.config(text=f"Lignes dans la playlist : {row_count}")
    else:
        print(f"Lignes dans la playlist : {row_count}")


def colorize_playlist_rows(playlist_tree):
    """
    Colore les lignes de playlist_tree en fonction de la valeur extraite de la 4ème colonne.
    Les lignes ayant une valeur commune dans la 4ème colonne auront la même couleur.

    :param playlist_tree: Le Treeview contenant les données.
    """
    # Dictionnaire pour stocker les couleurs attribuées
    color_mapping = {}
    # Liste de couleurs disponibles
    colors = ["#FFCCCC", "#CCFFCC", "#CCCCFF", "#FFFFCC", "#FFCCFF", "#CCFFFF"]

    # Fonction pour extraire la valeur significative de la 4ème colonne
    def extract_value(column_value):
        personnage = ""
        if not column_value or "/" not in column_value or "_" not in column_value:
            personnage = "unknown"
        try:
            last_part = column_value.rsplit("/", 1)[-1]  # Récupérer la partie après le dernier '/'
            personnage = last_part.split("_", 1)[0]  # Récupérer la partie avant le premier '_'
        except IndexError:
            personnage = "unknown"
        #print(f"Lignes dans la playlist : {personnage}")
        return personnage

    # Parcourir toutes les lignes de playlist_tree
    rows = playlist_tree.get_children()
    for row in rows:
        values = playlist_tree.item(row, "values")  # Récupérer les valeurs de la ligne
        if len(values) >= 4:
            key = extract_value(values[3])  # Extraire la clé depuis la 4ème colonne
        else:
            key = "unknown"

        # Assigner une couleur à cette clé si elle n'a pas encore de couleur
        if key not in color_mapping:
            color_mapping[key] = colors[len(color_mapping) % len(colors)]  # Cycle dans la liste des couleurs

        # Appliquer la couleur au fond de la ligne
        playlist_tree.tag_configure(key, background=color_mapping[key])
        playlist_tree.item(row, tags=(key,))


