import random
import pygame

from utils import HEIGHT, WIDTH

class Obstacle:
    def __init__(self, speed):
        self.x = random.randint(0, WIDTH - 50)
        self.y = -50  # Start above the screen
        self.width = 50
        self.height = 20
        self.color = (255, 0, 0)  # Red obstacle
        self.speed = speed  # Initial speed (can be adjusted)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, speed_multiplier=1):
        self.y += self.speed * speed_multiplier  # Apply the speed multiplier to movement
        if self.y > HEIGHT:  # If the obstacle goes off the screen, reset its position
            self.y = -50
            self.x = random.randint(0, WIDTH - 50)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        glow = (min(255, self.color[0] + 60), min(255, self.color[1] + 60), min(255, self.color[2] + 60))
        pygame.draw.rect(screen, glow, (self.x-2, self.y-2, self.width+4, self.height+4), border_radius=6)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), border_radius=6)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def off_screen(self):
        return self.y > HEIGHT
