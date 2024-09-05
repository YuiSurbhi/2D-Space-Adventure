import pygame
import random

class PowerUp:
    def __init__(self, x, y, type):
        # Load the power-up image based on its type
        self.type = type
        self.image = pygame.image.load(f"assets/images/{type}_powerup.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2  # Speed at which the power-up moves down the screen

    def update(self):
        # Move the power-up down
        self.rect.y += self.speed

        # Reset power-up position if it goes off-screen
        if self.rect.top > pygame.display.get_surface().get_height():
            self.rect.x = random.randint(0, pygame.display.get_surface().get_width() - self.rect.width)
            self.rect.y = random.randint(-100, -40)  # Respawn above the screen

    def draw(self, screen):
        # Draw the power-up on the screen
        screen.blit(self.image, self.rect)

    def apply_effect(self, player):
        # Apply the effect of the power-up to the player
        if self.type == 'shield':
            player.activate_shield()
        elif self.type == 'double_fire':
            player.enable_double_fire()
        elif self.type == 'speed_boost':
            player.increase_speed()
        # Add more power-up types as needed
