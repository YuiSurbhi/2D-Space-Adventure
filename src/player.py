import pygame

class Player:
    def __init__(self, x, y):
        # Load the player's spaceship image
        self.image = pygame.image.load("assets/images/spaceship.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5  # Set the speed of the spaceship

    def handle_keys(self):
        # Get key states
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def update(self):
        # Update the player's position
        self.handle_keys()

    def draw(self, screen):
        # Draw the player on the screen
        screen.blit(self.image, self.rect)
