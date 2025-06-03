import pygame
import sys  # For sys.exit()

# Ensure constants are imported if they are defined in game.py and used for comparison here
# Assuming your game.py now includes the updated show_main_menu and other actions
from game import (
    Game,
    show_main_menu,
    ACTION_QUIT_GAME,
    ACTION_SHOW_INSTRUCTIONS,
    ACTION_START_GAME,
    ACTION_BACK_TO_MAIN_MENU,
)
from utils import WIDTH, HEIGHT  #


def main():
    pygame.init()
    # pygame.mixer.init() # If you add sounds later, initialize mixer here or early in Game class
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Neon Dodge")

    username = ""  # Default username, will be updated from menu
    running_application = True

    while running_application:
        # UNPACK THE TUPLE HERE:
        action, updated_username = show_main_menu(
            screen, username
        )  # Receive both action and username

        # ALWAYS update the username with the latest from the menu
        # This ensures that even if an action like "instructions" is returned,
        # the username field's content is preserved for the next time show_main_menu is called.
        username = updated_username

        if action == ACTION_QUIT_GAME:
            running_application = False  # Signal to break the main application loop
        elif action == ACTION_SHOW_INSTRUCTIONS:
            # Create a Game instance specifically to show instructions
            # The username passed here is a placeholder as it's not critical for viewing instructions
            # The start_state parameter will directly put the game instance into instructions mode
            temp_game_for_instructions = Game(
                screen, username, ai_mode=False, start_state=Game.STATE_INSTRUCTIONS
            )
            # The run_instructions_loop should return an action (like BACK_TO_MAIN_MENU or QUIT_GAME)
            instruction_result = temp_game_for_instructions.run_instructions_loop()

            if instruction_result == ACTION_QUIT_GAME:
                running_application = False  # Quit from instructions screen
            # If instruction_result is ACTION_BACK_TO_MAIN_MENU, the loop continues,
            # which will re-call show_main_menu with the preserved 'username'.
            # No 'else' needed here as continuing the loop automatically goes back to the menu.

        elif action == ACTION_START_GAME:  # This condition now checks the action part
            # Game should only start if ACTION_START_GAME is explicitly returned
            print(
                f"Starting game with username: {username}"
            )  # Use the updated username

            # Create and run the game session
            game_session = Game(
                screen, username, ai_mode=False
            )  # Game starts in STATE_PLAYING by default

            # game_loop will run until an explicit exit to menu or quit action is triggered within the game
            session_result = game_session.game_loop()

            if (
                session_result == ACTION_QUIT_GAME
            ):  # If game loop signaled a full application quit
                running_application = False  # Signal to break the main application loop
            # If session_result was Game.STATE_EXIT_TO_MENU (or any other value that isn't ACTION_QUIT_GAME),
            # the main application loop continues, effectively returning to show_main_menu().

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
