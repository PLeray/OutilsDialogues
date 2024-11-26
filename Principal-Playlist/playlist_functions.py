# fichier: playlist_functions.py
import json, threading, pygame

from tkinter import ttk, filedialog, Menu
from LectureOgg import JouerAudio

def select_and_add_to_playlist(event, tree, playlist_tree, tk):
    # Identifier la ligne sous le curseur
    item = tree.identify_row(event.y)
    if item:  # Si une ligne est détectée
        tree.selection_set(item)  # Sélectionner cette ligne
        # Appeler la fonction pour ajouter à la playlist
        add_to_playlist(tree, playlist_tree, tk)


 # Fonction pour ajouter une/des ligne sélectionnée(s) au tableau playlist
def add_to_playlist(tree, playlist_tree, tk):
    # Ajouter toutes les lignes sélectionnées
    selected_items = tree.selection()  # Obtenir toutes les lignes sélectionnées
    for item in selected_items:
        selected_values = tree.item(item, 'values')  # Obtenir les valeurs de la ligne
        playlist_tree.insert("", tk.END, values=selected_values)  # Ajouter à la playlist

#definition de la playlist
def setup_playlist(root, tree, tk, columns, gender_var):
    main_frame = tk.Frame(root)
    main_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=10, pady=10)

    button_frame = tk.Frame(main_frame)
    button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

    playlist_frame = tk.Frame(main_frame, height=450, bg='lightgray')
    playlist_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

    playlist_columns = columns
    playlist_tree = ttk.Treeview(playlist_frame, columns=playlist_columns, show="headings", height=10)

    # Configurer les colonnes (largeur, alignement, etc.)

    for column in playlist_columns:
        playlist_tree.heading(column, text=column)

    for column in playlist_columns:
        if column == "ID":
            playlist_tree.column(column, width=130, minwidth=100, stretch=False, anchor="w")
        elif column == "Origine":
            playlist_tree.column(column, width=70, minwidth=200, stretch=False, anchor="w")
        elif column == "Origine 2":
            playlist_tree.column(column, width=70, minwidth=200, stretch=False, anchor="w")
        else:
            playlist_tree.column(column, width=200, anchor="w")


    playlist_scrollbar = ttk.Scrollbar(playlist_frame, orient=tk.VERTICAL, command=playlist_tree.yview)
    playlist_tree.configure(yscroll=playlist_scrollbar.set)
    playlist_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    playlist_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Ajouter le clic droit pour supprimer une ligne dans la playlist
    playlist_tree.bind("<Button-3>", lambda event: show_context_menu_Playlist(event, playlist_tree, root))
    # lecture ligne
    playlist_tree.bind("<<TreeviewSelect>>", lambda event: SelectionLignePlayliste(event, playlist_tree, gender_var))  # Sélectionner une ligne pour afficher les détails


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

    return playlist_tree

#Fonction pour la selection d'une ligne de la playlist
def SelectionLignePlayliste(event, playlist_tree, gender_var):
    selected_item = playlist_tree.selection()[0]
    selected_values = playlist_tree.item(selected_item, 'values')

    selected_gender = gender_var.get()
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

            item_values = playlist_tree.item(item, "values")
            audio_info = item_values[3]  # Supposons que la 3e colonne contient les infos audio

            if audio_info:
                #print(f"Lecture de : {audio_info}")
                try:
                    JouerAudio(audio_info)
                except Exception as e:
                    print(f"Erreur lors de la lecture de {audio_info} : {e}")
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



"""
# Fonction pour ajouter les filtres et les boutons de contrôle au-dessus du premier tableau
def add_filters2(frame, tree):
    filter_frame = tk.Frame(frame)
    filter_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

    columns = ["ID", "Sous-titres", "Origine", "Personnage", "Origine", "Quête"]
    filters = []
    for i, column in enumerate(columns):
        label = tk.Label(filter_frame, text=f"Filtre {column}")
        label.grid(row=0, column=i, padx=5)
        entry = tk.Entry(filter_frame)
        entry.grid(row=1, column=i, padx=5)
        filters.append(entry)

    def apply_filters():
        for item in tree.get_children():
            tree.delete(item)

        data: Dict[str, Dialogue] = load_json(file_path)
        for key, value in data.items():
            sous_titres = value.get('female', {}).get('text', 'N/A')
            vo_path = value.get('female', {}).get('vo', {}).get('main', 'N/A')
            if '{}' in vo_path:
                vo_path = vo_path.split('{}', 1)[-1]
            path = value.get('_path', 'N/A')

            # Découper le chemin en "Origine" et "Quête"
            path_parts = path.split('/', 1)
            origine_2 = path_parts[0] if len(path_parts) > 0 else 'N/A'
            quete = path_parts[1].split('{}', 1)[-1] if len(path_parts) > 1 else 'N/A'

            # Appliquer les filtres
            match = True
            for i, entry in enumerate(filters):
                if entry.get() and entry.get().lower() not in str((key, sous_titres, origine_2, vo_path, origine_2, quete)[i]).lower():
                    match = False
                    break

            if match:
                item_id = tree.insert("", tk.END, values=(key, sous_titres, origine_2, vo_path, origine_2, quete))
                if vo_path == "N/A":
                    tree.item(item_id, tags=('na_audio',))

    filter_button = tk.Button(filter_frame, text="Appliquer les filtres", command=apply_filters)
    filter_button.grid(row=1, column=len(columns), padx=5)

    reset_filter_button = tk.Button(filter_frame, text="Réinitialiser les filtres", command=lambda: reset_filters(tree, filters))
    reset_filter_button.grid(row=1, column=len(columns) + 1, padx=5)

"""