import pygame
from utils import WIDTH, HEIGHT


# Inherit from pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # Call the parent Sprite constructor
        self.original_width = 60
        self.original_height = 20
        self.width = self.original_width
        self.height = self.original_height

        self.color = (0, 255, 180)

        # Create self.image and self.rect
        self.image = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        self.image.fill(self.color)  # Simple fill for now, can be more complex
        # If you want rounded corners on the image itself:
        # self.image.fill((0,0,0,0)) # Transparent background
        # pygame.draw.rect(self.image, self.color, (0,0,self.width,self.height), border_radius=6)

        self.rect = self.image.get_rect()

        self.rect.x = 300  # Start at the center
        self.rect.y = 740  # Near the bottom
        self.speed = 8

    def move(self, keys):
        dx = 0
        dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed

        self.rect.x += dx
        self.rect.y += dy

        # Update self.x and self.y if other parts of your code still use them, though rect.x/y is preferred
        self.x = self.rect.x
        self.y = self.rect.y

        # Boundary checks using self.rect
        self.rect.left = max(2.5, self.rect.left)
        self.rect.right = min(WIDTH - 2.5, self.rect.right)
        self.rect.top = max(HEIGHT // 2, self.rect.top)
        self.rect.bottom = min(HEIGHT - 5, self.rect.bottom)

    def update_visuals(self):
        """Recreates self.image if size or color changes. Call after modifying width/height/color."""
        # This is important if player size changes (e.g., shrink powerup)
        old_center = self.rect.center
        self.image = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        # self.image.fill(self.color) # Or draw rounded rect
        pygame.draw.rect(
            self.image, self.color, (0, 0, self.width, self.height), border_radius=6
        )
        self.rect = self.image.get_rect(center=old_center)

    # The draw method is no longer strictly necessary if using group.draw(),
    # but it's good to have a consistent way to draw the player.
    # Pygame's group.draw() will use self.image and self.rect.
    # However, your Game.render_game() currently calls player.draw() explicitly.
    def draw(self, screen):
        # The player's self.image should be updated by update_visuals() if size changes
        pygame.draw.rect(screen, self.color, self.rect, border_radius=6)
        # Or, if self.image is always up-to-date:
        # screen.blit(self.image, self.rect)

    # get_rect() is no longer needed as self.rect is the primary rectangle.
    # def get_rect(self):
    #     return pygame.Rect(self.x, self.y, self.width, self.height)
