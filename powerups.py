import pygame
import random

# Define weights for each power-up type
# Higher number means more common
POWERUP_WEIGHTS = {
    "shield": 5,  # Common
    "slowmo": 4,  # Common
    "shrink": 3,  # Uncommon
    "turret": 2,  # Rare
    "bomb": 3,  # Very Rare (powerful, so should be rare)
    "extralife": 1,  # Very Rare (valuable)
}

# This list is still useful for defining all *possible* types and their colors,
# but the selection will happen from the weighted pool.
# POWERUP_TYPES_AVAILABLE = list(POWERUP_WEIGHTS.keys()) # Or keep your existing POWERUP_TYPES list if it's comprehensive

POWERUP_COLORS = {
    "shield": (0, 200, 255),  # Light Blue
    "slowmo": (255, 255, 0),  # Yellow
    "bomb": (255, 80, 80),  # Red
    "shrink": (255, 0, 255),  # Magenta
    "extralife": (0, 255, 0),  # Green
    "turret": (200, 200, 200),  # Light Grey / Silver
}

# Create the selection pool based on weights
_POWERUP_SELECTION_POOL = []
for type_name, weight in POWERUP_WEIGHTS.items():
    _POWERUP_SELECTION_POOL.extend([type_name] * weight)


class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Select type from the weighted pool
        if (
            not _POWERUP_SELECTION_POOL
        ):  # Should not happen if POWERUP_WEIGHTS is defined
            # Fallback to an arbitrary choice or raise an error
            # For now, let's pick shield if pool is empty, though this indicates a setup issue.
            print("Warning: _POWERUP_SELECTION_POOL is empty! Defaulting to shield.")
            self.type = "shield"
        else:
            self.type = random.choice(_POWERUP_SELECTION_POOL)

        self.size = 30
        self.color = POWERUP_COLORS[self.type]  # Get color for the chosen type
        self.speed = 4

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
            50, 750 - self.size
        )  # Assuming screen width around 800
        self.rect.y = -self.size

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > pygame.display.get_surface().get_height():
            self.kill()

    # def draw(self, screen): # Not strictly needed if using group.draw()
    #     screen.blit(self.image, self.rect)
