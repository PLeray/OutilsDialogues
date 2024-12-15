import os
import math
import json

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
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{project_name}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f9f9f9;
                    margin: 0;
                    padding: 0;
                }}
                .canvas {{
                    position: relative;
                    width: 100%;
                    height: auto;
                    margin: 50px auto;
                    background-color: white;
                    border: 1px solid #ccc;
                }}
                .block {{
                    position: absolute;
                    width: 400px;
                    min-height: 100px;
                    background-color: #a0e99b;
                    border: 2px solid #4CAF50;
                    text-align: center;
                    padding: 10px;
                    border-radius: 5px;
                    font-weight: bold;
                    box-sizing: border-box;
                }}
                svg {{
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    pointer-events: none; /* Les SVG ne bloquent pas les clics */
                }}
                line {{
                    stroke: blue;
                    stroke-width: 2;
                }}
            </style>
            <script>
                function drawLines() {{
                    const svg = document.getElementById('svg-canvas');
                    svg.innerHTML = ''; // Réinitialiser le SVG

                    const lines = JSON.parse('{self.generate_connections_json()}');

                    lines.forEach(line => {{
                        const startElement = document.getElementById(line.start);
                        const endElement = document.getElementById(line.end);

                        if (startElement && endElement) {{
                            const startRect = startElement.getBoundingClientRect();
                            const endRect = endElement.getBoundingClientRect();

                            const startX = startRect.left + startRect.width / 2 - svg.getBoundingClientRect().left;
                            const startY = startRect.bottom - svg.getBoundingClientRect().top;
                            const endX = endRect.left + endRect.width / 2 - svg.getBoundingClientRect().left;
                            const endY = endRect.top - svg.getBoundingClientRect().top;

                            const lineElem = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                            lineElem.setAttribute('x1', startX);
                            lineElem.setAttribute('y1', startY);
                            lineElem.setAttribute('x2', endX);
                            lineElem.setAttribute('y2', endY);
                            svg.appendChild(lineElem);
                        }}
                    }});
                }}

                window.addEventListener('load', drawLines);
                window.addEventListener('resize', drawLines);
            </script>
        </head>
        """
        return html_content
    
    def generate_connections_json(self):
        """Génère un JSON des connexions pour JavaScript."""
        connections = []
        for etape in self.sequence.etapes:
            for block in etape.blocs:
                for next_block in block.blocs_suivants:
                    connections.append({
                        "start": f"block-{block.identifiant}",
                        "end": f"block-{next_block.identifiant}"
                    })
        return json.dumps(connections)

    def generate_project_html(self):
        """Génère une page HTML représentant les étapes, les blocs et les connexions du projet."""
        project_name = os.path.splitext(os.path.basename(self.file_projet))[0]
        output_dir = os.path.join(os.path.dirname(self.file_projet), f"{project_name}_files")
        os.makedirs(output_dir, exist_ok=True)

        html_filename = os.path.join(output_dir, f"{project_name}.html")

        print("==> Génération de la page HTML...")
        html_content = self.generate_HeaderStyle(project_name)
        html_content += """
        <body>
            <h1 style="text-align:center;">{project_name}</h1>
            <div class="canvas">
                <svg id="svg-canvas"></svg>
        """.format(project_name=project_name)

        current_y = 50
        step_spacing = 250
        horizontal_spacing = 150

        for etape in self.sequence.etapes:
            num_blocs = len(etape.blocs)
            total_width = num_blocs * (400 + horizontal_spacing) - horizontal_spacing
            start_x = (1200 - total_width) // 2

            for i, block in enumerate(etape.blocs):
                x = start_x + i * (400 + horizontal_spacing)
                y = current_y
                html_content += f"""
                <div id="block-{block.identifiant}" class="block" style="top: {y}px; left: {x}px;">
                    {block.identifiant}<br>{block.title}<br>{block.comment}
                </div>
                """
            current_y += step_spacing

        html_content += """
            </div>
        </body>
        </html>
        """

        with open(html_filename, "w", encoding="utf-8") as file:
            file.write(html_content)

        print(f"==> Page HTML générée avec succès : {html_filename}")
