import pygame
import sys

# Initialize pygame
pygame.init()

# Constants - Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
DRAW_AREA_HEIGHT = 500  # Area for drawing
UI_HEIGHT = 100        # Area for tools and colors

FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Drawing colors available
COLORS = [
    BLACK,
    WHITE,
    (255, 0, 0),      # Red
    (0, 255, 0),      # Green
    (0, 0, 255),      # Blue
    (255, 255, 0),    # Yellow
    (255, 165, 0),    # Orange
    (128, 0, 128),    # Purple
    (255, 192, 203),  # Pink
    (0, 255, 255),    # Cyan
]

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paint Application")
clock = pygame.time.Clock()

# Font setup
font = pygame.font.SysFont("Verdana", 16)


class PaintApp:
    """Main paint application class"""

    def __init__(self):
        # Create drawing surface (canvas)
        self.canvas = pygame.Surface((SCREEN_WIDTH, DRAW_AREA_HEIGHT))
        self.canvas.fill(WHITE)

        # Current tool: 'brush', 'rectangle', 'circle', 'eraser'
        self.current_tool = 'brush'

        # Current color
        self.current_color = BLACK
        self.brush_size = 5

        # For shape drawing (rectangle/circle)
        self.start_pos = None  # Starting position when mouse is pressed
        self.temp_surface = None  # Temporary surface for preview

        # Tool button rectangles
        self.tool_buttons = {}
        # Color button rectangles
        self.color_buttons = []

        self.create_ui()

    def create_ui(self):
        """Create UI elements (tool buttons and color buttons)"""
        # Tool buttons
        button_width = 80
        button_height = 40
        button_y = DRAW_AREA_HEIGHT + 30

        tools = [
            ('brush', 'Brush'),
            ('rectangle', 'Rect'),
            ('circle', 'Circle'),
            ('eraser', 'Eraser'),
            ('clear', 'Clear')
        ]

        for i, (tool, label) in enumerate(tools):
            x = 20 + i * (button_width + 10)
            self.tool_buttons[tool] = {
                'rect': pygame.Rect(x, button_y, button_width, button_height),
                'label': label
            }

        # Color buttons
        color_size = 40
        color_start_x = 450
        color_y = DRAW_AREA_HEIGHT + 30

        for i, color in enumerate(COLORS):
            x = color_start_x + (i % 5) * (color_size + 10)
            y = color_y if i < 5 else color_y + color_size + 10
            self.color_buttons.append({
                'rect': pygame.Rect(x, y, color_size, color_size),
                'color': color
            })

    def draw_ui(self, screen):
        """Draw the UI bar with tools and colors"""
        # Draw UI background
        pygame.draw.rect(screen, GRAY, (0, DRAW_AREA_HEIGHT, SCREEN_WIDTH, UI_HEIGHT))
        pygame.draw.line(screen, DARK_GRAY, (0, DRAW_AREA_HEIGHT), (SCREEN_WIDTH, DRAW_AREA_HEIGHT), 2)

        # Draw tool buttons
        for tool, data in self.tool_buttons.items():
            rect = data['rect']
            # Highlight selected tool
            if tool == self.current_tool:
                pygame.draw.rect(screen, (150, 200, 255), rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)

            # Draw button label
            label = font.render(data['label'], True, BLACK)
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)

        # Draw color buttons
        for color_btn in self.color_buttons:
            rect = color_btn['rect']
            pygame.draw.rect(screen, color_btn['color'], rect)
            pygame.draw.rect(screen, BLACK, rect, 2)

            # Highlight selected color
            if color_btn['color'] == self.current_color:
                pygame.draw.rect(screen, (255, 0, 0), rect, 3)

        # Draw instructions
        instructions = [
            "Left Click: Draw | Drag: Create shapes",
            "Select tool, then click and drag to draw shapes"
        ]
        for i, text in enumerate(instructions):
            label = font.render(text, True, BLACK)
            screen.blit(label, (SCREEN_WIDTH - 300, DRAW_AREA_HEIGHT + 20 + i * 25))

    def handle_click(self, pos):
        """Handle mouse click in UI area"""
        # Check tool buttons
        for tool, data in self.tool_buttons.items():
            if data['rect'].collidepoint(pos):
                if tool == 'clear':
                    self.clear_canvas()
                else:
                    self.current_tool = tool
                    # Set color to white for eraser
                    if tool == 'eraser':
                        self.current_color = WHITE
                    elif self.current_tool != 'brush':
                        # Restore last color if switching from eraser
                        pass
                return True

        # Check color buttons
        for color_btn in self.color_buttons:
            if color_btn['rect'].collidepoint(pos):
                self.current_color = color_btn['color']
                # Switch from eraser to brush when color is selected
                if self.current_tool == 'eraser':
                    self.current_tool = 'brush'
                return True

        return False

    def clear_canvas(self):
        """Clear the canvas"""
        self.canvas.fill(WHITE)

    def start_drawing(self, pos):
        """Start drawing shape at position"""
        self.start_pos = pos
        # Create temporary surface for preview
        self.temp_surface = self.canvas.copy()

    def draw_shape(self, current_pos):
        """Draw shape preview while dragging"""
        if self.start_pos is None:
            return

        # Restore original canvas
        self.canvas.blit(self.temp_surface, (0, 0))

        # Calculate rectangle dimensions
        x = min(self.start_pos[0], current_pos[0])
        y = min(self.start_pos[1], current_pos[1])
        width = abs(current_pos[0] - self.start_pos[0])
        height = abs(current_pos[1] - self.start_pos[1])

        # Draw preview based on tool
        if self.current_tool == 'rectangle':
            pygame.draw.rect(self.canvas, self.current_color, (x, y, width, height))
            pygame.draw.rect(self.canvas, BLACK, (x, y, width, height), 1)

        elif self.current_tool == 'circle':
            # Calculate circle parameters
            center_x = (self.start_pos[0] + current_pos[0]) // 2
            center_y = (self.start_pos[1] + current_pos[1]) // 2
            radius = max(width, height) // 2
            pygame.draw.circle(self.canvas, self.current_color, (center_x, center_y), radius)
            pygame.draw.circle(self.canvas, BLACK, (center_x, center_y), radius, 1)

    def end_drawing(self):
        """Finish drawing shape"""
        self.start_pos = None
        self.temp_surface = None

    def draw_brush(self, pos):
        """Draw with brush or eraser at position"""
        size = self.brush_size * 3 if self.current_tool == 'eraser' else self.brush_size
        pygame.draw.circle(self.canvas, self.current_color, pos, size)

    def run(self):
        """Main game loop"""
        drawing = False  # Flag to track if we're currently drawing

        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                # Mouse button down
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        pos = event.pos

                        # Check if clicked on UI
                        if pos[1] >= DRAW_AREA_HEIGHT:
                            self.handle_click(pos)
                            continue

                        # Start drawing
                        drawing = True
                        if self.current_tool in ['rectangle', 'circle']:
                            self.start_drawing((pos[0], pos[1] - 0))  # Adjust for canvas
                        elif self.current_tool in ['brush', 'eraser']:
                            self.draw_brush((pos[0], pos[1]))

                # Mouse motion (dragging)
                if event.type == pygame.MOUSEMOTION:
                    if drawing:
                        pos = event.pos
                        # Only draw in canvas area
                        if pos[1] < DRAW_AREA_HEIGHT:
                            if self.current_tool in ['rectangle', 'circle']:
                                self.draw_shape((pos[0], pos[1]))
                            elif self.current_tool in ['brush', 'eraser']:
                                self.draw_brush((pos[0], pos[1]))

                # Mouse button up
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        drawing = False
                        if self.current_tool in ['rectangle', 'circle']:
                            self.end_drawing()

            # Draw everything
            screen.blit(self.canvas, (0, 0))
            self.draw_ui(screen)

            # Draw current tool info
            tool_text = font.render(f"Tool: {self.current_tool.capitalize()}", True, BLACK)
            screen.blit(tool_text, (10, DRAW_AREA_HEIGHT + 10))

            # Update display
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()
        sys.exit()


def main():
    """Main function"""
    app = PaintApp()
    app.run()


if __name__ == "__main__":
    main()
