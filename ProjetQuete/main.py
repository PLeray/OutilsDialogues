import pygame
import json

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 50
STEP_HEIGHT = 100
GRID_COLOR = (200, 200, 200)
BLOCK_COLOR = (50, 150, 250)
PRECEDENT_COLOR = (250, 100, 100)
SUIVANT_COLOR = (100, 250, 100)
SELECTED_STEP_COLOR = (255, 165, 0)  # Orange
CONNECTION_COLOR = (0, 100, 0)
MENU_COLOR = (240, 240, 240)
FPS = 30

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bloc Manipulation par Étapes")
clock = pygame.time.Clock()

# Classes
class Block:
    def __init__(self, x, etape, index):
        self.x = x
        self.etape = etape
        self.index = index  # Index within the step for ordering
        self.precedents = []
        self.suivants = []
        
    def to_dict(self):
        """Serialize the block."""
        return {
            "x": self.x,
            "etape": self.etape,
            "index": self.index,
            "precedents": [(b.etape, b.index) for b in self.precedents],
            "suivants": [(b.etape, b.index) for b in self.suivants],
        }        

    def draw(self, highlight=None):
        y = self.etape * STEP_HEIGHT + STEP_HEIGHT // 2 - BLOCK_SIZE // 2
        rect = pygame.Rect(self.x, y, 5*BLOCK_SIZE, BLOCK_SIZE)
        if highlight == "precedent":
            color = PRECEDENT_COLOR
        elif highlight == "suivant":
            color = SUIVANT_COLOR
        else:
            color = BLOCK_COLOR
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, CONNECTION_COLOR, rect, 2)

    def center_position(self, step_width, block_count):
        """Re-center the block horizontally based on step size."""
        block_spacing = step_width // max(1, block_count + 1)
        self.x = (self.index + 1) * block_spacing - BLOCK_SIZE // 2

class Grid:
    def __init__(self):
        self.steps = []  # List of steps, each step contains blocks
        self.selected_step = None  # Index of the selected step
        self.selected_block = None  # Block currently selected for movement
    
    def add_step(self, index=None):
        """Add a new step."""
        if index is None:
            self.steps.append([])
        else:
            self.steps.insert(index + 1, [])

    def select_step(self, y):
        """Select a step based on vertical position."""
        step_index = y // STEP_HEIGHT
        if 0 <= step_index < len(self.steps):
            self.selected_step = step_index

    def remove_step(self, step_index):
        """Remove an entire step and all its blocks."""
        if 0 <= step_index < len(self.steps):
            del self.steps[step_index]
            # Update the step indices for remaining steps
            for i, step_blocks in enumerate(self.steps):
                for block in step_blocks:
                    block.etape = i

    def add_block(self, step_index):
        """Add a new block to a specific step."""
        step_blocks = self.steps[step_index]
        block = Block(0, step_index, len(step_blocks))
        step_blocks.append(block)
        self.recenter_blocks(step_index)

    def remove_block(self, step_index, block):
        """Remove a block and its connections."""
        step_blocks = self.steps[step_index]
        if block in step_blocks:
            # Remove connections to/from the block
            for b in step_blocks:
                if block in b.precedents:
                    b.precedents.remove(block)
                if block in b.suivants:
                    b.suivants.remove(block)
            step_blocks.remove(block)
            self.recenter_blocks(step_index)

    def block_at(self, x, y):
        """Find a block at the given screen coordinates."""
        for step_index, step_blocks in enumerate(self.steps):
            step_y = step_index * STEP_HEIGHT
            if step_y <= y < step_y + STEP_HEIGHT:
                for block in step_blocks:
                    block_y = step_y + STEP_HEIGHT // 2 - BLOCK_SIZE // 2
                    block_rect = pygame.Rect(block.x, block_y, BLOCK_SIZE, BLOCK_SIZE)
                    if block_rect.collidepoint(x, y):
                        return block, step_index
        return None, None

    def connect_blocks(self, source, target, connection_type):
        """Connect two blocks."""
        if source.etape < target.etape :
            if source not in target.precedents:  # Avoid duplicates
                target.precedents.append(source)
            if target not in source.suivants:  # Avoid duplicates
                source.suivants.append(target)
                return True
        else :
            print("l'étape de la source doit etre inférieur à la target")
            return False

    def clear_connections(self, block):
        """Clear all connections of a block."""
        block.precedents.clear()
        block.suivants.clear()

    def recenter_blocks(self, step_index):
        """Re-center all blocks in the specified step."""
        step_blocks = self.steps[step_index]
        step_width = SCREEN_WIDTH
        for i, block in enumerate(step_blocks):
            block.index = i
            block.center_position(step_width, len(step_blocks))

    def move_block(self, step_index, direction):
        """Move the selected block left or right within its step."""
        step_blocks = self.steps[step_index]
        if self.selected_block in step_blocks:
            index = step_blocks.index(self.selected_block)
            new_index = max(0, min(len(step_blocks) - 1, index + direction))
            step_blocks[index], step_blocks[new_index] = step_blocks[new_index], step_blocks[index]
            self.recenter_blocks(step_index)

    def align_blocks(self):
        """Align blocks with simple connections vertically."""
        for step_blocks in self.steps:
            for block in step_blocks:
                # Check for a simple "suivant" connection
                if len(block.suivants) == 1 and len(block.precedents) == 0:
                    suivant = block.suivants[0]
                    suivant.x = block.x
                # Check for a simple "precedent" connection
                if len(block.precedents) == 1 and len(block.suivants) == 0:
                    precedent = block.precedents[0]
                    precedent.x = block.x

    def draw(self, selected_blocks=None):
        """Draw steps, blocks, and connections."""
        # Draw steps
        for i, step in enumerate(self.steps):
            step_y = i * STEP_HEIGHT
            rect = pygame.Rect(0, step_y, SCREEN_WIDTH, STEP_HEIGHT)
            color = SELECTED_STEP_COLOR if i == self.selected_step else GRID_COLOR
            pygame.draw.rect(screen, color, rect, 2)

        # Draw blocks
        for step_blocks in self.steps:
            for block in step_blocks:
                highlight = None
                if selected_blocks:
                    if block in selected_blocks.get("precedents", []):
                        highlight = "precedent"
                    elif block in selected_blocks.get("suivants", []):
                        highlight = "suivant"
                block.draw(highlight)

        # Draw connections (above blocks)
        for step_blocks in self.steps:
            for block in step_blocks:
                for next_block in block.suivants:
                    start_pos = (block.x + BLOCK_SIZE // 2, block.etape * STEP_HEIGHT + STEP_HEIGHT // 2)
                    end_pos = (next_block.x + BLOCK_SIZE // 2, next_block.etape * STEP_HEIGHT + STEP_HEIGHT // 2)
                    pygame.draw.line(screen, CONNECTION_COLOR, start_pos, end_pos, 3)

    def save_state(self, filename):
        """Save the grid state to a JSON file."""
        data = {
            "steps": [
                [block.to_dict() for block in step_blocks]
                for step_blocks in self.steps
            ]
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)  # Add indentation for pretty-printing
        print(f"State saved to {filename}")

    def load_state(self, filename):
        """Load the grid state from a JSON file."""
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            self.steps = []
            for step_blocks in data["steps"]:
                step = []
                for block_data in step_blocks:
                    block = Block(
                        block_data["x"],
                        block_data["etape"],
                        block_data["index"]
                    )
                    step.append(block)
                self.steps.append(step)

            # Reconnect blocks
            for step_blocks, serialized_blocks in zip(self.steps, data["steps"]):
                for block, block_data in zip(step_blocks, serialized_blocks):
                    block.precedents = [
                        self.steps[p_etape][p_index]
                        for p_etape, p_index in block_data["precedents"]
                    ]
                    block.suivants = [
                        self.steps[s_etape][s_index]
                        for s_etape, s_index in block_data["suivants"]
                    ]
            print(f"State loaded from {filename}")
        except FileNotFoundError:
            print(f"File {filename} not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON.")

# Context menu
def draw_menu(x, y, options):
    """Draw a context menu at the given position."""
    font = pygame.font.Font(None, 24)
    menu_height = 30 * len(options)
    menu_width = max(font.size(option)[0] for option in options) + 20
    menu_rect = pygame.Rect(x, y, menu_width, menu_height)
    pygame.draw.rect(screen, MENU_COLOR, menu_rect)
    pygame.draw.rect(screen, CONNECTION_COLOR, menu_rect, 2)

    for i, option in enumerate(options):
        text = font.render(option, True, (0, 0, 0))
        screen.blit(text, (x + 10, y + i * 30))

    return menu_rect

# Main loop
def main():
    running = True
    grid = Grid()
    grid.add_step()  # Add initial step
    selected_blocks = {"precedents": [], "suivants": []}
    menu_active = False
    menu_rect = None
    menu_options = []
    menu_action = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Input Clavier ############    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:  # Add a new step
                    if grid.selected_step is not None:
                        grid.add_step(grid.selected_step)
                    else:
                        grid.add_step()
                    print("Added a new step.")
                elif event.key == pygame.K_a:  # Add a block to the selected step
                    if grid.selected_step is not None:
                        grid.add_block(grid.selected_step)
                        print(f"Added a block to step {grid.selected_step}.")
                
                elif event.key == pygame.K_c:  # Validate connections
                    # Create connections based on selected blocks
                    for prev in selected_blocks["precedents"]:
                        #grid.connect_blocks(next_block, prev, "precedents")
                        for next_block in selected_blocks["suivants"]:
                            if grid.connect_blocks(prev, next_block, "suivant") :
                                print("Connections validated.")
                    selected_blocks = {"precedents": [], "suivants": []}
                    grid.align_blocks()  # Align blocks after validation

                elif event.key == pygame.K_s:  # Save state
                    grid.save_state("projet.json")

                elif event.key == pygame.K_l:  # Load state
                    grid.load_state("projet.json")

                elif event.key == pygame.K_LEFT:  # Move block left
                    if grid.selected_block:
                        grid.move_block(grid.selected_block.etape, -1)
                
                elif event.key == pygame.K_RIGHT:  # Move block right
                    if grid.selected_block:
                        grid.move_block(grid.selected_block.etape, 1)
            # Clic Souris  ############              
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # Menu clic Droit ##########
                if menu_active and menu_rect and not menu_rect.collidepoint(x, y):
                    menu_active = False  # Close menu if clicking outside
                
                # clic Gauche sur menu du clic droit########## 
                if event.button == 1 and menu_active and menu_rect:  # Left click on menu du clic droit
                    for i, option in enumerate(menu_options):
                        if menu_rect.collidepoint(x, y + i * 30):
                            if option == "Supprimer les liaisons" and menu_action[0] == "block":
                                grid.clear_connections(menu_action[1])
                                print("Cleared connections.")
                            elif option == "Supprimer le bloc" and menu_action[0] == "block":
                                grid.remove_block(menu_action[2], menu_action[1])
                                print("Removed block.")
                            elif option == "Supprimer l'étape" and menu_action[0] == "step":
                                grid.remove_step(menu_action[1])
                                print("Removed step.")
                            menu_active = False
                            break
                    menu_active = False                    
                
                # clic Gauche ##########                    
                elif event.button == 1:  # Left click
                    block, step_index = grid.block_at(x, y)
                    if block:  # Select block for connections
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            selected_blocks["precedents"].append(block)
                            print(f"Block ({block.x}, Step {block.etape}) ajouté comme precedent.")
                        elif pygame.key.get_mods() & pygame.KMOD_CTRL:
                            selected_blocks["suivants"].append(block)
                            print(f"Block ({block.x}, Step {block.etape}) ajouté comme suivant.")
                        else: #Selection de base d'un Bloc
                            grid.selected_block = block
                            print(f"Selected block ({block.x}, Step {block.etape}).")
                    else:  #Selection de base d'uns Etape step
                        grid.select_step(y)
                        print(f"Selected step {grid.selected_step}.")
                
                # clic Droit ########## 
                elif event.button == 3:  # Right click for context menu
                    block, step_index = grid.block_at(x, y)
                    if block:
                        menu_options = ["Supprimer les liaisons", "Supprimer le bloc"]
                        menu_action = ("block", block, step_index)
                        menu_active = True
                    elif grid.selected_step is not None:
                        menu_options = ["Supprimer l'étape"]
                        menu_action = ("step", grid.selected_step)
                        menu_active = True
                    if menu_active:
                        menu_rect = draw_menu(x, y, menu_options)
                        print(f"Menu Etape opened at ({x}, {y})")   
               

        screen.fill((255, 255, 255))
        grid.draw(selected_blocks)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
