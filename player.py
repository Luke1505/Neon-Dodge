import pygame
import settings  # Import settings


# Inherit from pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self, game_settings=settings):  # Accept game_settings
        super().__init__()
        self.settings = game_settings  # Store settings
        self.original_width = 60
        self.original_height = 20
        self.width = self.original_width
        self.height = self.original_height

        self.color = settings.PLAYER_COLOR  # Use settings color

        self.image = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        self.rect.x = 300
        self.rect.y = 740
        self.speed = self.settings.PLAYER_SPEED  # Use settings for speed
        self.update_visuals()  # Call once at init

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

        self.x = self.rect.x
        self.y = self.rect.y

        self.rect.left = max(2.5, self.rect.left)
        self.rect.right = min(
            self.settings.WIDTH - 2.5, self.rect.right
        )  # Use settings.WIDTH
        self.rect.top = max(
            self.settings.HEIGHT // 2, self.rect.top
        )  # Use settings.HEIGHT
        self.rect.bottom = min(
            self.settings.HEIGHT - 5, self.rect.bottom
        )  # Use settings.HEIGHT

    def update_visuals(self):
        old_center = self.rect.center
        self.image = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        pygame.draw.rect(
            self.image, self.color, (0, 0, self.width, self.height), border_radius=6
        )
        self.rect = self.image.get_rect(center=old_center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=6)
