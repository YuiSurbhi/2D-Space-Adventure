from .settings import *  # Import any settings/constants needed
from .player import Player
from .enemy import Enemy
from .bullet import Bullet
from .utils import check_collision
from .powerup import PowerUp

import pygame
import random

class Game:
    def __init__(self):
        # Initialize Pygame and set up the display
        pygame.init()  # Ensure Pygame is initialized
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Adventure")

        # Load the background image and sounds
        try:
            self.background = pygame.image.load("assets/images/space_background.png").convert()
        except pygame.error as e:
            print(f"Unable to load background image: {e}")
            self.background = pygame.Surface((WIDTH, HEIGHT))  # Create a plain surface as fallback
            self.background.fill((0, 0, 0))  # Fill with black as fallback

        # Load the font
        try:
            self.font = pygame.font.Font("assets/fonts/game_over.ttf", 36)  # Load custom font
        except FileNotFoundError:
            print("Custom font not found, using default font.")
            self.font = pygame.font.Font(None, 36)  # Use default font if custom not found

        # Load the sound effects
        self.laser_sound = pygame.mixer.Sound("assets/sounds/laser_shooting.wav")
        self.enemy_hit_sound = pygame.mixer.Sound("assets/sounds/enemy_hit.wav")
        self.game_over_sound = pygame.mixer.Sound("assets/sounds/game_over.wav")

        # Set sound volumes (optional)
        self.laser_sound.set_volume(0.5)
        self.enemy_hit_sound.set_volume(0.5)
        self.game_over_sound.set_volume(0.5)

        # Button settings
        self.play_button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 - 25, 150, 50)  # Button size and position
        self.play_button_color = (0, 200, 0)  # Green color for button

        # Game state attributes
        self.running = True
        self.clock = pygame.time.Clock()
        self.score = 0  # Initialize score to zero
        self.level = 1  # Initialize level to 1
        self.lives = 3  # Initialize player lives
        self.font = pygame.font.Font(None, 36)  # Default font, size 36

        # Game entities
        self.player = Player(WIDTH // 2, HEIGHT - 50)
        self.enemies = self.create_enemies()  # Create enemies based on the level
        self.bullets = []  # List to store bullets

    def create_enemies(self):
        # Create enemies based on the current level
        num_enemies = 5 + (self.level - 1) * 3  # Increase number of enemies with each level
        return [Enemy(random.randint(0, WIDTH - 40), random.randint(-100, -40)) for _ in range(num_enemies)]

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

    def show_main_menu(self):
        # Display the main menu with the Play button
        self.screen.fill((0, 0, 0))  # Fill the screen with black
        title_text = self.font.render("Space Explorer", True, (255, 255, 255))
        play_text = self.font.render("Play", True, (255, 255, 255))

        # Draw the title and the play button
        self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))
        pygame.draw.rect(self.screen, self.play_button_color, self.play_button_rect)  # Draw the play button
        self.screen.blit(play_text, (self.play_button_rect.x + 50, self.play_button_rect.y + 10))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Pressing the spacebar fires a bullet
                    self.fire_bullet()

    def fire_bullet(self):
        # Create a bullet at the player's current position
        bullet = Bullet(self.player.rect.centerx, self.player.rect.top)
        self.bullets.append(bullet)

        # Play the laser shooting sound
        self.laser_sound.play()

    def update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        # Update bullets and remove them if they go off-screen
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.rect.bottom < 0:  # If the bullet goes off the screen, remove it
                self.bullets.remove(bullet)

        # Check for collisions between bullets and enemies
        self.check_collisions()

        # Check if all enemies are destroyed to move to the next level
        if not self.enemies:
            self.next_level()

        # Check if game over conditions are met
        if self.lives <= 0:
            self.game_over()

    def check_collisions(self):
        # Check for collision between each bullet and each enemy
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.rect.colliderect(enemy.rect):  # Collision detected
                    self.bullets.remove(bullet)  # Remove the bullet
                    self.enemies.remove(enemy)  # Remove the enemy
                    self.score += 10  # Increment score by 10

                    # Play the enemy hit sound
                    self.enemy_hit_sound.play()
                    break  # Exit the inner loop to avoid checking this bullet further

        # Check if an enemy collides with the player
        for enemy in self.enemies:
            if enemy.rect.colliderect(self.player.rect):
                self.lives -= 1  # Decrease player's lives
                self.enemies.remove(enemy)  # Remove the enemy

    def next_level(self):
        self.level += 1  # Increment level
        self.enemies = self.create_enemies()  # Create new enemies for the next level

    def game_over(self):
        # Play the game over sound
        self.game_over_sound.play()

        self.running = False  # Stop the main loop
        self.display_game_over()

    def display_game_over(self):
        self.screen.fill((0, 0, 0))  # Fill the screen with black
        game_over_text = self.font.render("Game Over", True, (255, 0, 0))  # Red color
        score_text = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))  # White color
        self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

        # Wait for a key press to restart or quit
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Press 'R' to restart
                        self.__init__()  # Restart the game
                        self.run()  # Restart the game loop
                        waiting = False
                    elif event.key == pygame.K_q:  # Press 'Q' to quit
                        waiting = False
                        self.running = False

    def draw(self):
        # Draw the background first
        self.screen.blit(self.background, (0, 0))

        # Draw the player, enemies, and bullets on top of the background
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)

        # Render and display the score, level, and lives
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        level_text = self.font.render(f"Level: {self.level}", True, (255, 255, 255))
        lives_text = self.font.render(f"Lives: {self.lives}", True, (255, 255, 255))

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 40))
        self.screen.blit(lives_text, (10, 70))

        pygame.display.flip()

