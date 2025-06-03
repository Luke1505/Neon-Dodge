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

# --- Flag Drawing Function ---
def draw_simplified_flag(screen, locale_code, rect):
    """Draws a simplified flag using Pygame primitives."""
    border_thickness = 2
    # Background for the flag button
    pygame.draw.rect(screen, settings.ACCENT_DARK_BLUE, rect, border_radius=5)
    # Border for the flag button
    pygame.draw.rect(screen, settings.BUTTON_COLOR_HOVER, rect, border_thickness, border_radius=5)

    flag_x, flag_y, flag_width, flag_height = rect.x + border_thickness, rect.y + border_thickness, rect.width - 2*border_thickness, rect.height - 2*border_thickness

    if locale_code == 'en':
        # Union Jack - simplified: Red cross on blue background
        # Top-left blue section
        pygame.draw.rect(screen, (0, 0, 100), (flag_x, flag_y, flag_width // 2, flag_height // 2))
        # Top-right blue section
        pygame.draw.rect(screen, (0, 0, 100), (flag_x + flag_width // 2, flag_y, flag_width // 2, flag_height // 2))
        # Bottom-left blue section
        pygame.draw.rect(screen, (0, 0, 100), (flag_x, flag_y + flag_height // 2, flag_width // 2, flag_height // 2))
        # Bottom-right blue section
        pygame.draw.rect(screen, (0, 0, 100), (flag_x + flag_width // 2, flag_y + flag_height // 2, flag_width // 2, flag_height // 2))

        # Red cross
        pygame.draw.rect(screen, (200, 0, 0), (flag_x, flag_y + flag_height // 3, flag_width, flag_height // 3)) # Horizontal stripe
        pygame.draw.rect(screen, (200, 0, 0), (flag_x + flag_width // 3, flag_y, flag_width // 3, flag_height)) # Vertical stripe

    elif locale_code == 'de':
        # German Flag: Black, Red, Gold horizontal stripes
        stripe_height = flag_height // 3
        pygame.draw.rect(screen, (0, 0, 0), (flag_x, flag_y, flag_width, stripe_height)) # Black
        pygame.draw.rect(screen, (200, 0, 0), (flag_x, flag_y + stripe_height, flag_width, stripe_height)) # Red
        pygame.draw.rect(screen, (255, 200, 0), (flag_x, flag_y + 2 * stripe_height, flag_width, stripe_height)) # Gold
    else:
        # Fallback for unsupported locales (e.g., just a colored rectangle with text)
        pygame.draw.rect(screen, settings.ACCENT_DARK_BLUE, (flag_x, flag_y, flag_width, flag_height))
        font = pygame.font.SysFont("consolas", 18)
        text_surf = font.render(locale_code.upper(), True, settings.BRIGHT_WHITE)
        screen.blit(text_surf, text_surf.get_rect(center=(rect.centerx, rect.centery)))


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

    # Language selection buttons setup (using drawn flags)
    available_locales = _LOCALE_MANAGER_GLOBAL.get_available_locales()
    flag_button_width = 60 # Adjusted size for drawn flags
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

        mouse_pos = pygame.mouse.get_pos()
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

        # Draw language selection buttons (using draw_simplified_flag)
        for locale_code, flag_rect in language_buttons.items():
            draw_simplified_flag(screen, locale_code, flag_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ACTION_QUIT_GAME, current_username
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    input_box_active = input_box_rect.collidepoint(mouse_pos)
                    if input_box_active:
                        cursor_position = len(current_username)
                    cursor_visible = True
                    last_cursor_toggle = pygame.time.get_ticks()

                    # Check language button clicks
                    for locale_code, flag_rect in language_buttons.items():
                        if flag_rect.collidepoint(mouse_pos):
                            _LOCALE_MANAGER_GLOBAL.set_locale(locale_code)
                            break # Only one language button can be clicked at a time

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
                else:
                    if event.key == pygame.K_ESCAPE:
                        return (
                            ACTION_QUIT_GAME,
                            current_username,
                        )
                    if event.key == pygame.K_i:
                        return (
                            ACTION_SHOW_INSTRUCTIONS,
                            current_username,
                        )
                    if event.key == pygame.K_RETURN:
                        return ACTION_START_GAME, (
                            current_username.strip()
                            if current_username.strip()
                            else _LOCALE_MANAGER_GLOBAL.get_text("guest")
                        )

        pygame.display.flip()
        clock.tick(60)
    return ACTION_QUIT_GAME, current_username


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
            self.username = _LOCALE_MANAGER_GLOBAL.get_text("player")

        self.pause_resume_button = None
        self.pause_instructions_button = None
        self.pause_restart_button = None
        self.pause_main_menu_button = None
        self.instructions_back_button = None

        self.confirm_quit_yes_button = None
        self.confirm_quit_no_button = None
        self.previous_state_on_quit_request = None
        self.quit_context_message = ""

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
        self.previous_state_on_quit_request = self.STATE_PLAYING

    def _update_stars(self):
        for i in range(len(self.stars)):
            star = self.stars[i]
            star[1] += star[2] * self.speed_multiplier
            if star[1] > self.settings.HEIGHT:
                self.stars[i] = [
                    random.randint(0, self.settings.WIDTH),
                    random.randint(-20, -5),
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
                star_data[3],
                (star_data[0], star_data[1], star_data[4], star_data[4]),
            )

    def update_score(self):
        update_high_scores(self.username, self.score)
        self.high_score = get_high_score_value()

    @staticmethod
    def ai_decide_move(player, obstacles_group):
        if not obstacles_group:
            return 0
        closest = None
        min_dist = float("inf")
        for obs in obstacles_group:
            dist = abs(obs.rect.centerx - player.rect.x) + abs(
                obs.rect.centery - player.rect.y
            )
            if dist < min_dist:
                min_dist = dist
                closest = obs
        if not closest:
            return 0
            dx = 0
            dy = 0
        if player.rect.x < closest.rect.centerx:
            dx = -1
        elif player.rect.x > closest.rect.centerx:
            dx = 1
        if player.rect.y < closest.rect.centery:
            dy = -1
        elif player.rect.y > closest.rect.centery:
            dy = 1
        if abs(player.rect.x - closest.rect.centerx) > abs(
            player.rect.y - closest.rect.centery
        ):
            return 1 if dx > 0 else 2 if dx < 0 else 0
        else:
            return 3 if dy < 0 else 4 if dy > 0 else 0

    def run_instructions_loop(self):
        self.current_state = self.STATE_INSTRUCTIONS
        instructions_running = True
        back_button_rect = pygame.Rect(
            self.settings.WIDTH // 2 - self.settings.BUTTON_WIDTH // 2,
            self.settings.HEIGHT - 100,
            self.settings.BUTTON_WIDTH,
            self.settings.BUTTON_HEIGHT,
        )
        while instructions_running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.K_ESCAPE or event.type == pygame.K_p or event.type == pygame.K_i:
                    instructions_running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and back_button_rect.collidepoint(mouse_pos):
                        instructions_running = False
            self.screen.fill(self.settings.BACKGROUND_COLOR)
            self._draw_stars()
            self.render_instructions_screen(mouse_pos, back_button_rect)
            pygame.display.flip()
            self.clock.tick(30)

    def game_loop(self):
        while self.current_state not in [self.STATE_EXIT_TO_MENU, ACTION_QUIT_GAME]:
            self.screen.fill(self.settings.BACKGROUND_COLOR)
            self.handle_events()
            if self.current_state == self.STATE_PLAYING:
                self.update_game_logic()
            self.render_game()
            pygame.display.flip()
            self.clock.tick(60)
        if self.current_state == self.STATE_EXIT_TO_MENU:
            return self.STATE_EXIT_TO_MENU
        return ACTION_QUIT_GAME

    def handle_events(self):
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.previous_state_on_quit_request = self.current_state
                self.quit_context_message = self.locale.get_text("quit_game_prompt")
                self.current_state = self.STATE_CONFIRM_QUIT
                return

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self.current_state == self.STATE_PAUSED:
                    if (
                        self.pause_resume_button
                        and self.pause_resume_button.collidepoint(mouse_pos)
                    ):
                        self.current_state = self.STATE_PLAYING
                    elif (
                        self.pause_instructions_button
                        and self.pause_instructions_button.collidepoint(mouse_pos)
                    ):
                        self.current_state = self.STATE_INSTRUCTIONS
                    elif (
                        self.pause_restart_button
                        and self.pause_restart_button.collidepoint(mouse_pos)
                    ):
                        self.previous_state_on_quit_request = self.STATE_PAUSED
                        self.quit_context_message = self.locale.get_text("restart_main_menu_prompt")
                        self.current_state = self.STATE_CONFIRM_QUIT
                    elif (
                        self.pause_main_menu_button
                        and self.pause_main_menu_button.collidepoint(mouse_pos)
                    ):
                        self.previous_state_on_quit_request = self.STATE_PAUSED
                        self.quit_context_message = self.locale.get_text("quit_main_menu_prompt")
                        self.current_state = self.STATE_CONFIRM_QUIT
                elif self.current_state == self.STATE_INSTRUCTIONS:
                    if (
                        self.instructions_back_button
                        and self.instructions_back_button.collidepoint(mouse_pos)
                    ):
                        self.current_state = self.STATE_PAUSED
                elif self.current_state == self.STATE_CONFIRM_QUIT:
                    if (
                        self.confirm_quit_yes_button
                        and self.confirm_quit_yes_button.collidepoint(mouse_pos)
                    ):
                        if self.quit_context_message == self.locale.get_text("quit_game_prompt"):
                            self.current_state = ACTION_QUIT_GAME
                        else:
                            self.current_state = self.STATE_EXIT_TO_MENU
                    elif (
                        self.confirm_quit_no_button
                        and self.confirm_quit_no_button.collidepoint(mouse_pos)
                    ):
                        self.current_state = self.previous_state_on_quit_request

            if e.type == pygame.KEYDOWN:
                if self.current_state == self.STATE_PLAYING:
                    if e.key == pygame.K_p:
                        self.current_state = self.STATE_PAUSED
                    elif e.key == pygame.K_ESCAPE:
                        self.previous_state_on_quit_request = self.STATE_PLAYING
                        self.quit_context_message = self.locale.get_text("go_to_pause_menu_prompt")
                        self.current_state = self.STATE_CONFIRM_QUIT
                elif self.current_state == self.STATE_PAUSED:
                    if e.key == pygame.K_p:
                        self.current_state = self.STATE_PLAYING
                    elif e.key == pygame.K_i:
                        self.current_state = self.STATE_INSTRUCTIONS
                    elif e.key == pygame.K_ESCAPE:
                        self.previous_state_on_quit_request = self.STATE_PAUSED
                        self.quit_context_message = self.locale.get_text("quit_main_menu_prompt")
                        self.current_state = self.STATE_CONFIRM_QUIT
                    elif e.key == pygame.K_r:
                        self.previous_state_on_quit_request = self.STATE_PAUSED
                        self.quit_context_message = self.locale.get_text("restart_main_menu_prompt")
                        self.current_state = self.STATE_CONFIRM_QUIT
                elif self.current_state == self.STATE_GAME_OVER:
                    if e.key == pygame.K_r:
                        self.previous_state_on_quit_request = self.STATE_GAME_OVER
                        self.quit_context_message = self.locale.get_text("restart_main_menu_prompt")
                        self.current_state = self.STATE_CONFIRM_QUIT
                    elif e.key == pygame.K_ESCAPE:
                        self.previous_state_on_quit_request = self.STATE_GAME_OVER
                        self.quit_context_message = self.locale.get_text("quit_main_menu_prompt")
                        self.current_state = self.STATE_CONFIRM_QUIT
                elif self.current_state == self.STATE_INSTRUCTIONS:
                    if (
                        e.key == pygame.K_p
                        or e.key == pygame.K_ESCAPE
                        or e.key == pygame.K_i
                    ):
                        self.current_state = self.STATE_PAUSED
                elif self.current_state == self.STATE_CONFIRM_QUIT:
                    if e.key == pygame.K_y:
                        if self.quit_context_message == self.locale.get_text("quit_game_prompt"):
                            self.current_state = ACTION_QUIT_GAME
                        else:
                            self.current_state = self.STATE_EXIT_TO_MENU
                    elif e.key == pygame.K_n:
                        self.current_state = self.previous_state_on_quit_request

        if not self.ai_mode and self.current_state == self.STATE_PLAYING:
            self.player.move(keys)

    def update_game_logic(self):
        now = pygame.time.get_ticks()
        if self.ai_mode:
            pass
        self._update_stars()
        self.timers.spawn_obstacle += 1
        current_spawn_interval = (
            self.settings.BASE_OBSTACLE_SPAWN_INTERVAL
        )
        if self.settings.SCORE_TO_REACH_MIN_INTERVAL > 0:
            if self.score >= self.settings.SCORE_TO_REACH_MIN_INTERVAL:
                current_spawn_interval = (
                    self.settings.MIN_OBSTACLE_SPAWN_INTERVAL
                )
            else:
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
        )
        if self.timers.spawn_obstacle > current_spawn_interval:
            self.timers.spawn_obstacle = 0
            new_obstacle = None
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
            self.score += 1
            if (
                self.score > 0
                and self.score % self.settings.OBSTACLE_SPEED_INCREASE_INTERVAL == 0
                and self.obstacle_speed < self.settings.MAX_OBSTACLE_SPEED
            ):
                if (self.score // self.settings.OBSTACLE_SPEED_INCREASE_INTERVAL) > (
                    (self.score - 1) // self.settings.OBSTACLE_SPEED_INCREASE_INTERVAL
                ):
                    self.obstacle_speed = min(
                        self.obstacle_speed
                        + self.settings.OBSTACLE_SPEED_INCREASE_AMOUNT,
                        self.settings.MAX_OBSTACLE_SPEED,
                    )
        self.update_powerups()
        self.update_effects(now)
        if self.companion:
            if now < self.timers.companion_active_end_tick:
                new_bullets = self.companion.update(self.player.rect)
                if new_bullets:
                    self.companion_bullets.add(new_bullets)
            else:
                self.companion = None
        self.companion_bullets.update()
        self.obstacles.update(self.speed_multiplier)
        self.powerups.update()
        self.particles.update()
        self.check_collisions(now)

    def update_effects(self, now):
        is_shrink_active = now < self.timers.shrink_effect_end_tick
        is_slowmo_active = now < self.timers.slowmo_effect_end_tick

        new_width = 30 if is_shrink_active else self.player.original_width
        new_height = 15 if is_shrink_active else self.player.original_height

        if self.player.width != new_width or self.player.height != new_height:
            self.player.width = new_width
            self.player.height = new_height
            self.player.update_visuals()

        self.player.speed = (
            6 if is_shrink_active else self.settings.PLAYER_SPEED
        )
        self.speed_multiplier = 0.5 if is_slowmo_active else 1.0

        if self.effects.pickup_message and now >= self.timers.pickup_message_end_tick:
            self.effects.pickup_message = ""

    def check_collisions(self, now):
        collided_obs_player = pygame.sprite.spritecollide(
            self.player, self.obstacles, False
        )
        if collided_obs_player:
            is_player_invincible = now < self.timers.player_invincible_end_tick
            if not is_player_invincible:
                for obs in collided_obs_player:
                    if self.effects.shield:
                        self.effects.shield = False
                        self._create_explosion(obs.rect.center, obs.color)
                        obs.kill()
                        self.effects.pickup_message = self.locale.get_text("shield_lost")
                        self.timers.pickup_message_end_tick = (
                            now + self.settings.PICKUP_MESSAGE_DURATION_MS
                        )
                    else:
                        self.lives -= 1
                        self._create_explosion(obs.rect.center, obs.color)
                        obs.kill()
                        if self.lives <= 0:
                            self.current_state = self.STATE_GAME_OVER
                            self.update_score()
                            break
                        else:
                            self.timers.player_invincible_end_tick = (
                                now + self.settings.PLAYER_INVINCIBILITY_DURATION_MS
                            )
                            self.effects.pickup_message = self.locale.get_text("life_lost", self.lives)
                            self.timers.pickup_message_end_tick = (
                                now + self.settings.PICKUP_MESSAGE_DURATION_MS
                            )
            elif collided_obs_player:
                for obs in collided_obs_player:
                    self._create_explosion(obs.rect.center, obs.color)
                    obs.kill()
        bullet_hits = pygame.sprite.groupcollide(
            self.companion_bullets, self.obstacles, True, False
        )
        for bullet, hit_obs_list in bullet_hits.items():
            for obs in hit_obs_list:
                self.score += 1
                self._create_explosion(obs.rect.center, obs.color)
                obs.kill()
        collided_powerups_player = pygame.sprite.spritecollide(
            self.player, self.powerups, True
        )
        for p_up in collided_powerups_player:
            self.handle_powerup_pickup(p_up, now)

    def update_powerups(self):
        self.timers.spawn_powerup += 1
        if self.timers.spawn_powerup > self.settings.POWERUP_SPAWN_INTERVAL:
            self.powerups.add(PowerUp(game_settings=self.settings))
            self.timers.spawn_powerup = 0

    def handle_powerup_pickup(self, powerup, current_tick):
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
            for obs in list(self.obstacles.sprites()):
                self._create_explosion(
                    obs.rect.center,
                    obs.color,
                    num_particles=self.settings.PARTICLES_PER_OBSTACLE_EXPLOSION // 2,
                )
                if (
                    hasattr(obs, "can_split")
                    and obs.can_split
                    and hasattr(obs, "get_split_pieces")
                ):
                    pieces = obs.get_split_pieces()
                    newly_split_obstacles.extend(pieces)
                obs.kill()
            self.obstacles.add(newly_split_obstacles)
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
        overlay = pygame.Surface((self.settings.WIDTH, self.settings.HEIGHT))
        overlay.set_alpha(230)
        overlay.fill((15, 15, 35))
        self.screen.blit(overlay, (0, 0))

        y_offset = 60
        title_surf = self.large_font.render(
            self.locale.get_text("instructions"), True, self.settings.MENU_TITLE_COLOR
        )
        self.screen.blit(
            title_surf,
            (self.settings.WIDTH // 2 - title_surf.get_width() // 2, y_offset),
        )
        y_offset += title_surf.get_height() + 30

        instructions_content_start_y = y_offset
        instructions_content_width = self.settings.WIDTH * 0.8 # 80% of screen width
        instructions_content_x = (self.settings.WIDTH - instructions_content_width) // 2

        instructions = [
            (self.locale.get_text("controls_title"), True),
            (self.locale.get_text("controls_move"), False),
            (self.locale.get_text("controls_pause"), False),
            (self.locale.get_text("controls_instructions"), False),
            (self.locale.get_text("controls_escape"), False),
            ("", False),
            (self.locale.get_text("objective_title"), True),
            (self.locale.get_text("objective_dodge"), False),
            (self.locale.get_text("objective_collect"), False),
            ("", False),
            (self.locale.get_text("powerups_title"), True),
            (self.locale.get_text("powerup_shield"), False),
            (self.locale.get_text("powerup_slowmo"), False),
            (self.locale.get_text("powerup_bomb"), False),
            (self.locale.get_text("powerup_shrink"), False),
            (self.locale.get_text("powerup_extralife"), False),
            (self.locale.get_text("powerup_turret"), False),
        ]

        # Calculate total height needed for all instructions to determine max available height per line
        # This is a bit tricky for dynamic fonts, a simpler approach is to give each line max available width.
        # However, if you want all text to shrink to fit a *total* height, you'd need to pre-calculate.
        # For simplicity here, we'll ensure each line fits its *width* and then adjust overall Y positioning.

        # Determine the maximum available height for the instruction content area
        # This assumes the back button position is fixed or calculated beforehand.
        back_button_temp_rect = pygame.Rect(
            self.settings.WIDTH // 2 - self.settings.BUTTON_WIDTH // 2,
            self.settings.HEIGHT - self.settings.BUTTON_HEIGHT - 40,
            self.settings.BUTTON_WIDTH,
            self.settings.BUTTON_HEIGHT,
        )
        max_instructions_content_height = back_button_temp_rect.top - instructions_content_start_y - 20 # 20px padding

        # We'll calculate the actual height used as we render
        current_y_for_text = y_offset

        for text, is_title in instructions:
            if is_title:
                # For titles, aim for a slightly larger font but still fit within the width
                max_line_width = instructions_content_width
                max_line_height = self.font.get_height() + 8 # Initial guess
                font = get_fitted_font(text, 30, max_line_width, max_line_height, "consolas")
                text_surf = font.render(text, True, (220, 220, 255))
                current_y_for_text += 10 # Add some padding before a new title
            else:
                # For regular text, aim for the small font size but fit within the width
                max_line_width = instructions_content_width
                max_line_height = self.small_font.get_height() + 5 # Initial guess
                font = get_fitted_font(text, 20, max_line_width, max_line_height, "consolas")
                text_surf = font.render(text, True, (200, 200, 200))

            # If the text surface is wider than the available width, center it within the instruction content area
            # Otherwise, just center it on the screen.
            text_x_position = instructions_content_x + (instructions_content_width - text_surf.get_width()) // 2
            self.screen.blit(text_surf, (text_x_position, current_y_for_text))
            current_y_for_text += text_surf.get_height() + 5 # Small padding between lines

        # Adjust y_offset for the back button based on where the text rendering ended
        final_button_y = max(current_y_for_text + 20, self.settings.HEIGHT - self.settings.BUTTON_HEIGHT - 40) # Ensure button is not too high
        cbbr = (
            back_button_override_rect
            if back_button_override_rect
            else pygame.Rect(
                self.settings.WIDTH // 2 - self.settings.BUTTON_WIDTH // 2,
                final_button_y,
                self.settings.BUTTON_WIDTH,
                self.settings.BUTTON_HEIGHT,
            )
        )
        self.instructions_back_button = cbbr # Update the class member
        # ... rest of the button drawing remains the same ...
        bc = self.settings.BUTTON_COLOR_NORMAL
        if mouse_pos and cbbr.collidepoint(mouse_pos):
            bc = self.settings.BUTTON_COLOR_HOVER
        pygame.draw.rect(self.screen, bc, cbbr, border_radius=10)
        draw_text_centered(
            self.screen,
            self.locale.get_text("back_button"),
            self.medium_font,
            self.settings.BUTTON_TEXT_COLOR,
            cbbr,
        )

    def render_confirm_quit_screen(self, mouse_pos=None):
        overlay = pygame.Surface((self.settings.WIDTH, self.settings.HEIGHT))
        overlay.set_alpha(230)
        overlay.fill((10, 10, 20))
        self.screen.blit(overlay, (0, 0))
        dialog_width = self.settings.WIDTH * 0.7
        dialog_height = self.settings.HEIGHT * 0.4
        dialog_x = self.settings.WIDTH // 2 - dialog_width // 2
        dialog_y = self.settings.HEIGHT // 2 - dialog_height // 2
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        pygame.draw.rect(self.screen, (30, 30, 50), dialog_rect, border_radius=15)
        pygame.draw.rect(
            self.screen,
            self.settings.MENU_TITLE_COLOR,
            dialog_rect,
            3,
            border_radius=15,
        )
        title_surf = self.large_font.render(
            self.locale.get_text("confirm_exit"), True, self.settings.MENU_TEXT_COLOR
        )
        self.screen.blit(
            title_surf,
            (dialog_rect.centerx - title_surf.get_width() // 2, dialog_rect.top + 30),
        )
        query_surf = self.font.render(
            self.quit_context_message, True, self.settings.MENU_SUBTEXT_COLOR
        )
        self.screen.blit(
            query_surf,
            (dialog_rect.centerx - query_surf.get_width() // 2, dialog_rect.top + 90),
        )
        button_w, button_h = 120, self.settings.BUTTON_HEIGHT
        gap = 30
        total_buttons_width = button_w * 2 + gap
        self.confirm_quit_yes_button = pygame.Rect(
            dialog_rect.centerx - total_buttons_width // 2,
            dialog_rect.bottom - button_h - 40,
            button_w,
            button_h,
        )
        self.confirm_quit_no_button = pygame.Rect(
            self.confirm_quit_yes_button.right + gap,
            self.confirm_quit_yes_button.top,
            button_w,
            button_h,
        )
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
        now = pygame.time.get_ticks()
        self._draw_stars()
        mouse_pos = pygame.mouse.get_pos()
        if (
            self.current_state == self.STATE_PLAYING
            or self.current_state == self.STATE_PAUSED
        ):
            is_player_invincible_visual = now < self.timers.player_invincible_end_tick
            if is_player_invincible_visual and (now // 100) % 2 == 0:
                pass
            else:
                self.player.draw(self.screen)
            self.obstacles.draw(self.screen)
            self.powerups.draw(self.screen)
            if self.companion:
                self.companion.draw(self.screen)
            self.companion_bullets.draw(self.screen)
            self.particles.draw(self.screen)
        self.render_ui(now)
        if self.current_state == self.STATE_PAUSED:
            self.show_pause_or_gameover_screen(self.locale.get_text("paused"), mouse_pos)
        elif self.current_state == self.STATE_GAME_OVER:
            self.show_pause_or_gameover_screen(self.locale.get_text("game_over"), mouse_pos)
        elif self.current_state == self.STATE_INSTRUCTIONS:
            self.render_instructions_screen(mouse_pos)
        elif self.current_state == self.STATE_CONFIRM_QUIT:
            self.render_confirm_quit_screen(mouse_pos)

    def render_ui(self, now):
        self.screen.blit(
            self.font.render(self.locale.get_text("player_score", self.username), True, (255, 255, 255)),
            (10, 10),
        )
        self.screen.blit(
            self.font.render(self.locale.get_text("score", self.score), True, (255, 255, 255)), (10, 40)
        )
        self.screen.blit(
            self.font.render(self.locale.get_text("lives", self.lives), True, (255, 255, 255)), (10, 70)
        )
        hs_text_surf = self.font.render(
            self.locale.get_text("high_score", self.high_score), True, (255, 255, 255)
        )
        self.screen.blit(
            hs_text_surf, (self.settings.WIDTH - hs_text_surf.get_width() - 10, 10)
        )
        ui_timer_y_current = 40
        ui_timer_x_pos = self.settings.WIDTH - self.settings.UI_TIMER_BAR_WIDTH - 10
        label_padding = 5
        timer_spacing = 15
        if self.companion and now < self.timers.companion_active_end_tick:
            time_left_turret = (self.timers.companion_active_end_tick - now) / 1000
            turret_timer_text_surf = self.small_font.render(
                self.locale.get_text("turret_active", time_left_turret), True, (200, 200, 200)
            )
            self.screen.blit(
                turret_timer_text_surf,
                (
                    self.settings.WIDTH - turret_timer_text_surf.get_width() - 10,
                    ui_timer_y_current,
                ),
            )
            ui_timer_y_current += turret_timer_text_surf.get_height() + (
                timer_spacing // 2
            )
        if now < self.timers.slowmo_effect_end_tick:
            time_left = self.timers.slowmo_effect_end_tick - now
            percentage_left = max(
                0, time_left / self.settings.SLOWMO_DURATION_MS
            )
            slowmo_label_surf = self.small_font.render(
                self.locale.get_text("slowmo"), True, self.settings.UI_SLOWMO_TIMER_COLOR
            )
            label_y = (
                ui_timer_y_current
                + (self.settings.UI_TIMER_BAR_HEIGHT - slowmo_label_surf.get_height())
                // 2
            )
            self.screen.blit(
                slowmo_label_surf,
                (
                    ui_timer_x_pos - slowmo_label_surf.get_width() - label_padding,
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
            )
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
            )
        if self.effects.pickup_message and now < self.timers.pickup_message_end_tick:
            msg_surface = self.font.render(
                self.effects.pickup_message, True, self.settings.UI_PICKUP_MESSAGE_COLOR
            )
            self.screen.blit(
                msg_surface,
                (
                    self.settings.WIDTH // 2 - msg_surface.get_width() // 2,
                    self.settings.HEIGHT - 60,
                ),
            )
        elif self.effects.pickup_message:
            self.effects.pickup_message = ""
        if self.effects.shield:
            pygame.draw.circle(
                self.screen,
                (0, 255, 255, 100),
                self.player.rect.center,
                int(self.player.rect.width * 0.75),
                3,
            )

    def show_pause_or_gameover_screen(self, message, mouse_pos=None):
        overlay = pygame.Surface((self.settings.WIDTH, self.settings.HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        center_x = self.settings.WIDTH // 2
        title_font = pygame.font.SysFont("consolas", 48)
        button_font = self.medium_font
        main_title_surf = title_font.render(message, True, (255, 255, 255))
        self.screen.blit(
            main_title_surf, (center_x - main_title_surf.get_width() // 2, 20)
        )
        if message != self.locale.get_text("game_over"):
            score_surf = self.font.render(
                self.locale.get_text("your_score", self.score), True, (255, 255, 255)
            )
            self.screen.blit(score_surf, (center_x - score_surf.get_width() // 2, 120))
            y_button_start = 220
        else:
            score_surf = self.font.render(
                self.locale.get_text("your_score", self.score), True, (255, 255, 255)
            )
            self.screen.blit(score_surf, (center_x - score_surf.get_width() // 2, 120))
            y_button_start = 220
        button_y = y_button_start + 30
        button_spacing_pause = self.settings.BUTTON_HEIGHT + 15
        if message == self.locale.get_text("paused"):
            self.pause_resume_button = pygame.Rect(
                center_x - self.settings.BUTTON_WIDTH // 2,
                button_y,
                self.settings.BUTTON_WIDTH,
                self.settings.BUTTON_HEIGHT,
            )
            color = (
                self.settings.BUTTON_COLOR_HOVER
                if mouse_pos and self.pause_resume_button.collidepoint(mouse_pos)
                else self.settings.BUTTON_COLOR_NORMAL
            )
            pygame.draw.rect(
                self.screen, color, self.pause_resume_button, border_radius=10
            )
            draw_text_centered(
                self.screen,
                self.locale.get_text("resume"),
                button_font,
                self.settings.BUTTON_TEXT_COLOR,
                self.pause_resume_button,
            )
            button_y += button_spacing_pause
            self.pause_instructions_button = pygame.Rect(
                center_x - self.settings.BUTTON_WIDTH // 2,
                button_y,
                self.settings.BUTTON_WIDTH,
                self.settings.BUTTON_HEIGHT,
            )
            color = (
                self.settings.BUTTON_COLOR_HOVER
                if mouse_pos and self.pause_instructions_button.collidepoint(mouse_pos)
                else self.settings.BUTTON_COLOR_NORMAL
            )
            pygame.draw.rect(
                self.screen, color, self.pause_instructions_button, border_radius=10
            )
            draw_text_centered(
                self.screen,
                self.locale.get_text("instructions_pause"),
                button_font,
                self.settings.BUTTON_TEXT_COLOR,
                self.pause_instructions_button,
            )
            button_y += button_spacing_pause
            self.pause_restart_button = pygame.Rect(
                center_x - self.settings.BUTTON_WIDTH // 2,
                button_y,
                self.settings.BUTTON_WIDTH,
                self.settings.BUTTON_HEIGHT,
            )
            color = (
                self.settings.BUTTON_COLOR_HOVER
                if mouse_pos and self.pause_restart_button.collidepoint(mouse_pos)
                else self.settings.BUTTON_COLOR_NORMAL
            )
            pygame.draw.rect(
                self.screen, color, self.pause_restart_button, border_radius=10
            )
            draw_text_centered(
                self.screen,
                self.locale.get_text("restart_pause"),
                button_font,
                self.settings.BUTTON_TEXT_COLOR,
                self.pause_restart_button,
            )
            button_y += button_spacing_pause
            self.pause_main_menu_button = pygame.Rect(
                center_x - self.settings.BUTTON_WIDTH // 2,
                button_y,
                self.settings.BUTTON_WIDTH,
                self.settings.BUTTON_HEIGHT,
            )
            color = (
                self.settings.BUTTON_COLOR_HOVER
                if mouse_pos and self.pause_main_menu_button.collidepoint(mouse_pos)
                else self.settings.BUTTON_COLOR_NORMAL
            )
            pygame.draw.rect(
                self.screen, color, self.pause_main_menu_button, border_radius=10
            )
            draw_text_centered(
                self.screen,
                self.locale.get_text("main_menu_pause"),
                button_font,
                self.settings.BUTTON_TEXT_COLOR,
                self.pause_main_menu_button,
            )
            button_y += button_spacing_pause
        elif message == self.locale.get_text("game_over"):
            self.pause_restart_button = pygame.Rect(
                center_x - self.settings.BUTTON_WIDTH // 2,
                button_y,
                self.settings.BUTTON_WIDTH,
                self.settings.BUTTON_HEIGHT,
            )
            color = (
                self.settings.BUTTON_COLOR_HOVER
                if mouse_pos and self.pause_restart_button.collidepoint(mouse_pos)
                else self.settings.BUTTON_COLOR_NORMAL
            )
            pygame.draw.rect(
                self.screen, color, self.pause_restart_button, border_radius=10
            )
            draw_text_centered(
                self.screen,
                self.locale.get_text("restart_pause"),
                button_font,
                self.settings.BUTTON_TEXT_COLOR,
                self.pause_restart_button,
            )
            button_y += button_spacing_pause
            self.pause_main_menu_button = pygame.Rect(
                center_x - self.settings.BUTTON_WIDTH // 2,
                button_y,
                self.settings.BUTTON_WIDTH,
                self.settings.BUTTON_HEIGHT,
            )
            color = (
                self.settings.BUTTON_COLOR_HOVER
                if mouse_pos and self.pause_main_menu_button.collidepoint(mouse_pos)
                else self.settings.BUTTON_COLOR_NORMAL
            )
            pygame.draw.rect(
                self.screen, color, self.pause_main_menu_button, border_radius=10
            )
            draw_text_centered(
                self.screen,
                self.locale.get_text("main_menu_pause"),
                button_font,
                self.settings.BUTTON_TEXT_COLOR,
                self.pause_main_menu_button,
            )
            button_y += button_spacing_pause
        if message == self.locale.get_text("game_over") or message == self.locale.get_text("paused"):
            draw_high_scores(self.screen, self.small_font, y_start=button_y + 10)