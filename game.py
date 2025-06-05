import pygame
import random
import math
from player import Player
from obstacle import Obstacle
from powerups import PowerUp
from utils import (
    get_username,
    save_high_scores,
    update_high_scores,
    get_high_scores,
    get_high_score_value,
)
from bullet import Bullet
from companion import Companion
from particle import Particle
from dataclasses import dataclass, field
import settings
from locale_manager import _LOCALE_MANAGER_GLOBAL

# --- Dataclasses ---
@dataclass
class GameTimers:
    spawn_obstacle: int = 0
    spawn_powerup: int = 0
    slowmo_effect_end_tick: int = 0
    shrink_effect_end_tick: int = 0
    pickup_message_end_tick: int = 0
    player_invincible_end_tick: int = 0
    companion_active_end_tick: int = 0


@dataclass
class ActiveEffects:
    shield: bool = False
    bomb_ready: bool = False
    pickup_message: str = ""


# ---

# Constants for menu actions
ACTION_SHOW_INSTRUCTIONS = "SHOW_INSTRUCTIONS"
ACTION_QUIT_GAME = "QUIT_GAME"
ACTION_START_GAME = "START_GAME"
ACTION_BACK_TO_MAIN_MENU = "BACK_TO_MAIN_MENU"

def draw_simplified_flag(screen, locale_code, rect):
    """Draws a flag using Pygame primitives.
       Aims for an accurate Union Jack representation."""
    border_thickness = 2
    # Optional: Background for the flag button (from original user code)
    # pygame.draw.rect(screen, settings.ACCENT_DARK_BLUE, rect, border_radius=5)
    # Optional: Border for the flag button (from original user code)
    # pygame.draw.rect(screen, settings.BUTTON_COLOR_HOVER, rect, border_thickness, border_radius=5)

    # Define the actual flag area within the button rect
    flag_rect_inner = pygame.Rect(
        rect.x + border_thickness,
        rect.y + border_thickness,
        rect.width - 2 * border_thickness,
        rect.height - 2 * border_thickness
    )
    flag_x, flag_y, flag_width, flag_height = flag_rect_inner.topleft[0], flag_rect_inner.topleft[1], flag_rect_inner.width, flag_rect_inner.height

    if locale_code == 'en':
        # Standard Union Jack colors
        BLUE = (1, 33, 105)      # Official: Pantone 280 C
        WHITE = (255, 255, 255)
        RED = (207, 20, 43)        # Official: Pantone 186 C

        H = flag_height # Base dimension for proportions

        # Helper function for points based on fractions of flag dimensions
        def px(x_frac, y_frac):
            return (flag_x + flag_width * x_frac, flag_y + flag_height * y_frac)

        flag_aspect_ratio = flag_width / flag_height if flag_height > 0 else 2.0 # Default to 2:1 if height is 0

        # --- 1. Background ---
        pygame.draw.rect(screen, BLUE, flag_rect_inner)

        # --- 2. St Andrew's Cross (White diagonals) ---
        # Thickness of St. Andrew's cross is H/5
        ay_f = 1/5.0  # y_offset for Andrew's (fraction of height)
        ax_f = ay_f / flag_aspect_ratio # x_offset for Andrew's (fraction of width)

        # Diagonal from top-left to bottom-right
        pygame.draw.polygon(screen, WHITE, [px(0,ay_f), px(ax_f,0), px(1,1-ay_f), px(1-ax_f,1)])
        # Diagonal from top-right to bottom-left
        pygame.draw.polygon(screen, WHITE, [px(1-ax_f,0), px(1,ay_f), px(0,1-ay_f), px(ax_f,1)])

        # --- 3. St Patrick's Cross (Red diagonals, counterchanged as hexagonal arms) ---
        # Proportions for St. Patrick's parts (fractions of height H)
        py_f_patrick_red = 1/15.0    # Red part of St. Patrick's saltire (H/15)
        py_f_narrow_fimb = 1/30.0  # Narrow white fimbriation (part of St. Andrew's) (H/30)
        # Broad white fimbriation (part of St. Andrew's) is H/5 - H/15 - H/30 = H/10

        # Convert y-fractions to x-fractions based on aspect ratio
        px_f_patrick_red = py_f_patrick_red / flag_aspect_ratio
        px_f_narrow_fimb = py_f_narrow_fimb / flag_aspect_ratio

        # Each of the 4 arms of St. Patrick's cross is a hexagon.
        # Points for Arm 1 (Top-Left quadrant, '\' diagonal, red shifted "up"/anti-clockwise)
        # Narrow white fimbriation is "above" this red arm.
        P1_Y_upper = px(0, py_f_narrow_fimb)
        P1_X_upper = px(px_f_narrow_fimb, 0)
        P1_C_upper = px(0.5 - px_f_narrow_fimb, 0.5 - py_f_narrow_fimb)
        P1_C_lower = px(0.5 - (px_f_narrow_fimb + px_f_patrick_red), 0.5 - (py_f_narrow_fimb + py_f_patrick_red))
        P1_X_lower = px(px_f_narrow_fimb + px_f_patrick_red, 0)
        P1_Y_lower = px(0, py_f_narrow_fimb + py_f_patrick_red)
        pygame.draw.polygon(screen, RED, [P1_Y_upper, P1_X_upper, P1_C_upper, P1_C_lower, P1_X_lower, P1_Y_lower])

        # Points for Arm 2 (Bottom-Right quadrant, '\' diagonal, red shifted "down"/anti-clockwise)
        # Narrow white fimbriation is "below" this red arm (relative to flag, or "above" relative to BR corner looking center)
        P2_Y_upper = px(1, 1 - py_f_narrow_fimb)
        P2_X_upper = px(1 - px_f_narrow_fimb, 1)
        P2_C_upper = px(0.5 + px_f_narrow_fimb, 0.5 + py_f_narrow_fimb)
        P2_C_lower = px(0.5 + (px_f_narrow_fimb + px_f_patrick_red), 0.5 + (py_f_narrow_fimb + py_f_patrick_red))
        P2_X_lower = px(1 - (px_f_narrow_fimb + px_f_patrick_red), 1)
        P2_Y_lower = px(1, 1 - (py_f_narrow_fimb + py_f_patrick_red))
        pygame.draw.polygon(screen, RED, [P2_Y_upper, P2_X_upper, P2_C_upper, P2_C_lower, P2_X_lower, P2_Y_lower])

        # Points for Arm 3 (Top-Right quadrant, '/' diagonal, red shifted "right"/clockwise)
        # Narrow white fimbriation is to the "right" of this red arm (closer to TR corner).
        P3_X_upper = px(1 - px_f_narrow_fimb, 0)
        P3_Y_upper = px(1, py_f_narrow_fimb)
        P3_C_upper = px(0.5 + px_f_narrow_fimb, 0.5 - py_f_narrow_fimb)
        P3_C_lower = px(0.5 + (px_f_narrow_fimb + px_f_patrick_red), 0.5 - (py_f_narrow_fimb + py_f_patrick_red))
        P3_Y_lower = px(1, py_f_narrow_fimb + py_f_patrick_red)
        P3_X_lower = px(1 - (px_f_narrow_fimb + px_f_patrick_red), 0)
        pygame.draw.polygon(screen, RED, [P3_X_upper, P3_Y_upper, P3_C_upper, P3_C_lower, P3_Y_lower, P3_X_lower])
        
        # Points for Arm 4 (Bottom-Left quadrant, '/' diagonal, red shifted "left"/clockwise)
        # Narrow white fimbriation is to the "left" of this red arm (closer to BL corner).
        P4_X_upper = px(px_f_narrow_fimb, 1)
        P4_Y_upper = px(0, 1 - py_f_narrow_fimb)
        P4_C_upper = px(0.5 - px_f_narrow_fimb, 0.5 + py_f_narrow_fimb)
        P4_C_lower = px(0.5 - (px_f_narrow_fimb + px_f_patrick_red), 0.5 + (py_f_narrow_fimb + py_f_patrick_red))
        P4_Y_lower = px(0, 1 - (py_f_narrow_fimb + py_f_patrick_red))
        P4_X_lower = px(px_f_narrow_fimb + px_f_patrick_red, 1)
        pygame.draw.polygon(screen, RED, [P4_X_upper, P4_Y_upper, P4_C_upper, P4_C_lower, P4_Y_lower, P4_X_lower])

        # --- 4. St George's Cross (central red cross with white fimbriation) ---
        george_r_thick = H * (1/5.0)    # Red part H/5
        george_w_fimb_thick = H * (1/15.0) # White fimbriation H/15

        # White fimbriation (drawn first, slightly larger)
        pygame.draw.rect(screen, WHITE, ( # Horizontal white bar
            flag_x,
            flag_y + flag_height/2 - (george_r_thick/2 + george_w_fimb_thick),
            flag_width,
            george_r_thick + 2*george_w_fimb_thick
        ))
        pygame.draw.rect(screen, WHITE, ( # Vertical white bar
            flag_x + flag_width/2 - (george_r_thick/2 + george_w_fimb_thick), # Thickness based on H for visual consistency
            flag_y,
            george_r_thick + 2*george_w_fimb_thick,
            flag_height
        ))

        # Red center cross
        pygame.draw.rect(screen, RED, ( # Horizontal red bar
            flag_x,
            flag_y + flag_height/2 - george_r_thick/2,
            flag_width,
            george_r_thick
        ))
        pygame.draw.rect(screen, RED, ( # Vertical red bar
            flag_x + flag_width/2 - george_r_thick/2, # Thickness based on H
            flag_y,
            george_r_thick,
            flag_height
        ))

    elif locale_code == 'de': # German Flag
        stripe_height = flag_height / 3.0
        pygame.draw.rect(screen, (0,0,0), (flag_x, flag_y, flag_width, stripe_height)) # Black
        pygame.draw.rect(screen, (221,0,0), (flag_x, flag_y + stripe_height, flag_width, stripe_height)) # Red (official: DD0000)
        pygame.draw.rect(screen, (255,206,0), (flag_x, flag_y + 2*stripe_height, flag_width, flag_height - 2*stripe_height)) # Gold (official: FFCE00)
    else: # Fallback
        pygame.draw.rect(screen, settings.ACCENT_DARK_BLUE, flag_rect_inner)
        try:
            font = pygame.font.SysFont("consolas", 18) # Adjust font as needed
            text_surf = font.render(locale_code.upper(), True, settings.BRIGHT_WHITE)
            text_rect = text_surf.get_rect(center=flag_rect_inner.center)
            screen.blit(text_surf, text_rect)
        except pygame.error:
            print(f"Warning: Font for locale '{locale_code}' not found or error rendering.")


def draw_text_centered(screen, text, font, color, surface_rect):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=surface_rect.center)
    screen.blit(text_surf, text_rect)

def get_fitted_font(text, max_font_size, max_width, max_height, font_name="consolas"):
    """
    Returns a Pygame font object that fits the given text within the specified
    max_width and max_height, starting from max_font_size and decreasing if necessary.
    """
    for size in range(max_font_size, 10, -1):  # Iterate downwards from max_font_size
        font = pygame.font.SysFont(font_name, size)
        text_surface = font.render(text, True, (255, 255, 255))  # Color doesn't matter for size check
        if text_surface.get_width() <= max_width and text_surface.get_height() <= max_height:
            return font
    return pygame.font.SysFont(font_name, 10) # Fallback to a very small font if nothing fits


def show_main_menu(screen, username=""):
    menu_font = pygame.font.SysFont("consolas", 30)
    title_font = pygame.font.SysFont("consolas", 48)
    small_font = pygame.font.SysFont("consolas", 22)
    input_font = pygame.font.SysFont("consolas", 28)
    clock = pygame.time.Clock()
    input_box_rect = pygame.Rect(settings.WIDTH // 2 - 150, 220, 300, 40)
    input_box_active = False
    current_username = username
    cursor_position = len(current_username)
    running = True
    button_y_start = input_box_rect.bottom + 40
    button_spacing = settings.BUTTON_HEIGHT + 20
    start_button_rect = pygame.Rect(
        settings.WIDTH // 2 - settings.BUTTON_WIDTH // 2,
        button_y_start,
        settings.BUTTON_WIDTH,
        settings.BUTTON_HEIGHT,
    )
    instructions_button_rect = pygame.Rect(
        settings.WIDTH // 2 - settings.BUTTON_WIDTH // 2,
        button_y_start + button_spacing,
        settings.BUTTON_WIDTH,
        settings.BUTTON_HEIGHT,
    )
    quit_button_rect = pygame.Rect(
        settings.WIDTH // 2 - settings.BUTTON_WIDTH // 2,
        button_y_start + button_spacing * 2,
        settings.BUTTON_WIDTH,
        settings.BUTTON_HEIGHT,
    )

    cursor_blink_interval = 500
    cursor_visible = True
    last_cursor_toggle = pygame.time.get_ticks()

    stars = []
    for _ in range(settings.NUM_STARS):
        x = random.randint(0, settings.WIDTH)
        y = random.randint(0, settings.HEIGHT)
        speed = random.randint(settings.STAR_SPEED_MIN, settings.STAR_SPEED_MAX)
        color = random.choice(settings.STAR_COLORS)
        size = random.randint(settings.STAR_SIZE_MIN, settings.STAR_SIZE_MAX)
        stars.append([x, y, speed, color, size])

    available_locales = _LOCALE_MANAGER_GLOBAL.get_available_locales()
    flag_button_width = 60
    flag_button_height = 40
    flag_button_padding = 10
    total_flag_buttons_width = len(available_locales) * (flag_button_width + flag_button_padding) - flag_button_padding
    flag_start_x = settings.WIDTH - total_flag_buttons_width - 10
    flag_y = 10

    language_buttons = {}
    for i, locale_code in enumerate(available_locales):
        flag_rect = pygame.Rect(flag_start_x + i * (flag_button_width + flag_button_padding), flag_y, flag_button_width, flag_button_height)
        language_buttons[locale_code] = flag_rect


    def _update_stars():
        for i in range(len(stars)):
            star = stars[i]
            star[1] += star[2]
            if star[1] > settings.HEIGHT:
                stars[i] = [
                    random.randint(0, settings.WIDTH),
                    random.randint(-20, -5),
                    random.randint(settings.STAR_SPEED_MIN, settings.STAR_SPEED_MAX),
                    random.choice(settings.STAR_COLORS),
                    random.randint(settings.STAR_SIZE_MIN, settings.STAR_SIZE_MAX),
                ]

    def _draw_stars():
        for star_data in stars:
            pygame.draw.rect(
                screen,
                star_data[3],
                (star_data[0], star_data[1], star_data[4], star_data[4]),
            )

    while running:
        current_time = pygame.time.get_ticks()
        if current_time - last_cursor_toggle > cursor_blink_interval:
            cursor_visible = not cursor_visible
            last_cursor_toggle = current_time

        mouse_pos = pygame.mouse.get_pos() # Keep for hover
        screen.fill(settings.BACKGROUND_COLOR)
        _update_stars()
        _draw_stars()

        draw_text_centered(
            screen,
            _LOCALE_MANAGER_GLOBAL.get_text("game_title"),
            title_font,
            settings.MENU_TITLE_COLOR,
            pygame.Rect(0, 100, settings.WIDTH, title_font.get_height()),
        )
        username_label_surf = small_font.render(
            _LOCALE_MANAGER_GLOBAL.get_text("enter_username"), True, settings.MENU_TEXT_COLOR
        )
        screen.blit(
            username_label_surf,
            (input_box_rect.x, input_box_rect.y - username_label_surf.get_height() - 5),
        )
        current_input_box_color = (
            settings.INPUT_BOX_COLOR_ACTIVE
            if input_box_active
            else settings.INPUT_BOX_COLOR_INACTIVE
        )
        pygame.draw.rect(
            screen, current_input_box_color, input_box_rect, 2, border_radius=5
        )
        username_text_surf = input_font.render(
            current_username, True, settings.MENU_TEXT_COLOR
        )
        screen.blit(
            username_text_surf,
            (
                input_box_rect.x + 10,
                input_box_rect.y
                + (input_box_rect.height - username_text_surf.get_height()) // 2,
            ),
        )

        if input_box_active and cursor_visible:
            text_before_cursor = input_font.render(
                current_username[:cursor_position], True, settings.MENU_TEXT_COLOR
            )
            cursor_x = input_box_rect.x + 10 + text_before_cursor.get_width()
            cursor_y = (
                input_box_rect.y
                + (input_box_rect.height - input_font.get_height()) // 2
            )
            cursor_height = input_font.get_height()
            pygame.draw.line(
                screen,
                settings.MENU_TEXT_COLOR,
                (cursor_x, cursor_y),
                (cursor_x, cursor_y + cursor_height),
                2,
            )

        start_color = (
            settings.BUTTON_COLOR_HOVER
            if start_button_rect.collidepoint(mouse_pos)
            else settings.BUTTON_COLOR_NORMAL
        )
        pygame.draw.rect(screen, start_color, start_button_rect, border_radius=10)
        draw_text_centered(
            screen,
            _LOCALE_MANAGER_GLOBAL.get_text("start_game"),
            menu_font,
            settings.BUTTON_TEXT_COLOR,
            start_button_rect,
        )
        instr_color = (
            settings.BUTTON_COLOR_HOVER
            if instructions_button_rect.collidepoint(mouse_pos)
            else settings.BUTTON_COLOR_NORMAL
        )
        pygame.draw.rect(
            screen, instr_color, instructions_button_rect, border_radius=10
        )
        draw_text_centered(
            screen,
            _LOCALE_MANAGER_GLOBAL.get_text("instructions"),
            menu_font,
            settings.BUTTON_TEXT_COLOR,
            instructions_button_rect,
        )
        quit_color = (
            settings.BUTTON_COLOR_HOVER
            if quit_button_rect.collidepoint(mouse_pos)
            else settings.BUTTON_COLOR_NORMAL
        )
        pygame.draw.rect(screen, quit_color, quit_button_rect, border_radius=10)
        draw_text_centered(
            screen, _LOCALE_MANAGER_GLOBAL.get_text("quit"), menu_font, settings.BUTTON_TEXT_COLOR, quit_button_rect
        )
        hs_y_start = quit_button_rect.bottom + 20
        if hs_y_start + 150 > settings.HEIGHT:
            hs_y_start = settings.HEIGHT - 150
        draw_high_scores(screen, small_font, y_start=hs_y_start)

        for locale_code, flag_rect in language_buttons.items():
            draw_simplified_flag(screen, locale_code, flag_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ACTION_QUIT_GAME, current_username

            # --- Touch Event Handling for Main Menu ---
            if event.type == pygame.FINGERDOWN:
                touch_pixel_x = event.x * settings.WIDTH
                touch_pixel_y = event.y * settings.HEIGHT
                finger_pos = (touch_pixel_x, touch_pixel_y)

                input_box_active = input_box_rect.collidepoint(finger_pos)
                if input_box_active:
                    # Approximate cursor position based on touch X within the box
                    relative_x = finger_pos[0] - input_box_rect.x - 10
                    char_count = 0
                    current_width = 0
                    # Iterate through characters to find where the touch landed
                    for char in current_username:
                        char_width = input_font.size(char)[0]
                        if current_width + char_width / 2 > relative_x:
                            break
                        current_width += char_width
                        char_count +=1
                    cursor_position = char_count
                cursor_visible = True
                last_cursor_toggle = pygame.time.get_ticks()

                for locale_code, flag_rect in language_buttons.items():
                    if flag_rect.collidepoint(finger_pos):
                        _LOCALE_MANAGER_GLOBAL.set_locale(locale_code)
                        break

                # Check button presses only if not activating input box, or if touch is outside input box
                # This prevents a button press if the user is trying to tap into the text field
                if not input_box_active or not input_box_rect.collidepoint(finger_pos):
                    if start_button_rect.collidepoint(finger_pos):
                        return ACTION_START_GAME, (
                            current_username.strip()
                            if current_username.strip()
                            else _LOCALE_MANAGER_GLOBAL.get_text("guest")
                        )
                    if instructions_button_rect.collidepoint(finger_pos):
                        return (
                            ACTION_SHOW_INSTRUCTIONS,
                            current_username,
                        )
                    if quit_button_rect.collidepoint(finger_pos):
                        return (
                            ACTION_QUIT_GAME,
                            current_username,
                        )

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left mouse click
                    input_box_active = input_box_rect.collidepoint(mouse_pos)
                    if input_box_active:
                        relative_x = mouse_pos[0] - input_box_rect.x - 10
                        char_count = 0
                        current_width = 0
                        for char in current_username:
                            char_width = input_font.size(char)[0]
                            if current_width + char_width / 2 > relative_x:
                                break
                            current_width += char_width
                            char_count +=1
                        cursor_position = char_count
                    cursor_visible = True
                    last_cursor_toggle = pygame.time.get_ticks()

                    for locale_code, flag_rect in language_buttons.items():
                        if flag_rect.collidepoint(mouse_pos):
                            _LOCALE_MANAGER_GLOBAL.set_locale(locale_code)
                            break

                    if not input_box_active or not input_box_rect.collidepoint(
                        mouse_pos
                    ):
                        if start_button_rect.collidepoint(mouse_pos):
                            return ACTION_START_GAME, (
                                current_username.strip()
                                if current_username.strip()
                                else _LOCALE_MANAGER_GLOBAL.get_text("guest")
                            )
                        if instructions_button_rect.collidepoint(mouse_pos):
                            return (
                                ACTION_SHOW_INSTRUCTIONS,
                                current_username,
                            )
                        if quit_button_rect.collidepoint(mouse_pos):
                            return (
                                ACTION_QUIT_GAME,
                                current_username,
                            )

            if event.type == pygame.KEYDOWN:
                cursor_visible = True
                last_cursor_toggle = pygame.time.get_ticks()

                if input_box_active:
                    if event.key == pygame.K_RETURN:
                        return ACTION_START_GAME, (
                            current_username.strip()
                            if current_username.strip()
                            else _LOCALE_MANAGER_GLOBAL.get_text("guest")
                        )
                    elif event.key == pygame.K_BACKSPACE:
                        if cursor_position > 0:
                            current_username = (
                                current_username[: cursor_position - 1]
                                + current_username[cursor_position:]
                            )
                            cursor_position = max(0, cursor_position - 1)
                    elif event.key == pygame.K_DELETE:
                        if cursor_position < len(current_username):
                            current_username = (
                                current_username[:cursor_position]
                                + current_username[cursor_position + 1 :]
                            )
                    elif event.key == pygame.K_LEFT:
                        cursor_position = max(0, cursor_position - 1)
                    elif event.key == pygame.K_RIGHT:
                        cursor_position = min(
                            len(current_username), cursor_position + 1
                        )
                    elif event.key == pygame.K_HOME:
                        cursor_position = 0
                    elif event.key == pygame.K_END:
                        cursor_position = len(current_username)
                    else:
                        if len(current_username) < 16 and event.unicode.isprintable():
                            current_username = (
                                current_username[:cursor_position]
                                + event.unicode
                                + current_username[cursor_position:]
                            )
                            cursor_position += 1
                else: # Input box not active
                    if event.key == pygame.K_ESCAPE:
                        return (
                            ACTION_QUIT_GAME,
                            current_username,
                        )
                    if event.key == pygame.K_i: # Shortcut for instructions
                        return (
                            ACTION_SHOW_INSTRUCTIONS,
                            current_username,
                        )
                    if event.key == pygame.K_RETURN: # Shortcut for start game
                        return ACTION_START_GAME, (
                            current_username.strip()
                            if current_username.strip()
                            else _LOCALE_MANAGER_GLOBAL.get_text("guest")
                        )

        pygame.display.flip()
        clock.tick(60)
    return ACTION_QUIT_GAME, current_username # Fallback


def draw_high_scores(screen, font, y_start):
    highscores = get_high_scores()
    highscores.sort(key=lambda x: x["score"], reverse=True)
    y_pos = y_start
    title_text_surf = font.render(_LOCALE_MANAGER_GLOBAL.get_text("top_scores"), True, (255, 255, 255))
    screen.blit(
        title_text_surf, (settings.WIDTH // 2 - title_text_surf.get_width() // 2, y_pos)
    )
    y_pos += 28
    for i, entry in enumerate(highscores[:10]):
        hs_text_surf = font.render(
            f"{i+1}. {entry['username']}: {entry['score']}", True, (200, 200, 200)
        )
        screen.blit(
            hs_text_surf, (settings.WIDTH // 2 - hs_text_surf.get_width() // 2, y_pos)
        )
        y_pos += 24


class Game:
    STATE_PLAYING = "playing"
    STATE_PAUSED = "paused"
    STATE_GAME_OVER = "game_over"
    STATE_INSTRUCTIONS = "instructions"
    STATE_EXIT_TO_MENU = "exit_to_menu"
    STATE_CONFIRM_QUIT = "confirm_quit"

    def __init__(
        self,
        screen,
        username,
        ai_mode=False,
        start_state=STATE_PLAYING,
        game_settings=settings,
    ):
        self.ai_mode = ai_mode
        self.screen = screen
        self.username = username.strip() or _LOCALE_MANAGER_GLOBAL.get_text("guest")
        self.settings = game_settings
        self.locale = _LOCALE_MANAGER_GLOBAL

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 28)
        self.small_font = pygame.font.SysFont("consolas", 20)
        self.medium_font = pygame.font.SysFont("consolas", 24)
        self.large_font = pygame.font.SysFont("consolas", 32)

        self.reset_game_state()
        self.current_state = start_state
        if not self.username and start_state == self.STATE_INSTRUCTIONS:
            self.username = _LOCALE_MANAGER_GLOBAL.get_text("player") # Use a generic player name for instructions if none set

        self.pause_resume_button = None
        self.pause_instructions_button = None
        self.pause_restart_button = None
        self.pause_main_menu_button = None
        self.instructions_back_button = None
        self.game_over_restart_button = None # Specific for game over screen
        self.game_over_main_menu_button = None # Specific for game over screen


        self.confirm_quit_yes_button = None
        self.confirm_quit_no_button = None
        self.previous_state_on_quit_request = None
        self.quit_context_message = ""
        
        self.current_touch_pos = None # For player movement touch

    def _create_star(self):
        x = random.randint(0, self.settings.WIDTH)
        y = random.randint(0, self.settings.HEIGHT)
        speed = random.randint(
            self.settings.STAR_SPEED_MIN, self.settings.STAR_SPEED_MAX
        )
        color = random.choice(self.settings.STAR_COLORS)
        size = random.randint(
            self.settings.STAR_SIZE_MIN, self.settings.STAR_SIZE_MAX
        )
        return [x, y, speed, color, size]

    def _create_explosion(
        self,
        position,
        base_color,
        num_particles=settings.PARTICLES_PER_OBSTACLE_EXPLOSION,
    ):
        for _ in range(num_particles):
            self.particles.add(Particle(position[0], position[1], base_color))

    def reset_game_state(self):
        self.player = Player(self.settings)
        self.obstacles = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.score = 0
        self.high_score = get_high_score_value()
        self.obstacle_speed = self.settings.OBSTACLE_BASE_SPEED
        self.speed_multiplier = 1.0
        self.lives = self.settings.INITIAL_LIVES
        self.timers = GameTimers()
        self.effects = ActiveEffects()
        self.companion = None
        self.companion_bullets = pygame.sprite.Group()
        self.stars = [
            self._create_star() for _ in range(self.settings.NUM_STARS)
        ]
        self.particles = pygame.sprite.Group()
        self.previous_state_on_quit_request = self.STATE_PLAYING # Default previous state
        self.current_touch_pos = None


    def _update_stars(self):
        for i in range(len(self.stars)):
            star = self.stars[i]
            star[1] += star[2] * self.speed_multiplier # Consider speed_multiplier for stars too
            if star[1] > self.settings.HEIGHT:
                self.stars[i] = [
                    random.randint(0, self.settings.WIDTH),
                    random.randint(-20, -5), # Respawn off-screen top
                    random.randint(
                        self.settings.STAR_SPEED_MIN, self.settings.STAR_SPEED_MAX
                    ),
                    random.choice(self.settings.STAR_COLORS),
                    random.randint(
                        self.settings.STAR_SIZE_MIN, self.settings.STAR_SIZE_MAX
                    ),
                ]

    def _draw_stars(self):
        for star_data in self.stars:
            pygame.draw.rect(
                self.screen,
                star_data[3], # color
                (star_data[0], star_data[1], star_data[4], star_data[4]), # x, y, size, size
            )

    def update_score(self):
        # Called when game over or potentially at other points if needed
        update_high_scores(self.username, self.score)
        self.high_score = get_high_score_value() # Refresh high score display

    @staticmethod
    def ai_decide_move(player, obstacles_group):
        # This is a very basic AI, likely not used if ai_mode is False
        if not obstacles_group:
            return 0 # No action
        closest = None
        min_dist = float("inf")
        for obs in obstacles_group:
            dist = abs(obs.rect.centerx - player.rect.x) + abs(
                obs.rect.centery - player.rect.y
            ) # Simple Manhattan distance
            if dist < min_dist:
                min_dist = dist
                closest = obs
        if not closest:
            return 0
            dx = 0 # Horizontal movement direction (-1 left, 1 right)
            dy = 0 # Vertical movement direction (-1 up, 1 down)
        # Determine direction towards/away from obstacle (this logic seems to be for avoidance)
        if player.rect.x < closest.rect.centerx:
            dx = -1 # Obstacle is to the right, consider moving left
        elif player.rect.x > closest.rect.centerx:
            dx = 1  # Obstacle is to the left, consider moving right

        if player.rect.y < closest.rect.centery:
            dy = -1 # Obstacle is below, consider moving up
        elif player.rect.y > closest.rect.centery:
            dy = 1  # Obstacle is above, consider moving down

        # Prioritize dominant axis for avoidance (simplified)
        if abs(player.rect.x - closest.rect.centerx) > abs(
            player.rect.y - closest.rect.centery
        ): # Horizontal distance is greater
            return 1 if dx > 0 else 2 if dx < 0 else 0 # 1 for right, 2 for left
        else: # Vertical distance is greater or equal
            return 3 if dy < 0 else 4 if dy > 0 else 0 # 3 for up, 4 for down


    def run_instructions_loop(self):
        # This loop is usually called from main_menu when ACTION_SHOW_INSTRUCTIONS is returned
        self.current_state = self.STATE_INSTRUCTIONS # Set state
        instructions_running = True
        # The back button rect is now managed by render_instructions_screen
        # self.instructions_back_button = pygame.Rect(...)

        while instructions_running:
            mouse_pos = pygame.mouse.get_pos() # For hover on back button

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Propagate quit action if initiated from instructions
                    return ACTION_QUIT_GAME # Or handle confirm quit logic here

                if event.type == pygame.FINGERDOWN:
                    touch_pixel_x = event.x * self.settings.WIDTH
                    touch_pixel_y = event.y * self.settings.HEIGHT
                    finger_pos = (touch_pixel_x, touch_pixel_y)
                    if self.instructions_back_button and self.instructions_back_button.collidepoint(finger_pos):
                        instructions_running = False # Go back to previous screen (usually main menu or pause)
                        # The caller (main.py) will handle next state after this returns.
                        # If called from pause, this will return to pause.
                        # If called from main_menu, this returns, and main_menu loop continues.

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.instructions_back_button and self.instructions_back_button.collidepoint(mouse_pos):
                        instructions_running = False

                if event.type == pygame.KEYDOWN: # Keyboard shortcuts
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p or event.key == pygame.K_i:
                        instructions_running = False

            self.screen.fill(self.settings.BACKGROUND_COLOR) # Clear screen
            self._update_stars() # Update star positions
            self._draw_stars()   # Draw stars
            self.render_instructions_screen(mouse_pos) # Draw instructions content and back button
            pygame.display.flip() # Update display
            self.clock.tick(30) # Cap FPS for instructions screen

        # When instructions_running becomes False, decide what to return.
        # If instructions were launched from main menu, it implicitly returns to main menu loop.
        # If instructions were launched from pause menu, it should return to pause menu.
        # The current logic implies it just exits this loop and the calling context resumes.
        # No explicit action return needed here unless it's a quit action.
        return ACTION_BACK_TO_MAIN_MENU # Or a more context-aware return value if needed

    def game_loop(self):
        # Main game loop
        while self.current_state not in [self.STATE_EXIT_TO_MENU, ACTION_QUIT_GAME]:
            self.screen.fill(self.settings.BACKGROUND_COLOR) # Base background
            self.handle_events() # Process inputs

            if self.current_state == self.STATE_PLAYING:
                self.update_game_logic() # Update game objects and state

            self.render_game() # Draw everything
            pygame.display.flip() # Show the new frame
            self.clock.tick(60) # Cap FPS

        # Loop ended, determine why
        if self.current_state == self.STATE_EXIT_TO_MENU:
            return ACTION_BACK_TO_MAIN_MENU # Signal to go back to main menu
        return ACTION_QUIT_GAME # Default to quit game if not explicitly exiting to menu

    def handle_events(self):
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        
        # Reset touch for player movement unless an event updates it
        # self.current_touch_pos = None # More robust: only clear on FINGERUP or if not STATE_PLAYING

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.previous_state_on_quit_request = self.current_state
                self.quit_context_message = self.locale.get_text("quit_game_prompt")
                self.current_state = self.STATE_CONFIRM_QUIT
                return # Exit event loop for this frame to show confirm screen

            # --- Player Movement Touch Handling (Only in STATE_PLAYING) ---
            if self.current_state == self.STATE_PLAYING:
                if e.type == pygame.FINGERDOWN:
                    self.current_touch_pos = (e.x, e.y) # Normalized 0.0-1.0
                elif e.type == pygame.FINGERMOTION:
                    if self.current_touch_pos: # Only if a finger is already down
                         self.current_touch_pos = (e.x, e.y)
                elif e.type == pygame.FINGERUP:
                    self.current_touch_pos = None
            elif self.current_touch_pos is not None and self.current_state != self.STATE_PLAYING :
                # Clear touch if game state changes away from playing and a touch was active
                self.current_touch_pos = None


            # --- Touch UI Interactions (FINGERDOWN) ---
            if e.type == pygame.FINGERDOWN:
                touch_pixel_x = e.x * self.settings.WIDTH
                touch_pixel_y = e.y * self.settings.HEIGHT
                finger_pos = (touch_pixel_x, touch_pixel_y)

                if self.current_state == self.STATE_PAUSED:
                    if self.pause_resume_button and self.pause_resume_button.collidepoint(finger_pos):
                        self.current_state = self.STATE_PLAYING
                    elif self.pause_instructions_button and self.pause_instructions_button.collidepoint(finger_pos):
                        self.current_state = self.STATE_INSTRUCTIONS
                    elif self.pause_restart_button and self.pause_restart_button.collidepoint(finger_pos):
                        self.previous_state_on_quit_request = self.STATE_PAUSED
                        self.quit_context_message = self.locale.get_text("restart_main_menu_prompt")
                        self.current_state = self.STATE_CONFIRM_QUIT
                    elif self.pause_main_menu_button and self.pause_main_menu_button.collidepoint(finger_pos):
                        self.previous_state_on_quit_request = self.STATE_PAUSED
                        self.quit_context_message = self.locale.get_text("quit_main_menu_prompt")
                        self.current_state = self.STATE_CONFIRM_QUIT
                elif self.current_state == self.STATE_INSTRUCTIONS: # In-game instructions
                    if self.instructions_back_button and self.instructions_back_button.collidepoint(finger_pos):
                        self.current_state = self.STATE_PAUSED # Or wherever it was launched from
                elif self.current_state == self.STATE_GAME_OVER:
                    if self.game_over_restart_button and self.game_over_restart_button.collidepoint(finger_pos):
                        self.previous_state_on_quit_request = self.STATE_GAME_OVER
                        self.quit_context_message = self.locale.get_text("restart_main_menu_prompt")
                        self.current_state = self.STATE_CONFIRM_QUIT
                    elif self.game_over_main_menu_button and self.game_over_main_menu_button.collidepoint(finger_pos):
                        self.previous_state_on_quit_request = self.STATE_GAME_OVER
                        self.quit_context_message = self.locale.get_text("quit_main_menu_prompt")
                        self.current_state = self.STATE_CONFIRM_QUIT
                elif self.current_state == self.STATE_CONFIRM_QUIT:
                    if self.confirm_quit_yes_button and self.confirm_quit_yes_button.collidepoint(finger_pos):
                        if self.quit_context_message == self.locale.get_text("quit_game_prompt"):
                            self.current_state = ACTION_QUIT_GAME
                        else: # For restart or main menu from pause/game_over
                            self.current_state = self.STATE_EXIT_TO_MENU
                    elif self.confirm_quit_no_button and self.confirm_quit_no_button.collidepoint(finger_pos):
                        self.current_state = self.previous_state_on_quit_request


            # --- Mouse UI Interactions (MOUSEBUTTONDOWN) ---
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1: # Left click
                if self.current_state == self.STATE_PAUSED:
                    if self.pause_resume_button and self.pause_resume_button.collidepoint(mouse_pos):
                        self.current_state = self.STATE_PLAYING
                    elif self.pause_instructions_button and self.pause_instructions_button.collidepoint(mouse_pos):
                        self.current_state = self.STATE_INSTRUCTIONS
                    elif self.pause_restart_button and self.pause_restart_button.collidepoint(mouse_pos):
                        self.previous_state_on_quit_request = self.STATE_PAUSED
                        self.quit_context_message = self.locale.get_text("restart_main_menu_prompt")
                        self.current_state = self.STATE_CONFIRM_QUIT
                    elif self.pause_main_menu_button and self.pause_main_menu_button.collidepoint(mouse_pos):
                        self.previous_state_on_quit_request = self.STATE_PAUSED
                        self.quit_context_message = self.locale.get_text("quit_main_menu_prompt")
                        self.current_state = self.STATE_CONFIRM_QUIT
                elif self.current_state == self.STATE_INSTRUCTIONS:
                    if self.instructions_back_button and self.instructions_back_button.collidepoint(mouse_pos):
                        self.current_state = self.STATE_PAUSED # Or previous state
                elif self.current_state == self.STATE_GAME_OVER:
                     if self.game_over_restart_button and self.game_over_restart_button.collidepoint(mouse_pos):
                        self.previous_state_on_quit_request = self.STATE_GAME_OVER
                        self.quit_context_message = self.locale.get_text("restart_main_menu_prompt")
                        self.current_state = self.STATE_CONFIRM_QUIT
                     elif self.game_over_main_menu_button and self.game_over_main_menu_button.collidepoint(mouse_pos):
                        self.previous_state_on_quit_request = self.STATE_GAME_OVER
                        self.quit_context_message = self.locale.get_text("quit_main_menu_prompt")
                        self.current_state = self.STATE_CONFIRM_QUIT
                elif self.current_state == self.STATE_CONFIRM_QUIT:
                    if self.confirm_quit_yes_button and self.confirm_quit_yes_button.collidepoint(mouse_pos):
                        if self.quit_context_message == self.locale.get_text("quit_game_prompt"):
                            self.current_state = ACTION_QUIT_GAME
                        else:
                            self.current_state = self.STATE_EXIT_TO_MENU
                    elif self.confirm_quit_no_button and self.confirm_quit_no_button.collidepoint(mouse_pos):
                        self.current_state = self.previous_state_on_quit_request

            # --- Keyboard Shortcuts ---
            if e.type == pygame.KEYDOWN:
                if self.current_state == self.STATE_PLAYING:
                    if e.key == pygame.K_p:
                        self.current_state = self.STATE_PAUSED
                    elif e.key == pygame.K_ESCAPE: # Esc in playing goes to pause confirmation
                        self.previous_state_on_quit_request = self.STATE_PLAYING # To return to playing if 'No'
                        self.quit_context_message = self.locale.get_text("go_to_pause_menu_prompt") # "Go to Pause Menu?"
                        self.current_state = self.STATE_CONFIRM_QUIT
                elif self.current_state == self.STATE_PAUSED:
                    if e.key == pygame.K_p:
                        self.current_state = self.STATE_PLAYING
                    elif e.key == pygame.K_i:
                        self.current_state = self.STATE_INSTRUCTIONS
                    elif e.key == pygame.K_ESCAPE: # Esc in pause goes to main menu confirmation
                        self.previous_state_on_quit_request = self.STATE_PAUSED
                        self.quit_context_message = self.locale.get_text("quit_main_menu_prompt")
                        self.current_state = self.STATE_CONFIRM_QUIT
                    elif e.key == pygame.K_r: # R in pause goes to restart confirmation
                        self.previous_state_on_quit_request = self.STATE_PAUSED
                        self.quit_context_message = self.locale.get_text("restart_main_menu_prompt")
                        self.current_state = self.STATE_CONFIRM_QUIT
                elif self.current_state == self.STATE_GAME_OVER:
                    if e.key == pygame.K_r: # Restart
                        self.previous_state_on_quit_request = self.STATE_GAME_OVER
                        self.quit_context_message = self.locale.get_text("restart_main_menu_prompt")
                        self.current_state = self.STATE_CONFIRM_QUIT
                    elif e.key == pygame.K_ESCAPE: # Main Menu
                        self.previous_state_on_quit_request = self.STATE_GAME_OVER
                        self.quit_context_message = self.locale.get_text("quit_main_menu_prompt")
                        self.current_state = self.STATE_CONFIRM_QUIT
                elif self.current_state == self.STATE_INSTRUCTIONS:
                    if (
                        e.key == pygame.K_p
                        or e.key == pygame.K_ESCAPE
                        or e.key == pygame.K_i
                    ): # Exit instructions
                        self.current_state = self.STATE_PAUSED # Assume instructions launched from pause
                elif self.current_state == self.STATE_CONFIRM_QUIT:
                    if e.key == pygame.K_y: # Yes
                        if self.quit_context_message == self.locale.get_text("quit_game_prompt"):
                            self.current_state = ACTION_QUIT_GAME
                        elif self.quit_context_message == self.locale.get_text("go_to_pause_menu_prompt"):
                            self.current_state = self.STATE_PAUSED # Go to pause menu
                        else: # For restart or main menu from pause/game_over
                            self.current_state = self.STATE_EXIT_TO_MENU
                    elif e.key == pygame.K_n: # No
                        self.current_state = self.previous_state_on_quit_request


        # --- Player Movement Call (Keyboard and Touch) ---
        if not self.ai_mode and self.current_state == self.STATE_PLAYING:
            self.player.move(keys, self.current_touch_pos)
        elif not self.ai_mode : # If not playing, ensure player doesn't move via stale touch_pos
             self.player.move(keys, None) # Pass None for touch if not in playing state

    def update_game_logic(self):
        now = pygame.time.get_ticks() # Current time
        if self.ai_mode:
            # AI logic would go here, potentially calling self.player.move()
            pass # Placeholder
        self._update_stars() # Move stars
        self.timers.spawn_obstacle += 1 # Increment obstacle spawn timer

        # Dynamic obstacle spawn interval based on score
        current_spawn_interval = (
            self.settings.BASE_OBSTACLE_SPAWN_INTERVAL
        )
        if self.settings.SCORE_TO_REACH_MIN_INTERVAL > 0: # Avoid division by zero if not set
            if self.score >= self.settings.SCORE_TO_REACH_MIN_INTERVAL:
                current_spawn_interval = (
                    self.settings.MIN_OBSTACLE_SPAWN_INTERVAL
                )
            else:
                # Linearly interpolate spawn interval
                progress = (
                    self.score / self.settings.SCORE_TO_REACH_MIN_INTERVAL
                )
                interval_reduction = (
                    self.settings.BASE_OBSTACLE_SPAWN_INTERVAL
                    - self.settings.MIN_OBSTACLE_SPAWN_INTERVAL
                ) * progress
                current_spawn_interval = (
                    self.settings.BASE_OBSTACLE_SPAWN_INTERVAL - interval_reduction
                )
        current_spawn_interval = max(
            self.settings.MIN_OBSTACLE_SPAWN_INTERVAL, int(current_spawn_interval)
        ) # Ensure it doesn't go below min

        # Spawn new obstacle if timer exceeds interval
        if self.timers.spawn_obstacle > current_spawn_interval:
            self.timers.spawn_obstacle = 0 # Reset timer
            new_obstacle = None
            # Chance to spawn a splittable obstacle
            if random.random() < self.settings.SPLITTABLE_OBSTACLE_CHANCE:
                new_obstacle = Obstacle(
                    self.obstacle_speed, 1, True, 2, game_settings=self.settings
                )
            else:
                new_obstacle = Obstacle(
                    self.obstacle_speed, 1, False, game_settings=self.settings
                )
            if new_obstacle:
                self.obstacles.add(new_obstacle)

            self.score += 1 # Increment score for surviving longer / spawning obstacles

            # Increase obstacle speed based on score milestones
            if (
                self.score > 0
                and self.score % self.settings.OBSTACLE_SPEED_INCREASE_INTERVAL == 0
                and self.obstacle_speed < self.settings.MAX_OBSTACLE_SPEED
            ):
                # Ensure speed increases only once per milestone
                if (self.score // self.settings.OBSTACLE_SPEED_INCREASE_INTERVAL) > (
                    (self.score - 1) // self.settings.OBSTACLE_SPEED_INCREASE_INTERVAL
                ):
                    self.obstacle_speed = min(
                        self.obstacle_speed
                        + self.settings.OBSTACLE_SPEED_INCREASE_AMOUNT,
                        self.settings.MAX_OBSTACLE_SPEED,
                    )

        self.update_powerups() # Handle powerup spawning
        self.update_effects(now) # Update durations of active effects (shrink, slowmo)

        # Companion (turret) logic
        if self.companion:
            if now < self.timers.companion_active_end_tick: # If companion is active
                new_bullets = self.companion.update(self.player.rect) # Update companion, may shoot
                if new_bullets:
                    self.companion_bullets.add(new_bullets)
            else:
                self.companion = None # Companion duration expired

        self.companion_bullets.update() # Move companion bullets
        self.obstacles.update(self.speed_multiplier) # Move obstacles (affected by slowmo)
        self.powerups.update() # Move powerups
        self.particles.update() # Update explosion particles

        self.check_collisions(now) # Handle collisions

    def update_effects(self, now):
        # Check and apply Shrink effect
        is_shrink_active = now < self.timers.shrink_effect_end_tick
        # Check and apply SlowMo effect
        is_slowmo_active = now < self.timers.slowmo_effect_end_tick

        new_width = 30 if is_shrink_active else self.player.original_width
        new_height = 15 if is_shrink_active else self.player.original_height

        if self.player.width != new_width or self.player.height != new_height:
            self.player.width = new_width
            self.player.update_visuals() # Recreate player image if size changed
            
        # Game speed multiplier for SlowMo
        self.speed_multiplier = 0.5 if is_slowmo_active else 1.0

        if self.effects.pickup_message and now >= self.timers.pickup_message_end_tick:
            self.effects.pickup_message = ""

    def check_collisions(self, now):
        # Player vs Obstacles
        collided_obs_player = pygame.sprite.spritecollide(
            self.player, self.obstacles, False # False: do not kill obstacles yet
        )
        if collided_obs_player:
            is_player_invincible = now < self.timers.player_invincible_end_tick # Temp invincibility after hit
            if not is_player_invincible:
                for obs in collided_obs_player: # Process each colliding obstacle
                    if self.effects.shield: # If shield is active
                        self.effects.shield = False # Shield breaks
                        self._create_explosion(obs.rect.center, obs.color)
                        obs.kill() # Destroy obstacle
                        self.effects.pickup_message = self.locale.get_text("shield_lost")
                        self.timers.pickup_message_end_tick = (
                            now + self.settings.PICKUP_MESSAGE_DURATION_MS
                        )
                    else: # No shield, player takes a hit
                        self.lives -= 1
                        self._create_explosion(obs.rect.center, obs.color)
                        obs.kill()
                        if self.lives <= 0:
                            self.current_state = self.STATE_GAME_OVER
                            self.update_score() # Save score on game over
                            break # Exit collision check loop for this frame
                        else:
                            # Grant temporary invincibility
                            self.timers.player_invincible_end_tick = (
                                now + self.settings.PLAYER_INVINCIBILITY_DURATION_MS
                            )
                            self.effects.pickup_message = self.locale.get_text("life_lost", self.lives)
                            self.timers.pickup_message_end_tick = (
                                now + self.settings.PICKUP_MESSAGE_DURATION_MS
                            )
            elif collided_obs_player: # Player is invincible but still collides
                 for obs in collided_obs_player: # Destroy obstacle without penalty
                    self._create_explosion(obs.rect.center, obs.color)
                    obs.kill()

        # Companion Bullets vs Obstacles
        bullet_hits = pygame.sprite.groupcollide(
            self.companion_bullets, self.obstacles, True, False # True: kill bullet, False: don't kill obstacle yet
        )
        for bullet, hit_obs_list in bullet_hits.items():
            for obs in hit_obs_list:
                self.score += 1 # Score for turret kills
                self._create_explosion(obs.rect.center, obs.color)
                obs.kill() # Destroy obstacle hit by bullet

        # Player vs PowerUps
        collided_powerups_player = pygame.sprite.spritecollide(
            self.player, self.powerups, True # True: kill (collect) powerup
        )
        for p_up in collided_powerups_player:
            self.handle_powerup_pickup(p_up, now)

    def update_powerups(self):
        # Spawn powerups periodically
        self.timers.spawn_powerup += 1
        if self.timers.spawn_powerup > self.settings.POWERUP_SPAWN_INTERVAL:
            self.powerups.add(PowerUp(game_settings=self.settings)) # Add a new powerup
            self.timers.spawn_powerup = 0 # Reset spawn timer

    def handle_powerup_pickup(self, powerup, current_tick):
        # Set duration for pickup message display
        self.timers.pickup_message_end_tick = (
            current_tick + self.settings.PICKUP_MESSAGE_DURATION_MS
        )
        if powerup.type == "shield":
            self.effects.shield = True
            self.effects.pickup_message = self.locale.get_text("shield_activated")
        elif powerup.type == "slowmo":
            self.timers.slowmo_effect_end_tick = (
                current_tick + self.settings.SLOWMO_DURATION_MS
            )
            self.effects.pickup_message = self.locale.get_text("slow_motion")
        elif powerup.type == "bomb":
            self.effects.pickup_message = self.locale.get_text("kaboom")
            newly_split_obstacles = []
            for obs in list(self.obstacles.sprites()): # Iterate over a copy
                self._create_explosion(
                    obs.rect.center,
                    obs.color,
                    num_particles=self.settings.PARTICLES_PER_OBSTACLE_EXPLOSION // 2, # Fewer particles for bomb
                )
                # If obstacle can split, get its pieces
                if (
                    hasattr(obs, "can_split")
                    and obs.can_split
                    and hasattr(obs, "get_split_pieces") # Ensure method exists
                ):
                    pieces = obs.get_split_pieces()
                    newly_split_obstacles.extend(pieces)
                obs.kill() # Destroy original obstacle
            self.obstacles.add(newly_split_obstacles) # Add any split pieces
        elif powerup.type == "shrink":
            self.timers.shrink_effect_end_tick = (
                current_tick + self.settings.SHRINK_DURATION_MS
            )
            self.effects.pickup_message = self.locale.get_text("shrink_activated")
        elif powerup.type == "extralife":
            self.lives += 1
            self.effects.pickup_message = self.locale.get_text("extra_life", self.lives)
        elif powerup.type == "turret":
            self.companion = Companion(self.player.rect, game_settings=self.settings)
            self.timers.companion_active_end_tick = (
                current_tick + self.settings.COMPANION_DURATION_MS
            )
            self.effects.pickup_message = self.locale.get_text("turret_activated")
            
    def render_instructions_screen(self, mouse_pos=None, back_button_override_rect=None):
        # Semi-transparent overlay for instructions
        overlay = pygame.Surface((self.settings.WIDTH, self.settings.HEIGHT), pygame.SRCALPHA)
        overlay.fill((15, 15, 35, 230)) # RGBA, A for alpha
        self.screen.blit(overlay, (0, 0))

        y_offset = 60 # Initial Y position for drawing
        title_surf = self.large_font.render(
            self.locale.get_text("instructions"), True, self.settings.MENU_TITLE_COLOR
        )
        self.screen.blit(
            title_surf,
            (self.settings.WIDTH // 2 - title_surf.get_width() // 2, y_offset),
        )
        y_offset += title_surf.get_height() + 30 # Space after title

        instructions_content_start_y = y_offset
        instructions_content_width = self.settings.WIDTH * 0.85 # Slightly wider content area
        instructions_content_x = (self.settings.WIDTH - instructions_content_width) // 2

        instructions = [
            (self.locale.get_text("controls_title"), True, self.settings.BRIGHT_WHITE), # Titles brighter
            (self.locale.get_text("controls_move"), False, self.settings.LIGHT_TEXT),
            (self.locale.get_text("controls_pause"), False, self.settings.LIGHT_TEXT),
            (self.locale.get_text("controls_instructions"), False, self.settings.LIGHT_TEXT),
            (self.locale.get_text("controls_escape"), False, self.settings.LIGHT_TEXT),
            ("", False, self.settings.LIGHT_TEXT), # Spacer
            (self.locale.get_text("objective_title"), True, self.settings.BRIGHT_WHITE),
            (self.locale.get_text("objective_dodge"), False, self.settings.LIGHT_TEXT),
            (self.locale.get_text("objective_collect"), False, self.settings.LIGHT_TEXT),
            ("", False, self.settings.LIGHT_TEXT), # Spacer
            (self.locale.get_text("powerups_title"), True, self.settings.BRIGHT_WHITE),
            (self.locale.get_text("powerup_shield"), False, self.settings.POWERUP_COLORS.get("shield", self.settings.LIGHT_TEXT)),
            (self.locale.get_text("powerup_slowmo"), False, self.settings.POWERUP_COLORS.get("slowmo", self.settings.LIGHT_TEXT)),
            (self.locale.get_text("powerup_bomb"), False, self.settings.POWERUP_COLORS.get("bomb", self.settings.LIGHT_TEXT)),
            (self.locale.get_text("powerup_shrink"), False, self.settings.POWERUP_COLORS.get("shrink", self.settings.LIGHT_TEXT)),
            (self.locale.get_text("powerup_extralife"), False, self.settings.POWERUP_COLORS.get("extralife", self.settings.LIGHT_TEXT)),
            (self.locale.get_text("powerup_turret"), False, self.settings.POWERUP_COLORS.get("turret", self.settings.LIGHT_TEXT)),
        ]

        current_y_for_text = y_offset
        line_spacing = 8 # Increased spacing between lines

        for text, is_title, text_color in instructions:
            if not text: # Handle empty strings as spacers
                current_y_for_text += line_spacing 
                continue

            font_to_use = self.medium_font if is_title else self.small_font
            
            # Word wrapping logic
            words = text.split(' ')
            lines = []
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                if font_to_use.size(test_line)[0] < instructions_content_width:
                    current_line = test_line
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "
            lines.append(current_line.strip()) # Add the last line

            for line_text in lines:
                if not line_text: continue
                text_surf = font_to_use.render(line_text, True, text_color)
                text_x_position = instructions_content_x
                if is_title: # Center titles within the content area
                     text_x_position = instructions_content_x + (instructions_content_width - text_surf.get_width()) // 2

                self.screen.blit(text_surf, (text_x_position, current_y_for_text))
                current_y_for_text += text_surf.get_height() + (line_spacing // 2)
            
            if is_title:
                 current_y_for_text += (line_spacing // 2) # Extra space after titles


        # Back Button
        final_button_y = max(current_y_for_text + 20, self.settings.HEIGHT - self.settings.BUTTON_HEIGHT - 40)
        cbbr = (
            back_button_override_rect # Use if provided (e.g., from older call)
            if back_button_override_rect
            else pygame.Rect( # Default position
                self.settings.WIDTH // 2 - self.settings.BUTTON_WIDTH // 2,
                final_button_y,
                self.settings.BUTTON_WIDTH,
                self.settings.BUTTON_HEIGHT,
            )
        )
        self.instructions_back_button = cbbr # Store for event handling
        
        bc = self.settings.BUTTON_COLOR_NORMAL # Default button color
        if mouse_pos and cbbr.collidepoint(mouse_pos): # Hover effect
            bc = self.settings.BUTTON_COLOR_HOVER
        pygame.draw.rect(self.screen, bc, cbbr, border_radius=10)
        draw_text_centered(
            self.screen,
            self.locale.get_text("back_button"), # Text for back button
            self.medium_font,
            self.settings.BUTTON_TEXT_COLOR,
            cbbr,
        )


    def render_confirm_quit_screen(self, mouse_pos=None):
        # Overlay for confirm quit dialog
        overlay = pygame.Surface((self.settings.WIDTH, self.settings.HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 10, 20, 230)) # Dark, semi-transparent
        self.screen.blit(overlay, (0, 0))

        # Dialog box
        dialog_width = self.settings.WIDTH * 0.7
        dialog_height = self.settings.HEIGHT * 0.4 # Adjusted height
        dialog_x = self.settings.WIDTH // 2 - dialog_width // 2
        dialog_y = self.settings.HEIGHT // 2 - dialog_height // 2
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)

        pygame.draw.rect(self.screen, (30, 30, 50), dialog_rect, border_radius=15) # Dialog background
        pygame.draw.rect( # Dialog border
            self.screen,
            self.settings.MENU_TITLE_COLOR, # Use a distinct border color
            dialog_rect,
            3, # Border thickness
            border_radius=15,
        )

        # Title "Confirm Exit"
        title_surf = self.large_font.render(
            self.locale.get_text("confirm_exit"), True, self.settings.MENU_TEXT_COLOR
        )
        self.screen.blit(
            title_surf,
            (dialog_rect.centerx - title_surf.get_width() // 2, dialog_rect.top + 30),
        )

        # Context message (e.g., "Quit Game?", "Restart?")
        query_surf = self.font.render(
            self.quit_context_message, True, self.settings.MENU_SUBTEXT_COLOR
        )
        self.screen.blit(
            query_surf,
            (dialog_rect.centerx - query_surf.get_width() // 2, dialog_rect.top + 90),
        )

        # Yes/No Buttons
        button_w, button_h = 120, self.settings.BUTTON_HEIGHT
        gap = 30 # Gap between buttons
        total_buttons_width = button_w * 2 + gap
        # Yes button rect
        self.confirm_quit_yes_button = pygame.Rect(
            dialog_rect.centerx - total_buttons_width // 2, # Position Yes button
            dialog_rect.bottom - button_h - 40, # Y position from bottom of dialog
            button_w,
            button_h,
        )
        # No button rect
        self.confirm_quit_no_button = pygame.Rect(
            self.confirm_quit_yes_button.right + gap, # Position No button relative to Yes
            self.confirm_quit_yes_button.top, # Same Y as Yes button
            button_w,
            button_h,
        )

        # Draw Yes button with hover
        yes_color = (
            self.settings.BUTTON_COLOR_HOVER
            if mouse_pos and self.confirm_quit_yes_button.collidepoint(mouse_pos)
            else self.settings.BUTTON_COLOR_NORMAL
        )
        pygame.draw.rect(
            self.screen, yes_color, self.confirm_quit_yes_button, border_radius=10
        )
        draw_text_centered(
            self.screen,
            self.locale.get_text("yes_button"),
            self.medium_font,
            self.settings.BUTTON_TEXT_COLOR,
            self.confirm_quit_yes_button,
        )

        # Draw No button with hover
        no_color = (
            self.settings.BUTTON_COLOR_HOVER
            if mouse_pos and self.confirm_quit_no_button.collidepoint(mouse_pos)
            else self.settings.BUTTON_COLOR_NORMAL
        )
        pygame.draw.rect(
            self.screen, no_color, self.confirm_quit_no_button, border_radius=10
        )
        draw_text_centered(
            self.screen,
            self.locale.get_text("no_button"),
            self.medium_font,
            self.settings.BUTTON_TEXT_COLOR,
            self.confirm_quit_no_button,
        )

    def render_game(self):
        now = pygame.time.get_ticks() # Get current time for animations/timers
        self._draw_stars() # Draw background stars first
        mouse_pos = pygame.mouse.get_pos() # Get mouse position for UI hovers

        # Draw game elements if playing or paused (but not game over, etc.)
        if (
            self.current_state == self.STATE_PLAYING
            or self.current_state == self.STATE_PAUSED # Still show game scene when paused
        ):
            # Player invincibility visual flicker
            is_player_invincible_visual = now < self.timers.player_invincible_end_tick
            if is_player_invincible_visual and (now // 100) % 2 == 0: # Flicker effect
                pass # Don't draw player to make it "blink"
            else:
                self.player.draw(self.screen)

            self.obstacles.draw(self.screen)
            self.powerups.draw(self.screen)
            if self.companion:
                self.companion.draw(self.screen)
            self.companion_bullets.draw(self.screen)
            self.particles.draw(self.screen) # Draw explosion particles

        self.render_ui(now) # Draw HUD elements (score, lives, timers)

        # Render overlay screens based on current state
        if self.current_state == self.STATE_PAUSED:
            self.show_pause_or_gameover_screen(self.locale.get_text("paused"), mouse_pos)
        elif self.current_state == self.STATE_GAME_OVER:
            self.show_pause_or_gameover_screen(self.locale.get_text("game_over"), mouse_pos)
        elif self.current_state == self.STATE_INSTRUCTIONS:
            self.render_instructions_screen(mouse_pos) # In-game instructions screen
        elif self.current_state == self.STATE_CONFIRM_QUIT:
            self.render_confirm_quit_screen(mouse_pos) # Confirmation dialog

    def render_ui(self, now):
        # Player and Score Info
        self.screen.blit(
            self.font.render(self.locale.get_text("player_score", self.username), True, settings.BRIGHT_WHITE),
            (10, 10),
        )
        self.screen.blit(
            self.font.render(self.locale.get_text("score", self.score), True, settings.BRIGHT_WHITE), (10, 40)
        )
        self.screen.blit(
            self.font.render(self.locale.get_text("lives", self.lives), True, settings.BRIGHT_WHITE), (10, 70)
        )

        # High Score
        hs_text_surf = self.font.render(
            self.locale.get_text("high_score", self.high_score), True, settings.BRIGHT_WHITE
        )
        self.screen.blit(
            hs_text_surf, (self.settings.WIDTH - hs_text_surf.get_width() - 10, 10)
        )

        # --- Timers and Effects UI (Right side of screen) ---
        ui_timer_y_current = 40 # Initial Y for first timer bar/text
        ui_timer_x_pos = self.settings.WIDTH - self.settings.UI_TIMER_BAR_WIDTH - 10 # X for timer bars
        label_padding = 5 # Padding between label and bar
        timer_spacing = self.settings.UI_TIMER_BAR_HEIGHT + 10 # Vertical spacing between timers
        
        # Turret Timer Bar
        if self.companion and now < self.timers.companion_active_end_tick:
            time_left = self.timers.companion_active_end_tick - now
            percentage_left = max(
                0, time_left / self.settings.COMPANION_DURATION_MS # Ensure not negative
            )
            turret_label_surf = self.small_font.render(
                self.locale.get_text("turret"), True, self.settings.UI_TURRET_TIMER_COLOR
            )
            label_y = ( # Center label vertically with the bar
                ui_timer_y_current
                + (self.settings.UI_TIMER_BAR_HEIGHT - turret_label_surf.get_height())// 2
            )
            self.screen.blit( # Draw "Turret" label
                turret_label_surf,
                (
                    ui_timer_x_pos - turret_label_surf.get_width() - label_padding, # Left of bar
                    label_y,
                ),
            )
            # Background of timer bar
            pygame.draw.rect(
                self.screen,
                self.settings.UI_TIMER_BAR_BG_COLOR,
                (
                    ui_timer_x_pos,
                    ui_timer_y_current,
                    self.settings.UI_TIMER_BAR_WIDTH,
                    self.settings.UI_TIMER_BAR_HEIGHT,
                ),
                border_radius=3
            )
            # Current progress of timer bar
            current_bar_width = int(self.settings.UI_TIMER_BAR_WIDTH * percentage_left)
            pygame.draw.rect(
                self.screen,
                self.settings.UI_TURRET_TIMER_COLOR,
                (
                    ui_timer_x_pos,
                    ui_timer_y_current,
                    current_bar_width,
                    self.settings.UI_TIMER_BAR_HEIGHT,
                ),
                border_radius=3
            )
            ui_timer_y_current += (
                self.settings.UI_TIMER_BAR_HEIGHT + timer_spacing
            )
        # SlowMo Timer Bar
        if now < self.timers.slowmo_effect_end_tick:
            time_left = self.timers.slowmo_effect_end_tick - now
            percentage_left = max(
                0, time_left / self.settings.SLOWMO_DURATION_MS # Ensure not negative
            )
            slowmo_label_surf = self.small_font.render(
                self.locale.get_text("slowmo"), True, self.settings.UI_SLOWMO_TIMER_COLOR
            )
            label_y = ( # Center label vertically with the bar
                ui_timer_y_current
                + (self.settings.UI_TIMER_BAR_HEIGHT - slowmo_label_surf.get_height())// 2
            )
            self.screen.blit( # Draw "SlowMo" label
                slowmo_label_surf,
                (
                    ui_timer_x_pos - slowmo_label_surf.get_width() - label_padding, # Left of bar
                    label_y,
                ),
            )
            # Background of timer bar
            pygame.draw.rect(
                self.screen,
                self.settings.UI_TIMER_BAR_BG_COLOR,
                (
                    ui_timer_x_pos,
                    ui_timer_y_current,
                    self.settings.UI_TIMER_BAR_WIDTH,
                    self.settings.UI_TIMER_BAR_HEIGHT,
                ),
                border_radius=3
            )
            # Current progress of timer bar
            current_bar_width = int(self.settings.UI_TIMER_BAR_WIDTH * percentage_left)
            pygame.draw.rect(
                self.screen,
                self.settings.UI_SLOWMO_TIMER_COLOR,
                (
                    ui_timer_x_pos,
                    ui_timer_y_current,
                    current_bar_width,
                    self.settings.UI_TIMER_BAR_HEIGHT,
                ),
                border_radius=3
            )
            ui_timer_y_current += (
                self.settings.UI_TIMER_BAR_HEIGHT + timer_spacing
            )
        if now < self.timers.shrink_effect_end_tick:
            time_left = self.timers.shrink_effect_end_tick - now
            percentage_left = max(
                0, time_left / self.settings.SHRINK_DURATION_MS
            )
            shrink_label_surf = self.small_font.render(
                self.locale.get_text("shrink"), True, self.settings.UI_SHRINK_TIMER_COLOR
            )
            label_y = (
                ui_timer_y_current
                + (self.settings.UI_TIMER_BAR_HEIGHT - shrink_label_surf.get_height())
                // 2
            )
            self.screen.blit(
                shrink_label_surf,
                (
                    ui_timer_x_pos - shrink_label_surf.get_width() - label_padding,
                    label_y,
                ),
            )
            pygame.draw.rect(
                self.screen,
                self.settings.UI_TIMER_BAR_BG_COLOR,
                (
                    ui_timer_x_pos,
                    ui_timer_y_current,
                    self.settings.UI_TIMER_BAR_WIDTH,
                    self.settings.UI_TIMER_BAR_HEIGHT,
                ),
                border_radius=3
            )
            current_bar_width = int(self.settings.UI_TIMER_BAR_WIDTH * percentage_left)
            pygame.draw.rect(
                self.screen,
                self.settings.UI_SHRINK_TIMER_COLOR,
                (
                    ui_timer_x_pos,
                    ui_timer_y_current,
                    current_bar_width,
                    self.settings.UI_TIMER_BAR_HEIGHT,
                ),
                border_radius=3
            )
            # ui_timer_y_current += timer_spacing # Only increment if another timer follows

        # Pickup Message (e.g., "Shield Activated!")
        if self.effects.pickup_message and now < self.timers.pickup_message_end_tick:
            msg_surface = self.font.render( # Use slightly larger font for messages
                self.effects.pickup_message, True, self.settings.UI_PICKUP_MESSAGE_COLOR
            )
            self.screen.blit(
                msg_surface,
                ( # Centered at bottom of screen
                    self.settings.WIDTH // 2 - msg_surface.get_width() // 2,
                    self.settings.HEIGHT - 60, # Position from bottom
                ),
            )
        elif self.effects.pickup_message: # Message expired
            self.effects.pickup_message = ""

        # Shield Visual Effect around player
        if self.effects.shield:
            pygame.draw.circle(
                self.screen,
                (0, 255, 255, 100),
                self.player.rect.center,
                int(self.player.rect.width * 0.75),
                3,
            )

    def show_pause_or_gameover_screen(self, message, mouse_pos=None):
        # Semi-transparent overlay
        overlay = pygame.Surface((self.settings.WIDTH, self.settings.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) # RGBA, A for alpha
        self.screen.blit(overlay, (0, 0))

        center_x = self.settings.WIDTH // 2
        title_font = pygame.font.SysFont("consolas", 48)
        button_font = self.medium_font # Font for buttons

        # Main Title (PAUSED or GAME OVER)
        main_title_surf = title_font.render(message, True, settings.BRIGHT_WHITE)
        self.screen.blit(
            main_title_surf, (center_x - main_title_surf.get_width() // 2, 80) # Y pos for title
        )

        # Score Display
        score_surf = self.font.render( # Slightly smaller font for score
            self.locale.get_text("your_score", self.score), True, settings.LIGHT_TEXT
        )
        self.screen.blit(score_surf, (center_x - score_surf.get_width() // 2, 160)) # Y pos for score

        # Buttons start Y position
        y_button_start = 240
        button_y = y_button_start
        button_spacing_pause = self.settings.BUTTON_HEIGHT + 20 # Spacing between buttons

        # --- PAUSED State Buttons ---
        if message == self.locale.get_text("paused"):
            # Resume Button
            self.pause_resume_button = pygame.Rect(
                center_x - self.settings.BUTTON_WIDTH // 2, button_y,
                self.settings.BUTTON_WIDTH, self.settings.BUTTON_HEIGHT,
            )
            color = ( # Hover effect
                self.settings.BUTTON_COLOR_HOVER
                if mouse_pos and self.pause_resume_button.collidepoint(mouse_pos)
                else self.settings.BUTTON_COLOR_NORMAL
            )
            pygame.draw.rect(self.screen, color, self.pause_resume_button, border_radius=10)
            draw_text_centered(self.screen, self.locale.get_text("resume"), button_font, self.settings.BUTTON_TEXT_COLOR, self.pause_resume_button)
            button_y += button_spacing_pause

            # Instructions Button
            self.pause_instructions_button = pygame.Rect(
                center_x - self.settings.BUTTON_WIDTH // 2, button_y,
                self.settings.BUTTON_WIDTH, self.settings.BUTTON_HEIGHT,
            )
            color = (
                self.settings.BUTTON_COLOR_HOVER
                if mouse_pos and self.pause_instructions_button.collidepoint(mouse_pos)
                else self.settings.BUTTON_COLOR_NORMAL
            )
            pygame.draw.rect(self.screen, color, self.pause_instructions_button, border_radius=10)
            draw_text_centered(self.screen, self.locale.get_text("instructions_pause"), button_font, self.settings.BUTTON_TEXT_COLOR, self.pause_instructions_button)
            button_y += button_spacing_pause

            # Restart Button
            self.pause_restart_button = pygame.Rect(
                center_x - self.settings.BUTTON_WIDTH // 2, button_y,
                self.settings.BUTTON_WIDTH, self.settings.BUTTON_HEIGHT,
            )
            color = (
                self.settings.BUTTON_COLOR_HOVER
                if mouse_pos and self.pause_restart_button.collidepoint(mouse_pos)
                else self.settings.BUTTON_COLOR_NORMAL
            )
            pygame.draw.rect(self.screen, color, self.pause_restart_button, border_radius=10)
            draw_text_centered(self.screen, self.locale.get_text("restart_pause"), button_font, self.settings.BUTTON_TEXT_COLOR, self.pause_restart_button)
            button_y += button_spacing_pause

            # Main Menu Button
            self.pause_main_menu_button = pygame.Rect(
                center_x - self.settings.BUTTON_WIDTH // 2, button_y,
                self.settings.BUTTON_WIDTH, self.settings.BUTTON_HEIGHT,
            )
            color = (
                self.settings.BUTTON_COLOR_HOVER
                if mouse_pos and self.pause_main_menu_button.collidepoint(mouse_pos)
                else self.settings.BUTTON_COLOR_NORMAL
            )
            pygame.draw.rect(self.screen, color, self.pause_main_menu_button, border_radius=10)
            draw_text_centered(self.screen, self.locale.get_text("main_menu_pause"), button_font, self.settings.BUTTON_TEXT_COLOR, self.pause_main_menu_button)
            # button_y += button_spacing_pause # No more buttons after this for paused state

        # --- GAME OVER State Buttons ---
        elif message == self.locale.get_text("game_over"):
            # Restart Button (Game Over)
            self.game_over_restart_button = pygame.Rect( # Use specific attribute for game over
                center_x - self.settings.BUTTON_WIDTH // 2, button_y,
                self.settings.BUTTON_WIDTH, self.settings.BUTTON_HEIGHT,
            )
            color = (
                self.settings.BUTTON_COLOR_HOVER
                if mouse_pos and self.game_over_restart_button.collidepoint(mouse_pos)
                else self.settings.BUTTON_COLOR_NORMAL
            )
            pygame.draw.rect(self.screen, color, self.game_over_restart_button, border_radius=10)
            draw_text_centered(self.screen, self.locale.get_text("restart_pause"), button_font, self.settings.BUTTON_TEXT_COLOR, self.game_over_restart_button)
            button_y += button_spacing_pause

            # Main Menu Button (Game Over)
            self.game_over_main_menu_button = pygame.Rect( # Use specific attribute
                center_x - self.settings.BUTTON_WIDTH // 2, button_y,
                self.settings.BUTTON_WIDTH, self.settings.BUTTON_HEIGHT,
            )
            color = (
                self.settings.BUTTON_COLOR_HOVER
                if mouse_pos and self.game_over_main_menu_button.collidepoint(mouse_pos)
                else self.settings.BUTTON_COLOR_NORMAL
            )
            pygame.draw.rect(self.screen, color, self.game_over_main_menu_button, border_radius=10)
            draw_text_centered(self.screen, self.locale.get_text("main_menu_pause"), button_font, self.settings.BUTTON_TEXT_COLOR, self.game_over_main_menu_button)
            button_y += button_spacing_pause # Move Y for high scores display

            # Display High Scores on Game Over screen
            draw_high_scores(self.screen, self.small_font, y_start=button_y + 20) # Add some padding