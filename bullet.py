import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_y=-10, color=(255, 255, 0), radius=4):
        super().__init__()
        self.radius = radius
        # Create a surface for the bullet
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_y = speed_y

    def update(self):
        self.rect.y += self.speed_y
        # Remove bullet if it goes off the top of the screen
        if self.rect.bottom < 0:
            self.kill()  # Removes sprite from all groups it's a member of

    def draw(
        self, screen
    ):  # Technically not needed if using sprite group's draw method
        screen.blit(self.image, self.rect)
