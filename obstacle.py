import random
import pygame
from utils import HEIGHT, WIDTH  #


class Obstacle(pygame.sprite.Sprite):
    BASE_WIDTH = 50
    BASE_HEIGHT = 20
    BASE_COLOR = (255, 0, 0)

    def __init__(
        self, speed, generation=1, can_split=False, num_splits=2, position=None
    ):
        super().__init__()

        self.speed = speed
        self.generation = generation
        self.can_split = can_split if self.generation > 0 else False
        self.num_splits = (
            num_splits  # For this specific request, we'll focus on num_splits = 2
        )

        if self.generation == 1:
            self.width = self.BASE_WIDTH
            self.height = self.BASE_HEIGHT
            self.color = self.BASE_COLOR
            self.effective_speed = self.speed
        elif self.generation == 0:
            self.width = int(
                self.BASE_WIDTH * 0.55
            )  # Make them slightly more than half for a small overlap/gap control
            self.height = int(
                self.BASE_HEIGHT * 0.7
            )  # Can also adjust height if desired
            self.color = (
                max(0, self.BASE_COLOR[0] - 70),
                self.BASE_COLOR[1],
                self.BASE_COLOR[2],
            )
            self.effective_speed = self.speed * 1.2
        else:
            self.width = self.BASE_WIDTH
            self.height = self.BASE_HEIGHT
            self.color = self.BASE_COLOR
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
            self.rect.x = random.randint(0, WIDTH - self.width)
            self.rect.y = -self.height

    def update(self, speed_multiplier=1):
        self.rect.y += self.effective_speed * speed_multiplier
        if self.rect.top > HEIGHT:
            self.kill()

    def get_split_pieces(self):
        if (
            not self.can_split or self.generation <= 0 or self.num_splits != 2
        ):  # Ensure it's set to split into 2 for this logic
            return []

        new_pieces = []

        # Create two new obstacles of generation 0
        # They will be smaller. We need their width to place them side-by-side.
        # Instantiate a temporary small piece to get its width for calculation
        temp_small_piece = Obstacle(speed=self.speed, generation=0, can_split=False)
        small_piece_width = temp_small_piece.width
        small_piece_height = (
            temp_small_piece.height
        )  # Though not strictly needed for horizontal placement

        # Position them side-by-side, centered around the parent's center x
        # Offset slightly so they don't perfectly overlap if width isn't exact half.
        # A small gap or slight overlap might occur based on rounding.

        # Position 1: To the left of the center
        pos1_x = self.rect.centerx - (small_piece_width / 2) - 1  # -1 for a tiny gap
        pos1_y = self.rect.centery

        # Position 2: To the right of the center
        pos2_x = self.rect.centerx + (small_piece_width / 2) + 1  # +1 for a tiny gap
        pos2_y = self.rect.centery

        piece1 = Obstacle(
            speed=self.speed, generation=0, can_split=False, position=(pos1_x, pos1_y)
        )
        new_pieces.append(piece1)

        piece2 = Obstacle(
            speed=self.speed, generation=0, can_split=False, position=(pos2_x, pos2_y)
        )
        new_pieces.append(piece2)

        return new_pieces

    def draw(self, screen):
        screen.blit(self.image, self.rect)
