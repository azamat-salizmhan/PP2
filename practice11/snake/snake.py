import pygame
import random
import sys
import math

# Initialize pygame
pygame.init()

# Screen and grid settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
UI_HEIGHT = 60  # Extra space for UI

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
DARK_GRAY = (64, 64, 64)
ORANGE = (255, 165, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + UI_HEIGHT))
pygame.display.set_caption("Snake Game - Practice 11")
clock = pygame.time.Clock()

# Font setup
font = pygame.font.SysFont("Arial", 20)
font_large = pygame.font.SysFont("Arial", 50)
small_font = pygame.font.SysFont("Arial", 14)


class Snake:
    """Snake class with movement and collision handling"""

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset snake to starting position"""
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2

        # Initial body: 3 segments
        self.body = [
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y)
        ]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.grow = False

    def change_direction(self, new_direction):
        """Change direction if not opposite"""
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.next_direction = new_direction

    def move(self):
        """Move snake forward"""
        self.direction = self.next_direction

        # New head position
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Insert new head
        self.body.insert(0, new_head)

        # Remove tail unless growing
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def grow_snake(self, amount=1):
        """Mark snake to grow by amount"""
        self.grow = True
        # For simplicity, grow by 1 segment per food

    def draw(self, screen):
        """Draw snake on screen"""
        for i, segment in enumerate(self.body):
            color = DARK_GREEN if i == 0 else GREEN
            rect = pygame.Rect(
                segment[0] * GRID_SIZE,
                segment[1] * GRID_SIZE + UI_HEIGHT,
                GRID_SIZE - 2,
                GRID_SIZE - 2
            )
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

    def check_self_collision(self):
        """Check if head collides with body"""
        head = self.body[0]
        return head in self.body[1:]

    def check_wall_collision(self):
        """Check if snake hits wall"""
        head_x, head_y = self.body[0]
        return head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT


class Food:
    """
    Food with different weights and timer:
    - Small: 5 points, 10 seconds, Green
    - Medium: 10 points, 7 seconds, Yellow
    - Large: 15 points, 5 seconds, Red
    """

    FOOD_TYPES = [
        {'name': 'Small', 'weight': 5, 'color': GREEN, 'time': 10},
        {'name': 'Medium', 'weight': 10, 'color': YELLOW, 'time': 7},
        {'name': 'Large', 'weight': 15, 'color': RED, 'time': 5},
    ]

    def __init__(self):
        self.position = (0, 0)
        self.food_type = None
        self.spawn_time = 0
        self.lifetime = 0
        self.active = False

    def spawn(self, snake_body):
        """Generate new food with random type"""
        # Randomly select food type (equal chance)
        self.food_type = random.choice(self.FOOD_TYPES)

        # Place at random position not on snake
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            pos = (x, y)

            if pos not in snake_body:
                self.position = pos
                break

        # Set timer
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = self.food_type['time'] * 1000  # Convert to milliseconds
        self.active = True

    def is_expired(self):
        """Check if food timer expired"""
        if not self.active:
            return True
        current_time = pygame.time.get_ticks()
        return current_time - self.spawn_time > self.lifetime

    def get_time_remaining(self):
        """Get remaining time percentage (0.0 to 1.0)"""
        if not self.active:
            return 0
        elapsed = pygame.time.get_ticks() - self.spawn_time
        return max(0, 1 - (elapsed / self.lifetime))

    def draw(self, screen):
        """Draw food and timer bar"""
        if not self.active:
            return

        # Food rectangle
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE + UI_HEIGHT,
            GRID_SIZE - 2,
            GRID_SIZE - 2
        )
        pygame.draw.rect(screen, self.food_type['color'], rect)
        pygame.draw.rect(screen, BLACK, rect, 1)

        # Draw weight value on food
        text = small_font.render(str(self.food_type['weight']), True, BLACK)
        text_rect = text.get_rect(center=(rect.centerx, rect.centery))
        screen.blit(text, text_rect)

        # Draw timer bar above food
        time_pct = self.get_time_remaining()
        bar_width = GRID_SIZE - 2
        bar_height = 4
        bar_x = self.position[0] * GRID_SIZE
        bar_y = self.position[1] * GRID_SIZE + UI_HEIGHT - 6

        # Background bar
        pygame.draw.rect(screen, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))
        # Foreground bar (color changes from green to red)
        bar_color = (int(255 * (1 - time_pct)), int(255 * time_pct), 0)
        pygame.draw.rect(screen, bar_color, (bar_x, bar_y, bar_width * time_pct, bar_height))


def draw_ui(score, level, food_type, time_remaining):
    """Draw UI bar with score, level, and food info"""
    # UI background
    pygame.draw.rect(screen, GRAY, (0, 0, SCREEN_WIDTH, UI_HEIGHT))
    pygame.draw.line(screen, WHITE, (0, UI_HEIGHT), (SCREEN_WIDTH, UI_HEIGHT), 2)

    # Score and level
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, YELLOW)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 35))

    # Food info (if active)
    if food_type and time_remaining > 0:
        food_text = font.render(f"Food: {food_type['name']} ({food_type['weight']}pts)", True, food_type['color'])
        timer_text = font.render(f"Time: {int(time_remaining * food_type['time'])}s", True, WHITE)

        screen.blit(food_text, (200, 10))
        screen.blit(timer_text, (200, 35))


def draw_game_over(score, level):
    """Draw game over screen"""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT + UI_HEIGHT))
    overlay.fill(BLACK)
    overlay.set_alpha(200)
    screen.blit(overlay, (0, 0))

    texts = [
        ("GAME OVER", font_large, RED, -50),
        (f"Score: {score}", font, WHITE, 30),
        (f"Level: {level}", font, YELLOW, 60),
        ("Press R to restart", font, WHITE, 100),
    ]

    for text_str, text_font, color, y_offset in texts:
        text = text_font.render(text_str, True, color)
        x = SCREEN_WIDTH // 2 - text.get_width() // 2
        y = (SCREEN_HEIGHT + UI_HEIGHT) // 2 + y_offset
        screen.blit(text, (x, y))


def main():
    """Main game loop"""
    snake = Snake()
    food = Food()
    food.spawn(snake.body)

    # Game variables
    score = 0
    level = 1
    foods_eaten = 0
    game_over = False

    # Movement timing
    move_delay = 150
    last_move_time = pygame.time.get_ticks()

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Restart
                if event.key == pygame.K_r and game_over:
                    snake.reset()
                    food.spawn(snake.body)
                    score = 0
                    level = 1
                    foods_eaten = 0
                    move_delay = 150
                    game_over = False

                # Quit
                if event.key == pygame.K_ESCAPE:
                    running = False

                # Direction controls
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
            # Check if food expired
            if food.is_expired():
                food.spawn(snake.body)  # Respawn new food

            # Move snake
            current_time = pygame.time.get_ticks()
            if current_time - last_move_time > move_delay:
                snake.move()
                last_move_time = current_time

                # Check collisions
                if snake.check_wall_collision() or snake.check_self_collision():
                    game_over = True

                # Check food collision
                if snake.body[0] == food.position:
                    snake.grow_snake()
                    score += food.food_type['weight']  # Add food weight to score
                    foods_eaten += 1
                    food.spawn(snake.body)

                    # Level up every 4 foods
                    if foods_eaten % 4 == 0:
                        level += 1
                        move_delay = max(50, move_delay - 15)

        # Draw
        screen.fill(BLACK)

        # Game area background
        pygame.draw.rect(screen, DARK_GRAY, (0, UI_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT))

        # Grid lines
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, (60, 60, 60), (x, UI_HEIGHT), (x, SCREEN_HEIGHT + UI_HEIGHT))
        for y in range(UI_HEIGHT, SCREEN_HEIGHT + UI_HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, (60, 60, 60), (0, y), (SCREEN_WIDTH, y))

        # Draw game objects
        food.draw(screen)
        snake.draw(screen)

        # Draw UI
        time_remaining = food.get_time_remaining() if food.active else 0
        draw_ui(score, level, food.food_type if food.active else None, time_remaining)

        if game_over:
            draw_game_over(score, level)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
