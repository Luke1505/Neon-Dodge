import pygame
import random

POWERUP_TYPES = ["shield", "slowmo", "bomb","shrink"]
POWERUP_COLORS = {
    "shield": (0, 200, 255),
    "slowmo": (255, 255, 0),
    "bomb": (255, 80, 80),
    "shrink": (255, 0, 255),
}

class PowerUp:
    def __init__(self):
        self.type = random.choice(POWERUP_TYPES)
        self.rect = pygame.Rect(random.randint(50, 750), -30, 30, 30)
        self.color = POWERUP_COLORS[self.type]
        self.speed = 4
        self.icon_font = pygame.font.SysFont("consolas", 20)
        self.label = self.icon_font.render(self.type[0].upper(), True, (0, 0, 0))

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)
        screen.blit(
            self.label,
            (self.rect.centerx - self.label.get_width() // 2,
             self.rect.centery - self.label.get_height() // 2)
        )
