import os
from general_functions import charger_sous_titres_from_JSON_playlist

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
                    border-top: 2px solid #33acff;
                    border-bottom: 2px solid #33acff;
                    border-radius: 8px;
                    background-color: #ffffff;
                    width: 400px;
                    text-align: left;
                }}
                .block-subtitles {{
                    font-size: 14px;
                    margin-top: 5px;
                }}
                .block-subtitles div {{
                    font-weight: normal;
                }}
                .block-subtitles div strong {{
                    font-weight: bold;
                    color:  #33acff;
                }}
                .block-subtitles div commentaire {{
                    font-weight: bold;
                    color:  #4caf50;
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
            </style>
        </head>
        """

    def generate_project_html(self):
        project_name = os.path.splitext(os.path.basename(self.file_projet))[0]
        output_dir = os.path.join(os.path.dirname(self.file_projet), f"{project_name}_files")
        os.makedirs(output_dir, exist_ok=True)

        html_filename = os.path.join(output_dir, f"{project_name}.html")
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
                    perso = subtitle.get("perso", "Inconnu").capitalize()
                    if perso.strip():  # Vérifie si le texte est vide ou contient uniquement des espaces
                        perso = perso + " : " 
                    sous_titre = subtitle.get("sous_titre", "")
                    #html_content += f"<div><strong>{perso}</strong> {sous_titre}</div>\n"
                    html_content += f"<div><commentaire>{perso}</commentaire> {sous_titre}</div>\n"
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

        # Ajouter le script JS pour calculer les positions des lignes
        html_content += "<script>\n"
        html_content += "document.addEventListener('DOMContentLoaded', function () {\n"
        html_content += "    const svg = document.getElementById('connections');\n"
        html_content += "    const lines = document.querySelectorAll('line');\n"
        html_content += "    function updateLinePositions() {\n"
        html_content += "        lines.forEach(line => {\n"
        html_content += "            const startBlock = document.getElementById(line.dataset.start);\n"
        html_content += "            const endBlock = document.getElementById(line.dataset.end);\n"
        html_content += "            if (startBlock && endBlock) {\n"
        html_content += "                const startRect = startBlock.getBoundingClientRect();\n"
        html_content += "                const endRect = endBlock.getBoundingClientRect();\n"
        html_content += "                const svgRect = svg.getBoundingClientRect();\n"
        html_content += "                line.setAttribute('x1', startRect.left + startRect.width / 2 - svgRect.left);\n"
        html_content += "                line.setAttribute('y1', startRect.bottom - svgRect.top);\n"
        html_content += "                line.setAttribute('x2', endRect.left + endRect.width / 2 - svgRect.left);\n"
        html_content += "                line.setAttribute('y2', endRect.top - svgRect.top);\n"
        html_content += "            }\n"
        html_content += "        });\n"
        html_content += "    }\n"
        html_content += "    setTimeout(updateLinePositions, 100);\n"
        html_content += "});\n"
        html_content += "</script>\n"

        html_content += "</body></html>"

        with open(html_filename, "w", encoding="utf-8") as file:
            file.write(html_content)

        print(f"Page HTML générée avec succès : {html_filename}")
