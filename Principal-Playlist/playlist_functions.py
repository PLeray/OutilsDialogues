# fichier: playlist_functions.py

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

# Fonction pour supprimer une ligne de la playlist via un clic droit
def remove_selected_from_playlist(event, playlist_tree):
    try:
        selected_item = playlist_tree.selection()[0]
        playlist_tree.delete(selected_item)
    except IndexError:
        pass

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
def load_playlist_from_file(playlist_tree):
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, "r") as file:
            playlist_data = json.load(file)
            # Effacer l'ancienne playlist avant de charger la nouvelle
            clear_playlist(playlist_tree)
            # Ajouter les nouvelles données dans la playlist
            for values in playlist_data:
                playlist_tree.insert("", tk.END, values=values)


