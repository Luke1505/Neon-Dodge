import json
import os
import pygame
# import settings  # Removed direct import, settings will be passed

# WIDTH, HEIGHT, UI_TEXT_COLOR, HIGHSCORE_FILE will now be accessed via passed game_settings object
# Remove module-level assignments from settings.py

def save_high_scores(highscores, game_settings=None): # Accept game_settings
    # Initialize settings with fallback if not provided
    if game_settings is None:
        import settings as default_settings # Fallback import
        game_settings = default_settings
    with open(game_settings.HIGHSCORE_FILE, "w") as f: # Use game_settings
        json.dump(highscores, f, indent=4)


def get_high_scores(game_settings=None): # Accept game_settings
    # Initialize settings with fallback if not provided
    if game_settings is None:
        import settings as default_settings # Fallback import
        game_settings = default_settings

    if not os.path.exists(game_settings.HIGHSCORE_FILE): # Use game_settings
        return []
    try:
        with open(game_settings.HIGHSCORE_FILE, "r") as f: # Use game_settings
            highscores = json.load(f)
            highscores = sorted(highscores, key=lambda x: x["score"], reverse=True)[:10]
            return highscores
    except json.JSONDecodeError:
        return []


def update_high_scores(username, score, game_settings=None): # Accept game_settings
    # Initialize settings with fallback if not provided
    if game_settings is None:
        import settings as default_settings # Fallback import
        game_settings = default_settings

    highscores = get_high_scores(game_settings=game_settings) # Pass game_settings

    highscores.append({"username": username, "score": score})

    highscores.sort(key=lambda x: x["score"], reverse=True)

    save_high_scores(highscores[:10], game_settings=game_settings) # Pass game_settings


def get_high_score_value(game_settings=None): # Accept game_settings
    # Initialize settings with fallback if not provided
    if game_settings is None:
        import settings as default_settings # Fallback import
        game_settings = default_settings
    scores = get_high_scores(game_settings=game_settings) # Pass game_settings
    return scores[0]["score"] if scores else 0


def get_username(screen, game_settings=None): # Accept game_settings
    # Initialize settings with fallback if not provided
    if game_settings is None:
        import settings as default_settings # Fallback import
        game_settings = default_settings

    pygame.font.init()
    font = pygame.font.SysFont("consolas", 32)
    username = ""
    input_active = True
    clock = pygame.time.Clock()

    while input_active:
        screen.fill(game_settings.BACKGROUND_COLOR) # Changed to use BACKGROUND_COLOR from game_settings

        hint_text = "Enter Username (optional):"
        display_text = font.render(f"{hint_text} {username}", True, game_settings.MENU_TEXT_COLOR) # Changed to game_settings.MENU_TEXT_COLOR
        screen.blit(
            display_text, (game_settings.WIDTH // 2 - display_text.get_width() // 2, game_settings.HEIGHT // 2 - 30) # Use game_settings
        )

        instruction_text = font.render("Press ENTER to continue", True, game_settings.MENU_TEXT_COLOR) # Changed to game_settings.MENU_TEXT_COLOR
        screen.blit(
            instruction_text,
            (game_settings.WIDTH // 2 - instruction_text.get_width() // 2, game_settings.HEIGHT // 2 + 30), # Use game_settings
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