import pygame
import random

class Enemy:
    def __init__(self, x, y):
        # Load the enemy image
        self.image = pygame.image.load("assets/images/enemy1.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = random.randint(2, 5)  # Random speed for enemies

    def update(self):
        # Move the enemy down
        self.rect.y += self.speed

        # If the enemy goes off-screen, reset to the top
        if self.rect.top > pygame.display.get_surface().get_height():
            self.rect.x = random.randint(0, pygame.display.get_surface().get_width() - self.rect.width)
            self.rect.y = random.randint(-100, -40)  # Respawn above the screen

    def draw(self, screen):
        screen.blit(self.image, self.rect)

