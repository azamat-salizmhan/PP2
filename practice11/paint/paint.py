import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
CANVAS_HEIGHT = 580
UI_HEIGHT = 120

FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
LIGHT_GRAY = (220, 220, 220)

# Drawing colors
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
pygame.display.set_caption("Paint Application - Practice 11")
clock = pygame.time.Clock()

# Font setup
font = pygame.font.SysFont("Arial", 14)
title_font = pygame.font.SysFont("Arial", 16, bold=True)


class PaintApp:
    """Paint application with multiple drawing tools"""

    def __init__(self):
        # Create canvas
        self.canvas = pygame.Surface((SCREEN_WIDTH, CANVAS_HEIGHT))
        self.canvas.fill(WHITE)

        # Drawing settings
        self.current_tool = 'brush'
        self.previous_tool = 'brush'  # Store tool before eraser
        self.current_color = BLACK
        self.previous_color = BLACK    # Store color before eraser
        self.brush_size = 3

        # For shape drawing
        self.start_pos = None
        self.temp_surface = None

        # UI elements
        self.tool_buttons = {}
        self.color_buttons = []
        self.create_ui()

    def create_ui(self):
        """Create tool and color buttons"""
        # Tool buttons (2 rows)
        button_width = 75
        button_height = 35
        start_y = CANVAS_HEIGHT + 20

        tools = [
            ('brush', 'Brush'),
            ('rectangle', 'Rect'),
            ('square', 'Square'),
            ('circle', 'Circle'),
            ('right_triangle', 'R-Tri'),
            ('equilateral', 'E-Tri'),
            ('rhombus', 'Rhombus'),
            ('eraser', 'Eraser'),
            ('clear', 'Clear'),
        ]

        for i, (tool, label) in enumerate(tools):
            x = 20 + i * (button_width + 8)
            self.tool_buttons[tool] = {
                'rect': pygame.Rect(x, start_y, button_width, button_height),
                'label': label
            }

        # Color buttons (below tools)
        color_size = 35
        color_start_x = 20
        color_y = CANVAS_HEIGHT + 65

        for i, color in enumerate(COLORS):
            x = color_start_x + i * (color_size + 10)
            self.color_buttons.append({
                'rect': pygame.Rect(x, color_y, color_size, color_size),
                'color': color
            })

    def draw_ui(self, screen):
        """Draw the UI bar"""
        # UI background
        pygame.draw.rect(screen, GRAY, (0, CANVAS_HEIGHT, SCREEN_WIDTH, UI_HEIGHT))
        pygame.draw.line(screen, DARK_GRAY, (0, CANVAS_HEIGHT), (SCREEN_WIDTH, CANVAS_HEIGHT), 2)

        # Draw tool buttons
        for tool, data in self.tool_buttons.items():
            rect = data['rect']
            # Highlight selected tool
            if tool == self.current_tool:
                pygame.draw.rect(screen, (150, 200, 255), rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)

            # Draw label
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
                pygame.draw.rect(screen, RED, rect, 3)

        # Draw instructions
        instructions = [
            "Click & Drag: Draw shapes | Select tool → Click color → Draw",
            "Square/Rhombus: Drag diagonally | Triangles: Drag to set base/height",
        ]
        for i, text in enumerate(instructions):
            label = font.render(text, True, BLACK)
            screen.blit(label, (400, CANVAS_HEIGHT + 25 + i * 25))

    def handle_ui_click(self, pos):
        """Handle clicks on UI elements"""
        # Check tool buttons
        for tool, data in self.tool_buttons.items():
            if data['rect'].collidepoint(pos):
                if tool == 'clear':
                    self.clear_canvas()
                else:
                    # Save current state before switching to eraser
                    if tool == 'eraser':
                        self.previous_tool = self.current_tool
                        self.previous_color = self.current_color
                        self.current_color = WHITE
                    self.current_tool = tool
                return True

        # Check color buttons
        for color_btn in self.color_buttons:
            if color_btn['rect'].collidepoint(pos):
                self.current_color = color_btn['color']
                # Restore previous tool when selecting a color (exit eraser mode)
                if self.current_tool == 'eraser':
                    self.current_tool = self.previous_tool
                    self.current_color = color_btn['color']
                return True

        return False

    def clear_canvas(self):
        """Clear the canvas"""
        self.canvas.fill(WHITE)

    def start_drawing(self, pos):
        """Start drawing at position"""
        self.start_pos = pos
        self.temp_surface = self.canvas.copy()

    def draw_shape_preview(self, current_pos):
        """Draw shape preview while dragging"""
        if self.start_pos is None:
            return

        # Restore canvas
        self.canvas.blit(self.temp_surface, (0, 0))

        # Calculate dimensions
        dx = current_pos[0] - self.start_pos[0]
        dy = current_pos[1] - self.start_pos[1]

        if self.current_tool == 'rectangle':
            # Standard rectangle
            x = min(self.start_pos[0], current_pos[0])
            y = min(self.start_pos[1], current_pos[1])
            width = abs(dx)
            height = abs(dy)
            pygame.draw.rect(self.canvas, self.current_color, (x, y, width, height))
            pygame.draw.rect(self.canvas, BLACK, (x, y, width, height), 1)

        elif self.current_tool == 'square':
            # Perfect square (equal width and height)
            size = max(abs(dx), abs(dy))
            # Determine direction
            x = self.start_pos[0] if dx >= 0 else self.start_pos[0] - size
            y = self.start_pos[1] if dy >= 0 else self.start_pos[1] - size
            pygame.draw.rect(self.canvas, self.current_color, (x, y, size, size))
            pygame.draw.rect(self.canvas, BLACK, (x, y, size, size), 1)

        elif self.current_tool == 'circle':
            # Circle based on distance
            radius = int(math.sqrt(dx**2 + dy**2))
            pygame.draw.circle(self.canvas, self.current_color, self.start_pos, radius)
            pygame.draw.circle(self.canvas, BLACK, self.start_pos, radius, 1)

        elif self.current_tool == 'right_triangle':
            # Right triangle with right angle at start_pos
            points = [
                self.start_pos,  # Right angle corner
                (current_pos[0], self.start_pos[1]),  # Horizontal point
                current_pos,  # End point
            ]
            pygame.draw.polygon(self.canvas, self.current_color, points)
            pygame.draw.polygon(self.canvas, BLACK, points, 1)

        elif self.current_tool == 'equilateral':
            # Equilateral triangle
            side_length = math.sqrt(dx**2 + dy**2)
            if side_length > 0:
                # Calculate third point
                # Angle at start is 0, so points form equilateral triangle
                angle = math.atan2(dy, dx)
                p1 = self.start_pos
                p2 = current_pos
                # Third point: rotate p2 around p1 by 60 degrees
                angle60 = angle + math.pi / 3
                p3 = (
                    int(p1[0] + side_length * math.cos(angle60)),
                    int(p1[1] + side_length * math.sin(angle60))
                )
                points = [p1, p2, p3]
                pygame.draw.polygon(self.canvas, self.current_color, points)
                pygame.draw.polygon(self.canvas, BLACK, points, 1)

        elif self.current_tool == 'rhombus':
            # Rhombus (diamond) - all sides equal
            # Center is midpoint, corners are at start, current, and perpendicular points
            center_x = (self.start_pos[0] + current_pos[0]) / 2
            center_y = (self.start_pos[1] + current_pos[1]) / 2

            # Calculate diagonal vectors
            diag1_x = current_pos[0] - self.start_pos[0]
            diag1_y = current_pos[1] - self.start_pos[1]

            # Second diagonal is perpendicular (rotate 90 degrees)
            diag2_x = -diag1_y
            diag2_y = diag1_x

            # Four corners of rhombus
            points = [
                self.start_pos,  # Corner 1
                (int(center_x + diag2_x / 2), int(center_y + diag2_y / 2)),  # Corner 2
                current_pos,  # Corner 3
                (int(center_x - diag2_x / 2), int(center_y - diag2_y / 2)),  # Corner 4
            ]
            pygame.draw.polygon(self.canvas, self.current_color, points)
            pygame.draw.polygon(self.canvas, BLACK, points, 1)

    def end_drawing(self):
        """Finish drawing"""
        self.start_pos = None
        self.temp_surface = None

    def draw_brush(self, pos):
        """Draw with brush/eraser"""
        size = self.brush_size * 3 if self.current_tool == 'eraser' else self.brush_size
        pygame.draw.circle(self.canvas, self.current_color, pos, size)

    def run(self):
        """Main loop"""
        drawing = False

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                # Mouse down
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = event.pos

                        # Check UI click
                        if pos[1] >= CANVAS_HEIGHT:
                            self.handle_ui_click(pos)
                            continue

                        # Start drawing
                        drawing = True
                        if self.current_tool in ['rectangle', 'square', 'circle',
                                                  'right_triangle', 'equilateral', 'rhombus']:
                            self.start_drawing(pos)
                        elif self.current_tool in ['brush', 'eraser']:
                            self.draw_brush(pos)

                # Mouse motion
                if event.type == pygame.MOUSEMOTION:
                    if drawing:
                        pos = event.pos
                        if pos[1] < CANVAS_HEIGHT:
                            if self.current_tool in ['rectangle', 'square', 'circle',
                                                      'right_triangle', 'equilateral', 'rhombus']:
                                self.draw_shape_preview(pos)
                            elif self.current_tool in ['brush', 'eraser']:
                                self.draw_brush(pos)

                # Mouse up
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        drawing = False
                        if self.current_tool in ['rectangle', 'square', 'circle',
                                                  'right_triangle', 'equilateral', 'rhombus']:
                            self.end_drawing()

            # Draw everything
            screen.blit(self.canvas, (0, 0))
            self.draw_ui(screen)

            # Draw current tool info
            tool_text = font.render(f"Tool: {self.current_tool.replace('_', ' ').title()}", True, BLACK)
            screen.blit(tool_text, (SCREEN_WIDTH - 200, CANVAS_HEIGHT + 5))

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
