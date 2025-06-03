import pygame
import random
import settings  # Import settings

# Define weights for each power-up type
# Higher number means more common
POWERUP_WEIGHTS = {
    "shield": 5,
    "slowmo": 4,
    "shrink": 3,
    "turret": 2,
    "bomb": 3,
    "extralife": 1,
}

# Create the selection pool based on weights
_POWERUP_SELECTION_POOL = []
for type_name, weight in POWERUP_WEIGHTS.items():
    _POWERUP_SELECTION_POOL.extend([type_name] * weight)


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, game_settings=settings):  # Accept game_settings
        super().__init__()
        self.settings = game_settings  # Store settings

        # Select type from the weighted pool
        if not _POWERUP_SELECTION_POOL:
            print("Warning: _POWERUP_SELECTION_POOL is empty! Defaulting to shield.")
            self.type = "shield"
        else:
            self.type = random.choice(_POWERUP_SELECTION_POOL)

        self.size = self.settings.POWERUP_SIZE  # Use settings for size
        self.color = settings.POWERUP_COLORS[self.type]
        self.speed = self.settings.POWERUP_SPEED  # Use settings for speed

        self.image = pygame.Surface([self.size, self.size], pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, self.color, (0, 0, self.size, self.size))

        self.icon_font = pygame.font.SysFont("consolas", 20)
        label_char = self.type[0].upper()
        if self.type == "extralife":
            label_char = "1UP"
        elif self.type == "turret":
            label_char = "T"

        label_surface = self.icon_font.render(label_char, True, (0, 0, 0))
        label_rect = label_surface.get_rect(center=(self.size // 2, self.size // 2))
        self.image.blit(label_surface, label_rect)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(
            50, self.settings.WIDTH - self.size - 50
        )  # Use settings.WIDTH
        self.rect.y = -self.size

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > self.settings.HEIGHT:  # Use settings.HEIGHT
            self.kill()
