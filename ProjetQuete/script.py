import tkinter as tk
from tkinter import ttk


class BlocOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Organisateur de Blocs")

        # Conteneur principal
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.grid = [[]]  # Une liste de listes pour représenter les lignes et colonnes
        self.selected_block = None  # Bloc actuellement sélectionné

        # Boutons d'action
        self.controls = tk.Frame(self.root)
        self.controls.pack(fill=tk.X)

        self.add_button = ttk.Button(self.controls, text="Ajouter un Bloc", command=self.add_block)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.up_button = ttk.Button(self.controls, text="Remonter", command=self.move_up, state=tk.DISABLED)
        self.up_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.down_button = ttk.Button(self.controls, text="Descendre", command=self.move_down, state=tk.DISABLED)
        self.down_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.add_left_button = ttk.Button(self.controls, text="Ajouter à Gauche", command=self.add_left, state=tk.DISABLED)
        self.add_left_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.add_right_button = ttk.Button(self.controls, text="Ajouter à Droite", command=self.add_right, state=tk.DISABLED)
        self.add_right_button.pack(side=tk.LEFT, padx=5, pady=5)

    def add_block(self):
        """Ajoute un nouveau bloc à la dernière ligne."""
        block_number = sum(len(row) for row in self.grid) + 1
        frame = tk.Frame(self.canvas, bg="lightgray", relief=tk.RAISED, borderwidth=2)
        label = tk.Label(frame, text=f"Bloc {block_number}", bg="lightgray")
        label.pack(padx=10, pady=10)

        # Bind click events
        label.bind("<Button-1>", lambda e, f=frame: self.select_block(f))

        # Ajouter le bloc à la dernière ligne
        if not self.grid[-1]:
            self.grid[-1].append(frame)
        else:
            self.grid.append([frame])
        self.refresh_blocks()

    def refresh_blocks(self):
        """Réorganise et affiche les blocs."""
        self.canvas.delete("all")  # Efface tout sur le canvas

        x_start, y_start = 10, 10
        y = y_start
        for row in self.grid:
            x = x_start
            for block in row:
                self.canvas.create_window(x, y, window=block, anchor="nw")
                x += block.winfo_reqwidth() + 10
            y += 50  # Hauteur entre les lignes

        self.update_buttons_state()

    def select_block(self, block):
        """Sélectionne un bloc."""
        if self.selected_block:
            self.selected_block.config(bg="lightgray")
        self.selected_block = block
        self.selected_block.config(bg="red")
        self.update_buttons_state()

    def move_up(self):
        """Monte le bloc sélectionné d'une ligne."""
        for row in self.grid:
            if self.selected_block in row:
                index = row.index(self.selected_block)
                row.remove(self.selected_block)
                if row == []:
                    self.grid.remove(row)
                self.grid.insert(max(self.grid.index(row) - 1, 0), [self.selected_block])
                self.refresh_blocks()
                return

    def move_down(self):
        """Descend le bloc sélectionné d'une ligne."""
        for row in self.grid:
            if self.selected_block in row:
                index = row.index(self.selected_block)
                row.remove(self.selected_block)
                if row == []:
                    self.grid.remove(row)
                self.grid.insert(min(self.grid.index(row) + 1, len(self.grid)), [self.selected_block])
                self.refresh_blocks()
                return

    def add_left(self):
        """Ajoute le bloc sélectionné à gauche du bloc au-dessus."""
        for i, row in enumerate(self.grid):
            if self.selected_block in row:
                index = row.index(self.selected_block)
                if i > 0:
                    self.grid[i - 1].insert(0, self.selected_block)
                    row.remove(self.selected_block)
                    if not row:
                        self.grid.remove(row)
                    self.refresh_blocks()
                    return

    def add_right(self):
        """Ajoute le bloc sélectionné à droite du bloc au-dessus."""
        for i, row in enumerate(self.grid):
            if self.selected_block in row:
                index = row.index(self.selected_block)
                if i > 0:
                    self.grid[i - 1].append(self.selected_block)
                    row.remove(self.selected_block)
                    if not row:
                        self.grid.remove(row)
                    self.refresh_blocks()
                    return

    def update_buttons_state(self):
        """Active ou désactive les boutons en fonction de l'état."""
        if not self.selected_block:
            self.up_button.config(state=tk.DISABLED)
            self.down_button.config(state=tk.DISABLED)
            self.add_left_button.config(state=tk.DISABLED)
            self.add_right_button.config(state=tk.DISABLED)
        else:
            index_row = next((i for i, row in enumerate(self.grid) if self.selected_block in row), None)
            self.up_button.config(state=tk.NORMAL if index_row > 0 else tk.DISABLED)
            self.down_button.config(state=tk.NORMAL if index_row < len(self.grid) - 1 else tk.DISABLED)
            self.add_left_button.config(state=tk.NORMAL if index_row > 0 else tk.DISABLED)
            self.add_right_button.config(state=tk.NORMAL if index_row > 0 else tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = BlocOrganizerApp(root)
    root.mainloop()
