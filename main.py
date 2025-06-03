import pygame
import sys
import os # Import os for resource_path

from game import (
    Game,
    show_main_menu,
    ACTION_QUIT_GAME,
    ACTION_SHOW_INSTRUCTIONS,
    ACTION_START_GAME,
    ACTION_BACK_TO_MAIN_MENU,
)
from utils import WIDTH, HEIGHT
import settings # Import settings to access DEFAULT_LANGUAGE and LOCALE_DIR
from locale_manager import _LOCALE_MANAGER_GLOBAL

# Add the resource_path function here (or import if it's in utils.py)
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main():
    pygame.init()

    # --- Icon Setting ---
    # Load the icon image using resource_path
    # Make sure 'assets/icon.png' is the correct path to your icon file
    # and that 'assets' is included in your PyInstaller --add-data
    try:
        icon_path = resource_path("assets/icon.jpg") # Assuming your icon is named icon.png inside assets
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)
    except pygame.error as e:
        print(f"Error loading icon: {e}")
        print(f"Attempted to load from: {icon_path}")
    except FileNotFoundError:
        print(f"Icon file not found at: {icon_path}")
    # --- End Icon Setting ---

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Neon Dodge")

    username = ""
    running_application = True

    while running_application:
        action, updated_username = show_main_menu(screen, username)
        username = updated_username

        if action == ACTION_QUIT_GAME:
            running_application = False
        elif action == ACTION_SHOW_INSTRUCTIONS:
            temp_game_for_instructions = Game(
                screen, username, ai_mode=False, start_state=Game.STATE_INSTRUCTIONS
            )
            instruction_result = temp_game_for_instructions.run_instructions_loop()

            if instruction_result == ACTION_QUIT_GAME:
                running_application = False

        elif action == ACTION_START_GAME:
            print(f"Starting game with username: {username}")

            game_session = Game(
                screen, username, ai_mode=False
            )
            session_result = game_session.game_loop()

            if session_result == ACTION_QUIT_GAME:
                running_application = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()