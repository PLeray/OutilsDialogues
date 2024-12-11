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
CONNECTION_COLOR = (0, 0, 0)
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
        rect = pygame.Rect(self.x, y, BLOCK_SIZE, BLOCK_SIZE)
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

    def connect_blocks(self, source, target, connection_type):
        """Connect two blocks."""
        if connection_type == "precedent":
            target.precedents.append(source)
        elif connection_type == "suivant":
            source.suivants.append(target)

    def save_state(self, filename):
        """Save the grid state to a JSON file."""
        data = {
            "steps": [
                [block.to_dict() for block in step_blocks]
                for step_blocks in self.steps
            ]
        }
        with open(filename, "w") as f:
            json.dump(data, f)
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
    
    def add_step(self, index=None):
        """Add a new step."""
        if index is None:
            self.steps.append([])
        else:
            self.steps.insert(index + 1, [])

    def add_block(self, step_index):
        """Add a new block to a specific step."""
        step_blocks = self.steps[step_index]
        block = Block(0, step_index, len(step_blocks))
        step_blocks.append(block)
        self.recenter_blocks(step_index)

    def recenter_blocks(self, step_index):
        """Re-center all blocks in the specified step."""
        step_blocks = self.steps[step_index]
        step_width = SCREEN_WIDTH
        for i, block in enumerate(step_blocks):
            block.index = i
            block.center_position(step_width, len(step_blocks))

    def remove_block(self, step_index, block):
        """Remove a block and its connections."""
        step_blocks = self.steps[step_index]
        if block in step_blocks:
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

    def select_step(self, y):
        """Select a step based on vertical position."""
        step_index = y // STEP_HEIGHT
        if 0 <= step_index < len(self.steps):
            self.selected_step = step_index

    def connect_blocks(self, source, target, connection_type):
        """Connect two blocks."""
        if connection_type == "precedent":
            target.precedents.append(source)
        elif connection_type == "suivant":
            source.suivants.append(target)

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

# Main loop
def main():
    running = True
    grid = Grid()
    grid.add_step()  # Add initial step
    selected_blocks = {"precedents": [], "suivants": []}

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
                        for next_block in selected_blocks["suivants"]:
                            grid.connect_blocks(prev, next_block, "suivant")
                    selected_blocks = {"precedents": [], "suivants": []}
                    grid.align_blocks()  # Align blocks after validation
                    print("Connections validated.")

                elif event.key == pygame.K_s:  # Save state
                    grid.save_state("grid.json")
                elif event.key == pygame.K_l:  # Load state
                    grid.load_state("grid.json")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if event.button == 1:  # Left click
                    block, step_index = grid.block_at(x, y)
                    if block:  # Select block for connections
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            selected_blocks["precedents"].append(block)
                            print(f"Block ({block.x}, Step {block.etape}) added as precedent.")
                        else:
                            selected_blocks["suivants"].append(block)
                            print(f"Block ({block.x}, Step {block.etape}) added as suivant.")
                    else:  # Select step
                        grid.select_step(y)
                        print(f"Selected step {grid.selected_step}.")
                elif event.button == 3:  # Right click
                    if grid.selected_step is not None:
                        grid.add_block(grid.selected_step)

        screen.fill((255, 255, 255))
        grid.draw(selected_blocks)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
