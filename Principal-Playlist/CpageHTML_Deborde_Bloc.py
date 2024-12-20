import os
from general_functions import get_Perso_from_Wem, charger_sous_titres_from_JSON_playlist

class PageHTML:
    def __init__(self, sequence, file_projet):
        """
        Initialise la classe PageHTML avec une séquence et un chemin de projet.

        :param sequence: Objet Sequence contenant les étapes et les blocs.
        :param file_projet: Chemin du fichier projet pour déterminer l'emplacement de sortie.
        """
        self.sequence = sequence
        self.file_projet = file_projet

    def generate_HeaderStyle(self, project_name):
        """Génère l'en-tête HTML et le style CSS."""
        html_content = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{project_name}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 20px;
                }}
                .diagram-container {{
                    position: relative;
                    width: 100%;
                    max-width: 1000px;
                    margin: 0 auto;
                    height: auto;
                }}
                .node {{
                    background-color: #e8f4e8;
                    border: 1px solid #4caf50;
                    border-radius: 8px;
                    padding: 10px;
                    text-align: center;
                    width: 200px;
                    position: absolute;
                    box-sizing: border-box;
                    z-index: 2;
                    overflow-wrap: break-word;
                    word-wrap: break-word;
                    height: auto;
                    min-height: 60px;
                }}
                .node .title {{
                    font-weight: bold;
                    margin-bottom: 5px;
                }}
                svg {{
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: auto;
                    pointer-events: none;
                    z-index: 1;
                }}
                line {{
                    stroke: blue;
                    stroke-width: 2;
                }}
            </style>
        </head>
        """
        return html_content

    def generate_project_html(self):
        """Génère une page HTML représentant les étapes, les blocs et les connexions du projet."""
        project_name = os.path.splitext(os.path.basename(self.file_projet))[0]
        output_dir = os.path.join(os.path.dirname(self.file_projet), f"{project_name}_files")
        os.makedirs(output_dir, exist_ok=True)

        html_filename = os.path.join(output_dir, f"{project_name}.html")

        html_content = self.generate_HeaderStyle(project_name)
        html_content += f"""
        <body>
            <h1 style="text-align:center;">{project_name}</h1>
            <div class="diagram-container">
                <svg id="svg-canvas">
        """

        # Ajouter les connexions avant les blocs pour éviter les problèmes de superposition
        block_positions = {}
        current_y = 20
        step_spacing = 120
        horizontal_spacing = 200
        max_block_height_per_step = {}

        for etape in self.sequence.etapes:
            num_blocs = len(etape.blocs)
            total_width = num_blocs * (200 + horizontal_spacing) - horizontal_spacing
            start_x = (1000 - total_width) // 2
            max_block_height = 0

            for i, block in enumerate(etape.blocs):
                x = start_x + i * (200 + horizontal_spacing)
                y = current_y
                block_height = 60 + (len(block.comment) // 20) * 20
                max_block_height = max(max_block_height, block_height)
                block_positions[block.identifiant] = (x, y, block_height)

            max_block_height_per_step[current_y] = max_block_height
            current_y += step_spacing + max_block_height

        diagram_height = current_y + step_spacing
        html_content = html_content.replace('<svg id="svg-canvas">', f'<svg id="svg-canvas" style="height: {diagram_height}px;">')

        for etape in self.sequence.etapes:
            for block in etape.blocs:
                for next_block in block.blocs_suivants:
                    start_x, start_y, start_height = block_positions[block.identifiant]
                    end_x, end_y, _ = block_positions[next_block.identifiant]

                    start_x += 100  # Centre du bloc
                    start_y += start_height  # Bas du bloc
                    end_x += 100    # Centre du bloc suivant

                    html_content += f"""
                    <line x1="{start_x}" y1="{start_y}" x2="{end_x}" y2="{end_y}" />
                    """

        html_content += "</svg>\n"

        # Ajouter les blocs
        current_y = 20
        for etape in self.sequence.etapes:
            num_blocs = len(etape.blocs)
            total_width = num_blocs * (200 + horizontal_spacing) - horizontal_spacing
            start_x = (1000 - total_width) // 2

            for i, block in enumerate(etape.blocs):
                x = start_x + i * (200 + horizontal_spacing)
                y = current_y
                _, _, block_height = block_positions[block.identifiant]
                html_content += f"""
                <div class="node" id="block-{block.identifiant}" style="top: {y}px; left: {x}px; height: {block_height}px;">
                    <div class="title">{block.title}</div>
                    <div>{charger_sous_titres_from_JSON_playlist(block.playlist_lien)}</div>

                </div>
                """

            current_y += step_spacing + max_block_height_per_step[current_y]

        html_content += "</div>\n</body>\n</html>"

        with open(html_filename, "w", encoding="utf-8") as file:
            file.write(html_content)

        print(f"Page HTML générée avec succès : {html_filename}")
