import pygame
# import settings  # Removed direct import, settings will be passed


class Bullet(pygame.sprite.Sprite):
    def __init__(
        self, x, y, speed_y=None, radius=4, game_settings=None
    ):  # Accept game_settings
        super().__init__()
        # Initialize settings with fallback if not provided
        if game_settings is None:
            import settings as default_settings # Fallback import
            self.settings = default_settings
        else:
            self.settings = game_settings

        self.radius = radius
        # Use settings for default speed and color, or provided values
        self.speed_y = speed_y if speed_y is not None else self.settings.BULLET_SPEED
        self.color = self.settings.BULLET_COLOR

        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(x, y))


    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)