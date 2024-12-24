import os
from general_functions import charger_sous_titres_from_JSON_playlist
from LectureOgg import fusionner_audio_json
import global_variables  # Importer les variables globales

class PageHTML:
    def __init__(self, sequence, file_projet):
        self.sequence = sequence
        self.file_projet = file_projet

    def generate_HeaderStyle(self, project_name):
        return f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{project_name}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #ffffff;
                    margin: 0;
                    padding: 20px;
                }}
                .step-container {{
                    margin-bottom: 20px;
                    padding: 10px;
                    border-top: 1px solid #bbbbbb;
                    background-color: #f4f4f4;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    position: relative;
                }}
                .step-title {{
                    font-size: 9px;
                    font-weight: bold;
                    margin-bottom: 10px;
                    position: absolute;
                    color:  #bbbbbb;
                    top: 10px;
                    left: 10px;
                }}
                .block-container {{
                    display: flex;
                    justify-content: center;
                    gap: 100px; /* Augmente l'espacement entre les blocs */
                    flex-wrap: wrap;
                }}
                .block {{
                    padding: 10px;
                    padding-top: 0px;
                    padding-right: 25px;
                    border-top: 2px solid #33acff;
                    border-bottom: 2px solid #33acff;
                    border-radius: 8px;
                    background-color: #ffffff;
                    width: 400px;
                    text-align: left;
                    position: relative; /* Permet au bouton d’être positionné par rapport au bloc */
                }}
                .block-subtitles {{
                    font-size: 14px;
                    margin-top: 5px;
                }}
                .block-subtitles div {{
                    font-weight: normal;
                }}
                .block-subtitles div normal {{
                    color:  #444444;
                }}                
                .block-subtitles div perso {{
                    font-weight: bold;
                    color:  #33acff;
                }}
                .block-subtitles div commentaire {{
                    font-weight: normal;
                    color:  #4b00a0;
                    font-style: oblique;
                    display: block; /* S'assure que `commentaire` est traité comme un bloc (comme un paragraphe) */
                    margin-top: 15px; /* Espace avant le commentaire */
                    margin-bottom: 15px; /* Espace après le commentaire */
                }}      
                .block-subtitles div action {{
                    font-weight: normal;
                    color:  #00598c;
                    display: block; /* S'assure que `commentaire` est traité comme un bloc (comme un paragraphe) */
                    margin-top: 15px; /* Espace avant le commentaire */
                    margin-bottom: 15px; /* Espace après le commentaire */
                }}   
                .block-subtitles div message-sent {{
                    display: block;
                    margin: 10px 0;
                    padding: 10px;
                    border-radius: 8px;
                    max-width: 300px;
                    text-align: left;
                    word-wrap: break-word;
                    width: fit-content;                
                    background-color: #dcf8c6;
                    margin-left: auto;
                }}  
                .block-subtitles div message-received {{
                    display: block;
                    margin: 10px 0;
                    padding: 10px;
                    border-radius: 8px;
                    max-width: 300px;
                    text-align: left;
                    word-wrap: break-word;
                    width: fit-content;                
                    background-color: #f1f1f1;
                    margin-right: auto;
                }}                                                                             
                svg {{
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 10000px; /* Ajusté pour inclure toutes les étapes */
                    pointer-events: none;
                }}
                line {{
                    stroke: #33acff;
                    stroke-width: 2;
                }}
                .audio-button {{
                    width: 60px;
                    height: 60px;
                    background-color: #33acff;
                    border: 3px solid white;
                    border-radius: 50%;
                    position: absolute; /* Permet de placer le bouton indépendamment */
                    top: 50%; /* Centre verticalement le bouton */
                    right: -30px; /* Aligne le bouton à droite du bloc */
                    transform: translateY(-50%); /* Ajuste pour un centrage parfait */
                    cursor: pointer;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                }}
                .audio-button:hover {{
                    background-color: #007bb5;
                }}
                .audio-button::before {{
                    content: '';
                    position: absolute;
                    transition: all 0.3s ease;
                }}
                .audio-button.play::before {{
                    width: 0;
                    height: 0;
                    border-left: 15px solid white;
                    border-top: 10px solid transparent;
                    border-bottom: 10px solid transparent;
                }}
                .audio-button.pause::before {{
                    width: 10px;
                    height: 20px;
                    background-color: white;
                    box-shadow: 15px 0 0 white;
                }}                
                .audio-button::after {{
                    /* Tooltip */
                    content: "Cliquez sur le bouton ci-dessous pour lire ou arrêter le fichier audio";
                    position: absolute;
                    top: -35px; /* Décalage au-dessus du bouton */
                    right: 50%; /* Centré horizontalement par rapport au bouton */
                    transform: translateX(50%);
                    background-color: #000;
                    color: #fff;
                    padding: 5px 10px;
                    border-radius: 5px;
                    font-size: 12px;
                    white-space: nowrap;
                    opacity: 0;
                    visibility: hidden;
                    transition: opacity 0.2s ease-in-out, visibility 0.2s ease-in-out;
                    z-index: 10;
                }}
                .audio-button:hover::after {{
                    opacity: 1;
                    visibility: visible;
                }}
            </style>
        </head>
        """

    def generate_project_html(self):
        project_name = os.path.splitext(os.path.basename(self.file_projet))[0]
        output_dir = os.path.join(os.path.dirname(self.file_projet), f"{project_name}_files")
        html_filename = os.path.join(output_dir, f"{global_variables.CheminLocalization + global_variables.CheminLangue}/{project_name}.html")
        
        # Créer les dossiers si nécessaire
        os.makedirs(os.path.dirname(html_filename), exist_ok=True)

        html_content = self.generate_HeaderStyle(project_name)
        html_content += f"<body>\n<h1 style='text-align:center;'>{project_name}</h1>\n"

        block_positions = {}

        for idx, etape in enumerate(self.sequence.etapes, start=1):
            html_content += "<div class='step-container'>\n"

            # Nom de l'étape basé sur l'indice
            html_content += f"<div class='step-title'>Étape {idx}</div>\n"

            html_content += "<div class='block-container'>\n"
            for block in etape.blocs:
                block_id = f"block-{block.identifiant}"
                block_positions[block.identifiant] = block_id
                html_content += f"<div class='block' id='{block_id}'>\n"

                # Ajout des sous-titres
                subtitles = charger_sous_titres_from_JSON_playlist(block.playlist_lien)
                html_content += "<div class='block-subtitles'>\n"
                for subtitle in subtitles: 
                    prefixID = subtitle.get("type", "")
                    #prefixID = subtitle.get(global_variables.data_ID, "")[:3]
                    #print(f"prefixID : {prefixID}")
                    ["COMMENT", "ACTION", "MSG-IN", "MSG-OUT"]
                    divType = "normal"
                    if prefixID == "COMMENT":
                        divType = "commentaire"
                    elif  prefixID == "ACTION":
                        divType = "action"
                    elif  prefixID == "MSG-IN":
                        divType = "message-received"
                    elif  prefixID == "MSG-OUT":
                        divType = "message-sent"
                    else:
                        divType = "normal"
                    perso = subtitle.get("perso", "").capitalize()
                    if perso.strip():  # Vérifie si le texte est vide ou contient uniquement des espaces
                        perso = perso + " : " 
                    sous_titre = subtitle.get("sous_titre", "")

                    html_content += f"<div><{divType}><perso>{perso}</perso> {sous_titre}</{divType}></div>\n"

                html_content += f"<audio id=\"audio-{block.identifiant}\" src=\"ogg/Sound-{block.identifiant}.ogg\"></audio>\n"
                html_content += f"<button class=\"audio-button play\" onclick=\"togglePlay('{block.identifiant}')\"></button>\n"

                html_content += "</div>\n"

                html_content += "</div>\n"
            html_content += "</div>\n"

            html_content += "</div>\n"

        # Ajouter un conteneur SVG pour les lignes de liaison
        html_content += "<svg id='connections'>\n"

        for etape in self.sequence.etapes:
            for block in etape.blocs:
                for next_block in block.blocs_suivants:
                    if next_block.identifiant in block_positions:
                        html_content += f"<line x1='0' y1='0' x2='0' y2='0' data-start='block-{block.identifiant}' data-end='block-{next_block.identifiant}' />\n"
                    else:
                        print(f"Missing connection: {block.identifiant} -> {next_block.identifiant}")

        html_content += "</svg>\n"

        html_content += self.ScriptLiaison()
        html_content += self.ScriptBoutonOgg()

        html_content += "</body></html>"

        with open(html_filename, "w", encoding="utf-8") as file:
            file.write(html_content)

        print(f"Page HTML générée avec succès : {html_filename}")


    def ScriptBoutonOgg(self):
        leScript = "<script>\n"
        leScript += "function togglePlay(blockId) {\n"
        leScript += "    const audio = document.getElementById(`audio-${blockId}`);\n"
        leScript += "    const button = document.querySelector(`#block-${blockId} .audio-button`);\n"

        leScript += "    if (audio.paused || audio.ended) {\n"
        leScript += "        audio.play();\n"
        leScript += "        button.classList.remove('play');\n"
        leScript += "        button.classList.add('pause');\n"
        leScript += "    } else {\n"
        leScript += "        audio.pause();\n"
        leScript += "        button.classList.remove('pause');\n"
        leScript += "        button.classList.add('play');\n"
        leScript += "    }\n"

        leScript += "    // Réinitialiser l'état du bouton lorsqu'un audio se termine\n"
        leScript += "    audio.addEventListener('ended', () => {\n"
        leScript += "        button.classList.remove('pause');\n"
        leScript += "        button.classList.add('play');\n"
        leScript += "    });\n"
        leScript += "}\n"
        leScript += "</script>\n"
        return leScript
    
    def ScriptLiaison(self):
        # Ajouter le script JS pour calculer les positions des lignes
        leScript = "<script>\n"
        leScript += "document.addEventListener('DOMContentLoaded', function () {\n"
        leScript += "    const svg = document.getElementById('connections');\n"
        leScript += "    const lines = document.querySelectorAll('line');\n"
        leScript += "    function updateLinePositions() {\n"
        leScript += "        lines.forEach(line => {\n"
        leScript += "            const startBlock = document.getElementById(line.dataset.start);\n"
        leScript += "            const endBlock = document.getElementById(line.dataset.end);\n"
        leScript += "            if (startBlock && endBlock) {\n"
        leScript += "                const startRect = startBlock.getBoundingClientRect();\n"
        leScript += "                const endRect = endBlock.getBoundingClientRect();\n"
        leScript += "                const svgRect = svg.getBoundingClientRect();\n"
        leScript += "                line.setAttribute('x1', startRect.left + startRect.width / 2 - svgRect.left);\n"
        leScript += "                line.setAttribute('y1', startRect.bottom - svgRect.top);\n"
        leScript += "                line.setAttribute('x2', endRect.left + endRect.width / 2 - svgRect.left);\n"
        leScript += "                line.setAttribute('y2', endRect.top - svgRect.top);\n"
        leScript += "            }\n"
        leScript += "        });\n"
        leScript += "    }\n"
        leScript += "    setTimeout(updateLinePositions, 100);\n"
        leScript += "});\n"
        leScript += "</script>\n"
        return leScript
    
    def generate_Ogg(self):
        """
        Génère des fichiers .ogg pour chaque playlist JSON des blocs du projet.
        Les fichiers sont sauvegardés dans un sous-dossier nommé '/ogg' où la page HTML est générée.
        """
        project_name = os.path.splitext(os.path.basename(self.file_projet))[0]
        output_dir = os.path.join(os.path.dirname(self.file_projet), f"{project_name}_files")
        #ogg_dir = os.path.join(output_dir, "ogg")
        ogg_dir = os.path.join(output_dir, f"{global_variables.CheminLocalization + global_variables.CheminLangue}/ogg")
        # Créer le dossier /ogg s'il n'existe pas
        os.makedirs(ogg_dir, exist_ok=True)

        for etape in self.sequence.etapes:
            for block in etape.blocs:
                playlist_lien = block.playlist_lien
                if playlist_lien and os.path.exists(playlist_lien):
                    try:
                        # Chemin du fichier .ogg
                        block_id = block.identifiant
                        output_ogg_path = os.path.join(ogg_dir, f"Sound-{block_id}.ogg")
                        print(f"output_ogg_path : {output_ogg_path}")
                        # Appeler la fonction fusionner_audio_json
                        fusionner_audio_json(chemin_json=playlist_lien, chemin_ogg=output_ogg_path)
                        print(f"Fichier .ogg généré avec succès : {output_ogg_path}")
                    except Exception as e:
                        print(f"Erreur lors de la génération du fichier .ogg pour le bloc {block.identifiant} : {e}")
                else:
                    print(f"Aucune playlist JSON valide pour le bloc {block.identifiant}")
