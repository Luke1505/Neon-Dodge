import json
import os
import pygame
import settings  # Import settings

WIDTH, HEIGHT = settings.WIDTH, settings.HEIGHT  # Use settings for WIDTH, HEIGHT
UI_TEXT_COLOR = settings.MENU_TEXT_COLOR  # Changed from WHITE to UI_TEXT_COLOR from settings
HIGHSCORE_FILE = settings.HIGHSCORE_FILE  # Use settings for HIGHSCORE_FILE


def save_high_scores(highscores):
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump(highscores, f, indent=4)


def get_high_scores():
    if not os.path.exists(HIGHSCORE_FILE):
        return []
    try:
        with open(HIGHSCORE_FILE, "r") as f:
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

    while input_active:
        screen.fill(settings.BACKGROUND_COLOR) # Changed to use BACKGROUND_COLOR from settings

        hint_text = "Enter Username (optional):"
        display_text = font.render(f"{hint_text} {username}", True, UI_TEXT_COLOR) # Changed to UI_TEXT_COLOR
        screen.blit(
            display_text, (WIDTH // 2 - display_text.get_width() // 2, HEIGHT // 2 - 30)
        )

        instruction_text = font.render("Press ENTER to continue", True, UI_TEXT_COLOR) # Changed to UI_TEXT_COLOR
        screen.blit(
            instruction_text,
            (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 + 30),
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