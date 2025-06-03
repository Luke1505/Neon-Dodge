import random
import pygame

from utils import HEIGHT, WIDTH

# Inherit from pygame.sprite.Sprite
class Obstacle(pygame.sprite.Sprite): 
    def __init__(self, speed):
        super().__init__() # Call the parent Sprite constructor
        self.x = random.randint(0, WIDTH - 50)
        self.y = -50  # Start above the screen
        self.width = 50
        self.height = 20
        self.color = (255, 0, 0)  # Red obstacle
        self.speed = speed  # Initial speed (can be adjusted)
        
        # Create an image and rect attribute, required for Sprites
        self.image = pygame.Surface([self.width, self.height], pygame.SRCALPHA) # Use SRCALPHA for potential transparency
        # Draw the visual representation onto self.image
        glow_color = (min(255, self.color[0] + 60), min(255, self.color[1] + 60), min(255, self.color[2] + 60))
        pygame.draw.rect(self.image, glow_color, (0, 0, self.width, self.height), border_radius=6) # Draw glow first
        pygame.draw.rect(self.image, self.color, (2, 2, self.width - 4, self.height - 4), border_radius=6) # Draw main rect inset for glow
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


    def update(self, speed_multiplier=1):
        self.rect.y += self.speed * speed_multiplier  # Apply the speed multiplier to movement
        if self.rect.top > HEIGHT:  # If the obstacle goes off the screen
            self.kill() # Remove from all sprite groups

    # The draw method is no longer strictly necessary if using group.draw(), 
    # but can be kept for individual drawing if needed.
    # Pygame's group.draw() will use self.image and self.rect.
    def draw(self, screen):
        # This manual draw is fine, but group.draw(screen) is more conventional for sprites
        glow = (min(255, self.color[0] + 60), min(255, self.color[1] + 60), min(255, self.color[2] + 60))
        # For glow effect, it's better to draw it onto self.image in __init__
        # or have a separate glow surface. For simplicity, we'll rely on the __init__ drawing.
        screen.blit(self.image, self.rect)


    def off_screen(self): # This method is now less critical if self.kill() is used in update
        return self.rect.top > HEIGHT