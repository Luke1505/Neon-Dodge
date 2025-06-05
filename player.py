import pygame
# import settings  # Removed direct import, settings will be passed


# Inherit from pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self, game_settings=None):  # Accept game_settings
        super().__init__()
        # Initialize settings with fallback if not provided
        if game_settings is None:
            import settings as default_settings # Fallback import
            self.settings = default_settings
        else:
            self.settings = game_settings  # Store settings

        self.original_width = 60
        self.original_height = 20
        self.width = self.original_width
        self.height = self.original_height

        self.color = self.settings.PLAYER_COLOR  # Use settings color

        self.image = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        self.rect.x = 300
        self.rect.y = 740
        self.speed = self.settings.PLAYER_SPEED  # Use settings for speed
        self.update_visuals()  # Call once at init

    def move(self, keys, touch_pos=None): # Added touch_pos parameter
        dx = 0
        dy = 0

        if touch_pos:
            # --- Touch Input Logic ---
            # Move towards the touch position
            # Adjust sensitivity or dead zone as needed
            dead_zone = 10 # pixels, player won't move if touch is too close to its center

            # Horizontal movement
            if abs(touch_pos[0] * self.settings.WIDTH - self.rect.centerx) > dead_zone:
                if touch_pos[0] * self.settings.WIDTH < self.rect.centerx :
                    dx = -self.speed
                elif touch_pos[0] * self.settings.WIDTH > self.rect.centerx:
                    dx = self.speed

            # Vertical movement
            # Ensure player stays in the designated play area (e.g., bottom half of the screen)
            min_y_touch_control = self.settings.HEIGHT // 2 # Example: Player can only be controlled by touch in bottom half
            if touch_pos[1] * self.settings.HEIGHT > min_y_touch_control and \
               abs(touch_pos[1] * self.settings.HEIGHT - self.rect.centery) > dead_zone:
                if touch_pos[1] * self.settings.HEIGHT < self.rect.centery:
                    dy = -self.speed
                elif touch_pos[1] * self.settings.HEIGHT > self.rect.centery:
                    dy = self.speed
            # --- End Touch Input Logic ---
        else:
            # --- Keyboard Input Logic ---
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx = -self.speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = self.speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                dy = -self.speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy = self.speed
            # --- End Keyboard Input Logic ---


        self.rect.x += dx
        self.rect.y += dy

        # self.x = self.rect.x # These seem redundant as rect.x/y are the primary position
        # self.y = self.rect.y

        # Boundary checks (ensure these work well with touch)
        self.rect.left = max(2.5, self.rect.left)
        self.rect.right = min(
            self.settings.WIDTH - 2.5, self.rect.right
        )  # Use settings.WIDTH
        self.rect.top = max(
            self.settings.HEIGHT // 2, self.rect.top # Player stays in bottom half
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