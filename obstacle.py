import random
import pygame
# import settings  # Removed direct import, settings will be passed


class Obstacle(pygame.sprite.Sprite):
    BASE_WIDTH = (
        50  # Kept as class attributes for local reference, can be moved to settings
    )
    BASE_HEIGHT = (
        20  # Kept as class attributes for local reference, can be moved to settings
    )
    # BASE_COLOR will now be an instance attribute based on settings

    def __init__(
        self,
        speed,
        generation=1,
        can_split=False,
        num_splits=2,
        position=None,
        game_settings=None,  # Accept game_settings
    ):
        super().__init__()
        # Initialize settings with fallback if not provided
        if game_settings is None:
            import settings as default_settings # Fallback import
            self.settings = default_settings
        else:
            self.settings = game_settings  # Store settings

        self.speed = speed
        self.generation = generation
        self.can_split = can_split if self.generation > 0 else False
        self.num_splits = num_splits

        if self.generation == 1:
            self.width = self.BASE_WIDTH
            self.height = self.BASE_HEIGHT
            self.color = self.settings.NEON_RED # Use settings color
            self.effective_speed = self.speed
        elif self.generation == 0:
            self.width = int(self.BASE_WIDTH * 0.55)
            self.height = int(self.BASE_HEIGHT * 0.7)
            # Derive color from the base settings color, assuming NEON_RED is the base
            base_red = self.settings.NEON_RED
            self.color = (
                max(0, base_red[0] - 70),
                base_red[1],
                base_red[2],
            )
            self.effective_speed = self.speed * 1.2
        else:  # Fallback, though generation 1 and 0 are the primary types
            self.width = self.BASE_WIDTH
            self.height = self.BASE_HEIGHT
            self.color = self.settings.NEON_RED # Use settings color
            self.effective_speed = self.speed

        self.image = pygame.Surface([self.width, self.height], pygame.SRCALPHA)

        glow_color_val = 60
        if self.can_split and self.generation == 1:
            glow_color_val = 100

        glow_color = (
            min(255, self.color[0] + glow_color_val),
            min(255, self.color[1] + glow_color_val),
            min(255, self.color[2] + glow_color_val),
        )

        inset = min(2, self.width // 10, self.height // 10)
        pygame.draw.rect(
            self.image,
            glow_color,
            (0, 0, self.width, self.height),
            border_radius=max(1, inset * 3),
        )
        pygame.draw.rect(
            self.image,
            self.color,
            (inset, inset, self.width - inset * 2, self.height - inset * 2),
            border_radius=max(1, inset * 2),
        )

        self.rect = self.image.get_rect()

        if position:
            self.rect.center = position
        else:
            self.rect.x = random.randint(
                0, self.settings.WIDTH - self.width
            )  # Use settings.WIDTH
            self.rect.y = -self.height

    def update(self, speed_multiplier=1):
        self.rect.y += self.effective_speed * speed_multiplier
        if self.rect.top > self.settings.HEIGHT:  # Use settings.HEIGHT
            self.kill()

    def get_split_pieces(self):
        if not self.can_split or self.generation <= 0 or self.num_splits != 2:
            return []

        new_pieces = []

        temp_small_piece = Obstacle(
            speed=self.speed, generation=0, can_split=False, game_settings=self.settings
        )  # Pass settings
        small_piece_width = temp_small_piece.width
        small_piece_height = temp_small_piece.height

        pos1_x = self.rect.centerx - (small_piece_width / 2) - 1
        pos1_y = self.rect.centery

        pos2_x = self.rect.centerx + (small_piece_width / 2) + 1
        pos2_y = self.rect.centery

        piece1 = Obstacle(
            speed=self.speed,
            generation=0,
            can_split=False,
            position=(pos1_x, pos1_y),
            game_settings=self.settings,  # Pass settings
        )
        new_pieces.append(piece1)

        piece2 = Obstacle(
            speed=self.speed,
            generation=0,
            can_split=False,
            position=(pos2_x, pos2_y),
            game_settings=self.settings,  # Pass settings
        )
        new_pieces.append(piece2)

        return new_pieces

    def draw(self, screen):
        screen.blit(self.image, self.rect)