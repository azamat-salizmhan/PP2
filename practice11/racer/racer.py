import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)  # Gold coin
GRAY = (128, 128, 128)
SILVER = (192, 192, 192)  # Silver coin
BRONZE = (205, 127, 50)  # Bronze coin
GOLD = (255, 215, 0)  # Gold coin

# Road settings
ROAD_WIDTH = 300
LANE_WIDTH = ROAD_WIDTH // 3
ROAD_LEFT = (SCREEN_WIDTH - ROAD_WIDTH) // 2
ROAD_RIGHT = ROAD_LEFT + ROAD_WIDTH

# Game settings
COINS_FOR_SPEED_BOOST = 5  # Every 5 coins, enemy speed increases
SPEED_BOOST_AMOUNT = 1  # Amount to increase speed by

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Game - Practice 11")
clock = pygame.time.Clock()

# Font setup
font = pygame.font.SysFont("Arial", 20)
font_large = pygame.font.SysFont("Arial", 50)
small_font = pygame.font.SysFont("Arial", 14)


class Player(pygame.sprite.Sprite):
    """Player car controlled by arrow keys"""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 70))
        self.image.fill(GREEN)
        # Car details
        pygame.draw.rect(self.image, BLACK, (5, 10, 30, 15))  # Windshield
        pygame.draw.rect(self.image, BLACK, (0, 50, 10, 15))   # Wheels
        pygame.draw.rect(self.image, BLACK, (30, 50, 10, 15))
        pygame.draw.rect(self.image, BLACK, (0, 5, 10, 15))
        pygame.draw.rect(self.image, BLACK, (30, 5, 10, 15))

        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        self.speed = 5

    def move(self):
        """Handle keyboard input for movement"""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.move_ip(-self.speed, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.move_ip(self.speed, 0)

        # Keep player on road
        if self.rect.left < ROAD_LEFT:
            self.rect.left = ROAD_LEFT
        if self.rect.right > ROAD_RIGHT:
            self.rect.right = ROAD_RIGHT


class Enemy(pygame.sprite.Sprite):
    """Enemy car that moves down screen"""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 70))
        self.image.fill(RED)
        # Car details
        pygame.draw.rect(self.image, BLACK, (5, 45, 30, 15))
        pygame.draw.rect(self.image, BLACK, (0, 5, 10, 15))
        pygame.draw.rect(self.image, BLACK, (30, 5, 10, 15))
        pygame.draw.rect(self.image, BLACK, (0, 50, 10, 15))
        pygame.draw.rect(self.image, BLACK, (30, 50, 10, 15))

        self.rect = self.image.get_rect()
        self.base_speed = random.randint(3, 6)
        self.speed = self.base_speed
        self.respawn()

    def move(self):
        """Move enemy down and reset if off screen"""
        self.rect.move_ip(0, self.speed)

        if self.rect.top > SCREEN_HEIGHT:
            self.respawn()

    def respawn(self):
        """Place enemy at top of screen"""
        lane = random.randint(0, 2)
        self.rect.centerx = ROAD_LEFT + LANE_WIDTH // 2 + lane * LANE_WIDTH
        self.rect.top = random.randint(-300, -100)

    def increase_speed(self, amount):
        """Increase enemy speed"""
        self.speed += amount


class Coin(pygame.sprite.Sprite):
    """
    Coin with different weights:
    - Bronze: weight 1 (low value, most common)
    - Silver: weight 2 (medium value)
    - Gold: weight 3 (high value, rare)
    """

    # Coin types with their properties
    COIN_TYPES = [
        {'name': 'Bronze', 'color': BRONZE, 'weight': 1, 'chance': 0.6},  # 60% chance
        {'name': 'Silver', 'color': SILVER, 'weight': 2, 'chance': 0.3},  # 30% chance
        {'name': 'Gold', 'color': GOLD, 'weight': 3, 'chance': 0.1},    # 10% chance
    ]

    def __init__(self):
        super().__init__()
        self.coin_type = self._random_coin_type()
        self.weight = self.coin_type['weight']

        # Create coin image based on type
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.coin_type['color'], (15, 15), 12)
        pygame.draw.circle(self.image, BLACK, (15, 15), 12, 2)

        # Draw weight number in center
        text = small_font.render(str(self.weight), True, BLACK)
        text_rect = text.get_rect(center=(15, 15))
        self.image.blit(text, text_rect)

        self.rect = self.image.get_rect()
        self.speed = 3
        self.respawn()

    def _random_coin_type(self):
        """Select random coin type based on probability"""
        rand = random.random()
        cumulative = 0
        for coin_type in self.COIN_TYPES:
            cumulative += coin_type['chance']
            if rand <= cumulative:
                return coin_type
        return self.COIN_TYPES[0]  # Default to bronze

    def respawn(self):
        """Place coin at random position on road"""
        lane = random.randint(0, 2)
        self.rect.centerx = ROAD_LEFT + LANE_WIDTH // 2 + lane * LANE_WIDTH
        self.rect.top = random.randint(-500, -50)

        # Randomize coin type again on respawn
        self.coin_type = self._random_coin_type()
        self.weight = self.coin_type['weight']

        # Recreate image with new type
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.coin_type['color'], (15, 15), 12)
        pygame.draw.circle(self.image, BLACK, (15, 15), 12, 2)

        # Draw weight number
        text = small_font.render(str(self.weight), True, BLACK)
        text_rect = text.get_rect(center=(15, 15))
        self.image.blit(text, text_rect)

    def move(self):
        """Move coin down screen"""
        self.rect.move_ip(0, self.speed)

        if self.rect.top > SCREEN_HEIGHT:
            self.respawn()


def draw_road():
    """Draw road with lane markings"""
    # Grass background
    screen.fill((34, 139, 34))

    # Road
    pygame.draw.rect(screen, GRAY, (ROAD_LEFT, 0, ROAD_WIDTH, SCREEN_HEIGHT))

    # Lane markings
    for y in range(0, SCREEN_HEIGHT, 40):
        pygame.draw.rect(screen, WHITE, (ROAD_LEFT + LANE_WIDTH - 2, y, 4, 25))
        pygame.draw.rect(screen, WHITE, (ROAD_LEFT + 2 * LANE_WIDTH - 2, y, 4, 25))

    # Road borders
    pygame.draw.line(screen, WHITE, (ROAD_LEFT, 0), (ROAD_LEFT, SCREEN_HEIGHT), 4)
    pygame.draw.line(screen, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, SCREEN_HEIGHT), 4)


def draw_ui(score, coins_collected, total_weight, enemy_speed):
    """Draw score, coins, and speed info"""
    # Score and coins
    score_text = font.render(f"Score: {score}", True, WHITE)
    coins_text = font.render(f"Coins: {coins_collected}", True, YELLOW)
    weight_text = font.render(f"Value: {total_weight}", True, GOLD)
    speed_text = font.render(f"Enemy Speed: {enemy_speed}", True, RED)

    screen.blit(score_text, (10, 10))
    screen.blit(coins_text, (10, 35))
    screen.blit(weight_text, (10, 60))
    screen.blit(speed_text, (10, 85))


def show_game_over(score, coins_collected, total_weight):
    """Display game over screen"""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill(WHITE)
    overlay.set_alpha(200)
    screen.blit(overlay, (0, 0))

    texts = [
        ("GAME OVER", font_large, RED, -100),
        (f"Score: {score}", font, BLACK, 20),
        (f"Coins: {coins_collected}", font, BLACK, 50),
        (f"Total Value: {total_weight}", font, BLACK, 80),
        ("Press R to restart", font, BLACK, 120),
    ]

    for text_str, text_font, color, y_offset in texts:
        text = text_font.render(text_str, True, color)
        x = SCREEN_WIDTH // 2 - text.get_width() // 2
        y = SCREEN_HEIGHT // 2 + y_offset
        screen.blit(text, (x, y))


def main():
    """Main game loop"""
    player = Player()

    # Create enemies
    enemies = pygame.sprite.Group()
    for i in range(3):
        enemy = Enemy()
        enemy.rect.top = random.randint(-600, -100) - i * 150
        enemies.add(enemy)

    # Create coins
    coins = pygame.sprite.Group()
    for i in range(2):
        coin = Coin()
        coin.rect.top = random.randint(-800, -200) - i * 300
        coins.add(coin)

    # All sprites
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(enemies)
    all_sprites.add(coins)

    # Game variables
    score = 0
    coins_collected = 0
    total_weight = 0  # Total value of collected coins
    game_over = False

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Restart game
                if event.key == pygame.K_r and game_over:
                    game_over = False
                    score = 0
                    coins_collected = 0
                    total_weight = 0
                    player.rect.centerx = SCREEN_WIDTH // 2

                    # Reset enemies to base speed
                    for enemy in enemies:
                        enemy.respawn()
                        enemy.speed = enemy.base_speed

                    # Reset coins
                    for coin in coins:
                        coin.respawn()

                # Quit
                if event.key == pygame.K_ESCAPE:
                    running = False

        if not game_over:
            # Update
            player.move()

            for enemy in enemies:
                enemy.move()

                # Check collision with player
                if player.rect.colliderect(enemy.rect):
                    game_over = True

            for coin in coins:
                coin.move()

                # Check coin collection
                if player.rect.colliderect(coin.rect):
                    coins_collected += 1
                    total_weight += coin.weight  # Add coin's weight to total
                    coin.respawn()

                    # Increase enemy speed every N coins
                    if coins_collected % COINS_FOR_SPEED_BOOST == 0:
                        for enemy in enemies:
                            enemy.increase_speed(SPEED_BOOST_AMOUNT)

            score += 1

        # Draw
        draw_road()

        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)

        # Get current enemy speed for display
        current_speed = 0
        for enemy in enemies:
            current_speed = int(enemy.speed)
            break

        draw_ui(score, coins_collected, total_weight, current_speed)

        if game_over:
            show_game_over(score, coins_collected, total_weight)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
