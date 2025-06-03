import pygame
import random
import math  # Added for math.pi, math.cos, math.sin


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, base_obstacle_color, explosion_intensity=1.0):
        """
        Creates a particle for an explosion effect.
        :param x: Starting x position (center of explosion)
        :param y: Starting y position (center of explosion)
        :param base_obstacle_color: The primary color of the obstacle that exploded.
        :param explosion_intensity: Multiplier for particle speed
        """
        super().__init__()

        self.x = x
        self.y = y
        self.base_color = base_obstacle_color

        self.size = random.randint(2, 5)

        r_offset = random.randint(0, 50)
        g_offset = random.randint(-30, 30)
        b_offset = random.randint(-50, 0)

        r = max(0, min(255, self.base_color[0] + r_offset))
        g = max(0, min(255, self.base_color[1] + g_offset + random.randint(0, 40)))
        b = max(0, min(255, self.base_color[2] + b_offset))
        self.color = (r, g, b)

        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(self.x, self.y))

        angle = random.uniform(0, 2 * math.pi)
        speed_magnitude = random.uniform(1, 3.5) * explosion_intensity
        self.vx = math.cos(angle) * speed_magnitude
        self.vy = math.sin(angle) * speed_magnitude

        self.lifespan = random.randint(20, 50)  # Increased lifespan slightly
        self.current_lifespan = 0

        self.gravity = 0.05
        self.friction = 0.99

    def update(self):
        self.vx *= self.friction
        self.vy *= self.friction
        self.vy += self.gravity

        self.rect.x += self.vx
        self.rect.y += self.vy

        self.current_lifespan += 1
        if self.current_lifespan > self.lifespan:
            self.kill()
