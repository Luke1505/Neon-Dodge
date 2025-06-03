import pygame
from bullet import Bullet  # Import the Bullet class


class Companion(pygame.sprite.Sprite):
    COMPANION_OFFSET_X = -45  # Position relative to player (to the left)
    COMPANION_OFFSET_Y = 0  # Slightly below player's top
    FIRE_RATE_MS = 400  # Milliseconds between shots (faster rate)

    # Duration will be handled by a timer in the Game class via powerup pickup

    def __init__(
        self, player_rect
    ):  # Pass the whole player rect for better positioning
        super().__init__()
        self.width = 20
        self.height = 20
        self.image = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        self.color = (100, 150, 255)  # A distinct blue
        pygame.draw.rect(
            self.image, self.color, (0, 0, self.width, self.height), border_radius=5
        )
        self.rect = self.image.get_rect()
        self.last_shot_time = pygame.time.get_ticks()  # Initialize last shot time
        self.update_position(player_rect)  # Initial position

    def update_position(self, player_rect):
        # Stays to the defined offset of the player
        self.rect.centerx = player_rect.centerx + self.COMPANION_OFFSET_X
        self.rect.centery = player_rect.centery + self.COMPANION_OFFSET_Y

    def update(self, player_rect):  # Pass player_rect for continuous position updates
        self.update_position(player_rect)

        # Shooting logic
        now = pygame.time.get_ticks()
        bullets_fired = []
        if now - self.last_shot_time > self.FIRE_RATE_MS:
            self.last_shot_time = now
            bullets_fired = self.shoot()
        return bullets_fired  # Return a list of bullets (can be empty)

    def shoot(self):
        # Shoots straight up from companion's position
        bullet_start_x = self.rect.centerx
        bullet_start_y = self.rect.top
        # Companion bullets are a different color and slightly faster
        new_bullet = Bullet(
            bullet_start_x, bullet_start_y, speed_y=-15, color=(180, 180, 255), radius=5
        )
        return [new_bullet]

    def draw(
        self, screen
    ):  # Technically not needed if using sprite group's draw method for a single companion
        screen.blit(self.image, self.rect)
