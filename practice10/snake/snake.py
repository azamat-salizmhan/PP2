import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants - Screen and grid settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GRID_SIZE = 20  # Size of each grid cell
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 50))  # Extra space for UI
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Font setup
font = pygame.font.SysFont("Verdana", 20)
font_large = pygame.font.SysFont("Verdana", 50)


class Snake:
    """Snake class - handles movement, drawing, and collision"""

    def __init__(self):
        # Initial snake position (center of screen)
        self.reset()

    def reset(self):
        """Reset snake to initial state"""
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2

        # Create initial snake body (3 segments)
        self.body = [
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y)
        ]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.grow = False  # Flag to grow snake

    def change_direction(self, new_direction):
        """Change direction if not opposite to current"""
        # Prevent 180-degree turns (can't go back on yourself)
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.next_direction = new_direction

    def move(self):
        """Move snake in current direction"""
        self.direction = self.next_direction

        # Calculate new head position
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Insert new head
        self.body.insert(0, new_head)

        # Remove tail if not growing
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def grow_snake(self):
        """Mark snake to grow on next move"""
        self.grow = True

    def draw(self, screen):
        """Draw snake on screen"""
        for i, segment in enumerate(self.body):
            color = DARK_GREEN if i == 0 else GREEN  # Head is darker
            rect = pygame.Rect(
                segment[0] * GRID_SIZE,
                segment[1] * GRID_SIZE + 50,  # Offset for UI bar
                GRID_SIZE - 2,
                GRID_SIZE - 2
            )
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)  # Border

    def check_self_collision(self):
        """Check if head collides with body"""
        head = self.body[0]
        # Check if head is in any part of body (except itself)
        return head in self.body[1:]

    def check_wall_collision(self):
        """Check if snake hits the wall"""
        head_x, head_y = self.body[0]
        # Check if head is outside grid boundaries
        if head_x < 0 or head_x >= GRID_WIDTH:
            return True
        if head_y < 0 or head_y >= GRID_HEIGHT:
            return True
        return False


class Food:
    """Food class - generates food at random positions"""

    def __init__(self):
        self.position = (0, 0)

    def generate_position(self, snake_body):
        """Generate random position not on snake or walls"""
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            pos = (x, y)

            # Make sure food doesn't spawn on snake
            if pos not in snake_body:
                self.position = pos
                break

    def draw(self, screen):
        """Draw food on screen"""
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE + 50,  # Offset for UI bar
            GRID_SIZE - 2,
            GRID_SIZE - 2
        )
        pygame.draw.rect(screen, RED, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)


def draw_ui(screen, score, level):
    """Draw UI bar with score and level"""
    # Draw UI background
    pygame.draw.rect(screen, GRAY, (0, 0, SCREEN_WIDTH, 50))
    pygame.draw.line(screen, WHITE, (0, 50), (SCREEN_WIDTH, 50), 2)

    # Draw score and level text
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, YELLOW)

    screen.blit(score_text, (10, 15))
    screen.blit(level_text, (200, 15))


def draw_game_over(screen, score, level):
    """Draw game over screen"""
    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT + 50))
    overlay.fill(BLACK)
    overlay.set_alpha(200)
    screen.blit(overlay, (0, 0))

    # Game over text
    game_over_text = font_large.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    level_text = font.render(f"Level Reached: {level}", True, YELLOW)
    restart_text = font.render("Press R to restart", True, WHITE)

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 50))
    screen.blit(level_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 80))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 120))


def main():
    """Main game function"""
    # Create game objects
    snake = Snake()
    food = Food()
    food.generate_position(snake.body)

    # Game variables
    score = 0
    level = 1
    foods_eaten = 0  # Count foods for level progression
    game_over = False

    # Movement timing
    move_delay = 150  # Milliseconds between moves (higher = slower)
    last_move_time = pygame.time.get_ticks()

    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Restart game
                if event.key == pygame.K_r and game_over:
                    snake.reset()
                    food.generate_position(snake.body)
                    score = 0
                    level = 1
                    foods_eaten = 0
                    move_delay = 150
                    game_over = False

                # Quit on ESC
                if event.key == pygame.K_ESCAPE:
                    running = False

                # Direction controls (only when game is running)
                if not game_over:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        snake.change_direction(UP)
                    if event.key in (pygame.K_DOWN, pygame.K_s):
                        snake.change_direction(DOWN)
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        snake.change_direction(LEFT)
                    if event.key in (pygame.K_RIGHT, pygame.K_d):
                        snake.change_direction(RIGHT)

        if not game_over:
            # Move snake based on timer
            current_time = pygame.time.get_ticks()
            if current_time - last_move_time > move_delay:
                snake.move()
                last_move_time = current_time

                # Check wall collision
                if snake.check_wall_collision():
                    game_over = True

                # Check self collision
                if snake.check_self_collision():
                    game_over = True

                # Check food collision
                if snake.body[0] == food.position:
                    snake.grow_snake()
                    food.generate_position(snake.body)
                    score += 10
                    foods_eaten += 1

                    # Level progression every 4 foods
                    if foods_eaten % 4 == 0:
                        level += 1
                        # Increase speed (decrease delay)
                        move_delay = max(50, move_delay - 15)

        # Draw everything
        screen.fill(BLACK)

        # Draw game area background
        pygame.draw.rect(screen, (40, 40, 40), (0, 50, SCREEN_WIDTH, SCREEN_HEIGHT))

        # Draw grid lines (optional, for visual aid)
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, (60, 60, 60), (x, 50), (x, SCREEN_HEIGHT + 50))
        for y in range(50, SCREEN_HEIGHT + 50, GRID_SIZE):
            pygame.draw.line(screen, (60, 60, 60), (0, y), (SCREEN_WIDTH, y))

        # Draw game objects
        food.draw(screen)
        snake.draw(screen)

        # Draw UI
        draw_ui(screen, score, level)

        # Draw game over screen
        if game_over:
            draw_game_over(screen, score, level)

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
