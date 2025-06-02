import pygame
from utils import WIDTH, HEIGHT 

class Player:
    def __init__(self):
        self.width = 60
        self.height = 20
        self.x = 300  # Start at the center
        self.y = 740  # Near the bottom
        self.speed = 8
        self.color = (0, 255, 180)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
        # limit x to the left and right edges of the screen and 5 pixels from the edges
        self.x = max(2.5, min(WIDTH - self.width - 2.5, self.x))
        # limt y to the bottom half of the screen and 20 pixels from the bottom
        self.y = max(HEIGHT // 2, min(HEIGHT - self.height - 5, self.y))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move_action(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

        # Clamp to screen bounds
        self.x = max(0, min(WIDTH - self.width, self.x))
        self.y = max(0, min(HEIGHT - self.height, self.y))

        self.rect.topleft = (self.x, self.y)

        # Clamp to allowed region
        self.x = max(2.5, min(WIDTH - self.width - 2.5, self.x))
        self.y = max(HEIGHT // 2, min(HEIGHT - self.height - 5, self.y))
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), border_radius=6)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)