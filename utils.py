import json
import os
import pygame
import settings
import sys
# Import _LOCALE_MANAGER_GLOBAL from game.py to access it
from locale_manager import _LOCALE_MANAGER_GLOBAL

WIDTH, HEIGHT = settings.WIDTH, settings.HEIGHT
UI_TEXT_COLOR = settings.MENU_TEXT_COLOR
HIGHSCORE_FILE = settings.HIGHSCORE_FILE

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def save_high_scores(highscores):
    with open(resource_path(HIGHSCORE_FILE), "w") as f:
        json.dump(highscores, f, indent=4)


def get_high_scores():
    if not os.path.exists(resource_path(HIGHSCORE_FILE)):
        return []
    try:
        with open(resource_path(HIGHSCORE_FILE), "r") as f:
            highscores = json.load(f)
            highscores = sorted(highscores, key=lambda x: x["score"], reverse=True)[:10]
            return highscores
    except json.JSONDecodeError:
        return []


def update_high_scores(username, score):
    highscores = get_high_scores()

    highscores.append({"username": username, "score": score})

    highscores.sort(key=lambda x: x["score"], reverse=True)

    save_high_scores(highscores[:10])


def get_high_score_value():
    scores = get_high_scores()
    return scores[0]["score"] if scores else 0


def get_username(screen):
    pygame.font.init()
    font = pygame.font.SysFont("consolas", 32)
    username = ""
    input_active = True
    clock = pygame.time.Clock()

    # Use the global locale manager instance
    locale_manager = _LOCALE_MANAGER_GLOBAL
    if locale_manager is None:
        # Fallback if locale_manager is not yet initialized (e.g., if called outside main menu flow)
        print("Warning: LocaleManager not initialized in get_username. Using default text.")
        hint_text = "Enter Username (optional):"
        instruction_text = "Press ENTER to continue"
    else:
        hint_text = locale_manager.get_text("enter_username") # Translated
        instruction_text = locale_manager.get_text("press_enter_to_continue") # Add this key to your JSON files

    while input_active:
        screen.fill(settings.BACKGROUND_COLOR)

        display_text = font.render(f"{hint_text} {username}", True, UI_TEXT_COLOR)
        screen.blit(
            display_text, (WIDTH // 2 - display_text.get_width() // 2, HEIGHT // 2 - 30)
        )

        instruction_text_surf = font.render(instruction_text, True, UI_TEXT_COLOR)
        screen.blit(
            instruction_text_surf,
            (WIDTH // 2 - instruction_text_surf.get_width() // 2, HEIGHT // 2 + 30),
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username) < 12 and event.unicode.isprintable():
                        username += event.unicode

        clock.tick(30)

    return username.strip()