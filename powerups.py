import pygame
import random

POWERUP_TYPES = ["shield", "slowmo", "bomb", "shrink", "extralife", "turret"]
POWERUP_COLORS = {
    "shield": (0, 200, 255),
    "slowmo": (255, 255, 0),
    "bomb": (255, 80, 80),
    "shrink": (255, 0, 255),
    "extralife": (0, 255, 0),
    "turret": (200, 200, 200),
}

# Inherit from pygame.sprite.Sprite
class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # Call the parent Sprite constructor
        self.type = random.choice(POWERUP_TYPES)
        self.size = 30 # Define size for the powerup
        self.color = POWERUP_COLORS[self.type]
        self.speed = 4
        
        self.image = pygame.Surface([self.size, self.size], pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, self.color, (0,0, self.size, self.size)) # Draw ellipse onto self.image
        
        self.icon_font = pygame.font.SysFont("consolas", 20)
        label_char = self.type[0].upper()
        if self.type == "extralife":
            label_char = "1UP"
        elif self.type == "turret":
            label_char = "T"
        
        label_surface = self.icon_font.render(label_char, True, (0,0,0))
        # Blit the label onto the self.image
        label_rect = label_surface.get_rect(center=(self.size // 2, self.size // 2))
        self.image.blit(label_surface, label_rect)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, 750 - self.size) # Use self.size for boundary
        self.rect.y = -self.size # Start above screen

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > pygame.display.get_surface().get_height(): # Check against screen height
            self.kill() # Remove if off-screen

    # draw method is not strictly needed if using group.draw()
    # def draw(self, screen):
    #     screen.blit(self.image, self.rect)