import pygame
import sys # For sys.exit()
# Ensure constants are imported if they are defined in game.py and used for comparison here
from game import Game, show_main_menu, ACTION_QUIT_GAME, ACTION_SHOW_INSTRUCTIONS 
from utils import WIDTH, HEIGHT #

def main():
    pygame.init()
    # pygame.mixer.init() # If you add sounds later, initialize mixer here or early in Game class
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Neon Dodge")
    
    username = "" # Default username, can be updated from menu
    running_application = True

    while running_application:
        # show_main_menu now returns an action string or the username
        menu_action_or_username = show_main_menu(screen, username)

        if menu_action_or_username == ACTION_QUIT_GAME:
            running_application = False # Signal to break the main application loop
        elif menu_action_or_username == ACTION_SHOW_INSTRUCTIONS:
            # Create a Game instance specifically to show instructions
            # The username passed here is a placeholder as it's not critical for viewing instructions
            # The start_state parameter will directly put the game instance into instructions mode
            temp_game_for_instructions = Game(screen, "Player", ai_mode=False, start_state=Game.STATE_INSTRUCTIONS)
            temp_game_for_instructions.run_instructions_loop()
            # After instructions_loop finishes, the main application loop continues, 
            # which will call show_main_menu() again.
        else: 
            # A username was returned (or default "Guest"), so start the game
            username = menu_action_or_username # Update username if it was changed in the menu
            
            # Create and run the game session
            game_session = Game(screen, username, ai_mode=False) # Game starts in STATE_PLAYING by default
            
            # game_loop will run until an explicit exit to menu or quit action is triggered within the game
            session_result = game_session.game_loop() 

            if session_result == ACTION_QUIT_GAME: # If game loop signaled a full application quit
                running_application = False # Signal to break the main application loop
            # If session_result was Game.STATE_EXIT_TO_MENU (or any other value that isn't ACTION_QUIT_GAME),
            # the main application loop continues, effectively returning to show_main_menu().

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()