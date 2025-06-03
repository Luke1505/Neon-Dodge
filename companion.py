import pygame
from bullet import Bullet
import settings  # Import settings


class Companion(pygame.sprite.Sprite):
    COMPANION_OFFSET_X = -45
    COMPANION_OFFSET_Y = 0
    FIRE_RATE_MS = 400

    def __init__(self, player_rect, game_settings=settings):  # Accept game_settings
        super().__init__()
        self.settings = game_settings  # Store settings
        self.width = 20
        self.height = 20
        self.image = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        self.color = self.settings.NEON_BLUE  # Use settings color
        pygame.draw.rect(
            self.image, self.color, (0, 0, self.width, self.height), border_radius=5
        )
        self.rect = self.image.get_rect()
        self.last_shot_time = pygame.time.get_ticks()
        self.update_position(player_rect)

    def update_position(self, player_rect):
        self.rect.centerx = player_rect.centerx + self.COMPANION_OFFSET_X
        self.rect.centery = player_rect.centery + self.COMPANION_OFFSET_Y

    def update(self, player_rect):
        self.update_position(player_rect)

        now = pygame.time.get_ticks()
        bullets_fired = []
        if now - self.last_shot_time > self.FIRE_RATE_MS:
            self.last_shot_time = now
            bullets_fired = self.shoot()
        return bullets_fired

    def shoot(self):
        bullet_start_x = self.rect.centerx
        bullet_start_y = self.rect.top
        new_bullet = Bullet(
            bullet_start_x,
            bullet_start_y,
            speed_y=self.settings.COMPANION_BULLET_SPEED,
            color=self.settings.COMPANION_BULLET_COLOR,
            radius=5,  # Use settings for speed and color
        )
        return [new_bullet]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
