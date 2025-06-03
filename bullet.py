import pygame
import settings # Import settings


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_y=settings.BULLET_SPEED, color=settings.BULLET_COLOR, radius=4): # Use settings for default speed and color
        super().__init__()
        self.radius = radius
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_y = speed_y

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)