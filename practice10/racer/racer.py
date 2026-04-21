import pygame
import random
import sys

# Initialize pygame first
pygame.init()

# Constants - Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_YELLOW = (200, 200, 0)

# Road settings
ROAD_WIDTH = 300
LANE_WIDTH = ROAD_WIDTH // 3
ROAD_LEFT = (SCREEN_WIDTH - ROAD_WIDTH) // 2
ROAD_RIGHT = ROAD_LEFT + ROAD_WIDTH

# Setup display - must be done BEFORE loading fonts
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Game")
clock = pygame.time.Clock()

# Font setup - AFTER display init
font = pygame.font.SysFont("Arial", 20)
font_large = pygame.font.SysFont("Arial", 50)


class Player(pygame.sprite.Sprite):
    

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 70))
        self.image.fill(GREEN)
        # Draw car details
        pygame.draw.rect(self.image, BLACK, (5, 10, 30, 15))  # Windshield
        pygame.draw.rect(self.image, BLACK, (0, 50, 10, 15))   # Left back wheel
        pygame.draw.rect(self.image, BLACK, (30, 50, 10, 15))  # Right back wheel
        pygame.draw.rect(self.image, BLACK, (0, 5, 10, 15))    # Left front wheel
        pygame.draw.rect(self.image, BLACK, (30, 5, 10, 15))   # Right front wheel

        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        self.speed = 5

    def move(self):
        """Handle player movement with keyboard input"""
        keys = pygame.key.get_pressed()

        # Move left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.move_ip(-self.speed, 0)
        # Move right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.move_ip(self.speed, 0)

        # Keep player within road boundaries
        if self.rect.left < ROAD_LEFT:
            self.rect.left = ROAD_LEFT
        if self.rect.right > ROAD_RIGHT:
            self.rect.right = ROAD_RIGHT


class Enemy(pygame.sprite.Sprite):
    """Enemy car class - moves down the screen"""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 70))
        self.image.fill(RED)
        # Draw car details
        pygame.draw.rect(self.image, BLACK, (5, 45, 30, 15))
        pygame.draw.rect(self.image, BLACK, (0, 5, 10, 15))
        pygame.draw.rect(self.image, BLACK, (30, 5, 10, 15))
        pygame.draw.rect(self.image, BLACK, (0, 50, 10, 15))
        pygame.draw.rect(self.image, BLACK, (30, 50, 10, 15))

        self.rect = self.image.get_rect()
        # Random lane position
        lane = random.randint(0, 2)
        self.rect.centerx = ROAD_LEFT + LANE_WIDTH // 2 + lane * LANE_WIDTH
        self.rect.top = random.randint(-300, -100)
        self.speed = random.randint(3, 6)

    def move(self):
        """Move enemy down the screen"""
        self.rect.move_ip(0, self.speed)

        # Reset enemy when it goes off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.respawn()

    def respawn(self):
        """Respawn enemy at top with new random properties"""
        lane = random.randint(0, 2)
        self.rect.centerx = ROAD_LEFT + LANE_WIDTH // 2 + lane * LANE_WIDTH
        self.rect.top = random.randint(-300, -100)
        self.speed = random.randint(3, 6)


class Coin(pygame.sprite.Sprite):
    """Coin class - player collects these for points"""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        # Draw yellow circle for coin
        pygame.draw.circle(self.image, YELLOW, (15, 15), 12)
        pygame.draw.circle(self.image, DARK_YELLOW, (15, 15), 12, 2)
        # Draw a simple C shape
        pygame.draw.arc(self.image, BLACK, (8, 8, 14, 14), 0.8, 5.5, 2)

        self.rect = self.image.get_rect()
        self.respawn()

    def respawn(self):
        """Place coin at random position on road"""
        lane = random.randint(0, 2)
        self.rect.centerx = ROAD_LEFT + LANE_WIDTH // 2 + lane * LANE_WIDTH
        self.rect.top = random.randint(-500, -50)
        self.speed = 3

    def move(self):
        """Move coin down the screen"""
        self.rect.move_ip(0, self.speed)

        # Reset coin when it goes off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.respawn()


def draw_road():
    """Draw the road with lane markings"""
    # Fill background
    screen.fill((34, 139, 34))  # Grass green

    # Draw road
    pygame.draw.rect(screen, GRAY, (ROAD_LEFT, 0, ROAD_WIDTH, SCREEN_HEIGHT))

    # Draw lane dividers
    for y in range(0, SCREEN_HEIGHT, 40):
        pygame.draw.rect(screen, WHITE, (ROAD_LEFT + LANE_WIDTH - 2, y, 4, 25))
        pygame.draw.rect(screen, WHITE, (ROAD_LEFT + 2 * LANE_WIDTH - 2, y, 4, 25))

    # Draw road borders
    pygame.draw.line(screen, WHITE, (ROAD_LEFT, 0), (ROAD_LEFT, SCREEN_HEIGHT), 4)
    pygame.draw.line(screen, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, SCREEN_HEIGHT), 4)


def show_game_over(screen, score, coins_collected):
    """Display game over screen"""
    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill(WHITE)
    overlay.set_alpha(200)
    screen.blit(overlay, (0, 0))

    # Game over text
    game_over_text = font_large.render("GAME OVER", True, RED)
    score_text = font.render(f"Score: {score}", True, BLACK)
    coins_text = font.render(f"Coins: {coins_collected}", True, YELLOW)
    restart_text = font.render("Press R to restart", True, BLACK)

    # Center text
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
    screen.blit(coins_text, (SCREEN_WIDTH // 2 - coins_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))


def main():
    """Main game function"""
    # Create player
    player = Player()

    # Create enemies
    enemies = pygame.sprite.Group()
    for i in range(3):
        enemy = Enemy()
        # Stagger enemy positions
        enemy.rect.top = random.randint(-600, -100) - i * 150
        enemies.add(enemy)

    # Create coins
    coins = pygame.sprite.Group()
    for i in range(2):
        coin = Coin()
        coin.rect.top = random.randint(-800, -200) - i * 300
        coins.add(coin)

    # All sprites group
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(enemies)
    all_sprites.add(coins)

    # Game variables
    score = 0
    coins_collected = 0
    game_over = False

    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Restart game on 'R' key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    # Reset game
                    game_over = False
                    score = 0
                    coins_collected = 0
                    player.rect.centerx = SCREEN_WIDTH // 2

                    # Reset enemies
                    for enemy in enemies:
                        enemy.respawn()

                    # Reset coins
                    for coin in coins:
                        coin.respawn()

                # Quit on ESC key
                if event.key == pygame.K_ESCAPE:
                    running = False

        if not game_over:
            # Update game objects
            player.move()

            for enemy in enemies:
                enemy.move()

                # Check collision with player
                if player.rect.colliderect(enemy.rect):
                    game_over = True

            for coin in coins:
                coin.move()

                # Check collision with player (coin collection)
                if player.rect.colliderect(coin.rect):
                    coins_collected += 1
                    coin.respawn()

            # Increase score over time
            score += 1

        # Draw everything
        draw_road()

        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)

        # Display score and coins in top right corner
        score_text = font.render(f"Score: {score}", True, WHITE)
        coins_text = font.render(f"Coins: {coins_collected}", True, YELLOW)

        screen.blit(score_text, (SCREEN_WIDTH - 140, 10))
        screen.blit(coins_text, (SCREEN_WIDTH - 140, 40))

        # Show game over screen if game is over
        if game_over:
            show_game_over(screen, score, coins_collected)

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
