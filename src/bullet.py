import pygame

class Bullet:
    def __init__(self, x, y):
        # Load bullet image or create a simple rectangle bullet
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 255, 255))  # (R,G,B) color result in White bullet
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -7  # Bullet moves upwards

    def update(self):
        # Move bullet upwards
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
