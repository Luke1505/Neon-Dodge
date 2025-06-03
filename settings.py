# settings.py

# Screen Dimensions
WIDTH = 600  # Increased from 600
HEIGHT = 800 # Changed from 800 for a more horizontal game
# Note: Changing WIDTH/HEIGHT might require adjustments in object positioning in game.py if not relative to screen size.

# Colors (R, G, B) - Reworked vibrant neon palette using existing names and adding new ones
NEON_GREEN = (80, 255, 40)      # Vivid Lime Green (adjusted from 0, 255, 180)
NEON_BLUE = (0, 220, 255)       # Brighter Cyan/Teal (adjusted from 100, 150, 255)
NEON_YELLOW = (255, 255, 80)    # Brighter Yellow (adjusted from 255, 255, 0)
NEON_RED = (255, 0, 0)          # Classic Red (kept)
NEON_MAGENTA = (255, 50, 255)   # Intense Magenta/Fuchsia (adjusted from 255, 0, 255)
NEON_CYAN = (0, 255, 255)       # Classic Cyan (kept, will be used as Transparent_Effect)
NEON_ORANGE = (255, 180, 0)     # More intense Orange (newly added for obstacles)
NEON_PURPLE = (190, 110, 255)   # Bright Purple (newly added)
NEON_PINK = (255, 100, 200)     # Bright Pink (newly added for menu title)

# Background/UI shades
DEEP_SPACE_BLACK = (10, 10, 30) # Even darker background (used for BACKGROUND_COLOR)
ACCENT_DARK_BLUE = (40, 40, 90) # Slightly lighter for elements/buttons (new)
BRIGHT_WHITE = (255, 255, 255)  # Pure white for stark text (replaces old WHITE)
LIGHT_TEXT = (220, 220, 220)    # Off-white for general text (new)
MEDIUM_TEXT = (180, 180, 180)   # Dimmer text for high scores (new)
GREY_POWERUP = (150, 150, 150)  # For companion powerup (renamed from NEON_GREY for clarity, same value)

# Game Colors
BACKGROUND_COLOR = DEEP_SPACE_BLACK

# Player
PLAYER_COLOR = NEON_BLUE # Player is bright blue
PLAYER_SPEED = 6 # Adjusted from 8 for slightly less frantic movement
INITIAL_LIVES = 3

# Obstacles
OBSTACLE_COLORS = [NEON_MAGENTA, NEON_PURPLE, NEON_GREEN, NEON_ORANGE, NEON_YELLOW] # Array of colors for obstacles
OBSTACLE_BASE_SPEED = 3.0 # Increased from 4 for starting challenge (since speed_increase is now faster)
SPLITTABLE_OBSTACLE_CHANCE = 0.25 # (kept)
BASE_OBSTACLE_SPAWN_INTERVAL = 55 # Decreased from 40 for slightly slower initial spawn for ramp up
MIN_OBSTACLE_SPAWN_INTERVAL = 20 # (kept)
SCORE_TO_REACH_MIN_INTERVAL = 500 # Increased from 150 (slower to reach max spawn rate, more gradual difficulty)
OBSTACLE_SPEED_INCREASE_INTERVAL = 70 # Increased from 15 (speed up less frequently, but by larger amounts)
OBSTACLE_SPEED_INCREASE_AMOUNT = 0.3 # Decreased from 0.4 (to compensate for less frequent but higher max speed)
MAX_OBSTACLE_SPEED = 12.0 # Increased from 12 (kept)
PARTICLES_PER_OBSTACLE_EXPLOSION = 25 # Increased from 15 for more dramatic explosions

# Bullet Settings
BULLET_SPEED = -10 # (kept)
COMPANION_BULLET_SPEED = -15 # (kept)
BULLET_COLOR = NEON_YELLOW # (kept)
COMPANION_BULLET_COLOR = NEON_GREEN # Changed to NEON_GREEN for consistency with new palette

# Power-up Settings
POWERUP_SPAWN_INTERVAL = 350 # Frames between power-up spawns (decreased from 450, more frequent powerups)
POWERUP_SIZE = 30 # (kept)
POWERUP_SPEED = 4 # (kept)
POWERUP_COLORS = { # Map powerup types to colors
    "shield": NEON_GREEN,
    "slowmo": NEON_YELLOW,
    "bomb": NEON_MAGENTA, # Changed from NEON_RED
    "shrink": NEON_PURPLE,
    "extralife": NEON_BLUE,
    "turret": GREY_POWERUP,
}

# Timed Effect Durations (in milliseconds)
SHRINK_DURATION_MS = 10000 # (kept)
SLOWMO_DURATION_MS = 5000 # (kept)
PICKUP_MESSAGE_DURATION_MS = 2000 # (kept)
PLAYER_INVINCIBILITY_DURATION_MS = 1500 # (kept)
COMPANION_DURATION_MS = 10000 # (kept)

# UI Settings
UI_TIMER_BAR_WIDTH = 120 # Increased from 100
UI_TIMER_BAR_HEIGHT = 15 # Increased from 8
UI_TIMER_BAR_BG_COLOR = ACCENT_DARK_BLUE # Changed from (50,50,50)
UI_SLOWMO_TIMER_COLOR = NEON_YELLOW # (kept)
UI_SHRINK_TIMER_COLOR = NEON_MAGENTA # (kept)
UI_PICKUP_MESSAGE_COLOR = NEON_YELLOW # Changed from (255, 255, 100) for more vibrancy

# Starfield Settings
NUM_STARS = 200 # Increased from 100 for a denser field
STAR_SPEED_MIN = 1 # (kept)
STAR_SPEED_MAX = 5 # Increased from 4 for more dynamic scroll
STAR_COLORS = [
    NEON_BLUE,       # Use new neon colors
    NEON_PURPLE,
    BRIGHT_WHITE,    # Use the new bright white
    LIGHT_TEXT,      # Use light text color
]
STAR_SIZE_MIN = 1 # (kept)
STAR_SIZE_MAX = 3 # (kept)


# Menu Settings
BUTTON_WIDTH = 250 # Increased from 220
BUTTON_HEIGHT = 50 # Increased from 45
BUTTON_COLOR_NORMAL = ACCENT_DARK_BLUE # Changed from (0, 200, 255)
BUTTON_COLOR_HOVER = (80, 80, 150) # More distinct hover color
BUTTON_TEXT_COLOR = BRIGHT_WHITE # Changed from WHITE
INPUT_BOX_COLOR_ACTIVE = NEON_BLUE # Changed from (0, 200, 255)
INPUT_BOX_COLOR_INACTIVE = ACCENT_DARK_BLUE # Changed from WHITE for consistency with new theme
MENU_TEXT_COLOR = LIGHT_TEXT # Changed from WHITE
MENU_SUBTEXT_COLOR = MEDIUM_TEXT # Changed from (200, 200, 200)
MENU_TITLE_COLOR = NEON_PINK # Changed from NEON_GREEN for consistency with the overall theme title

# Highscore File
HIGHSCORE_FILE = "highscores.json"

# Fonts (Comments from original file, these remain as comments)
# FONT_NAME = "consolas"
# FONT_SIZE_LARGE = 32
# FONT_SIZE_MEDIUM = 24
# FONT_SIZE_SMALL = 20
# FONT_SIZE_MENU_TITLE = 48
# FONT_SIZE_MENU_BUTTON = 30
# FONT_SIZE_INPUT = 28