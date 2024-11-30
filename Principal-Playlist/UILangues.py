def change_language(lang):
    global current_language
    current_language = lang

    # Mettre à jour les textes des widgets existants
    add_button.config(text=_("add_to_playlist"))
    move_up_button.config(text=_("move_up"))
    move_down_button.config(text=_("move_down"))
    play_button.config(text=_("play"))
    stop_button.config(text=_("stop"))
    load_button.config(text=_("load_playlist"))
    save_button.config(text=_("save_playlist"))
    clear_button.config(text=_("clear_playlist"))
