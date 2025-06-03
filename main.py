import pygame
import sys
from game import Game, show_main_menu
from utils import get_username, WIDTH, HEIGHT

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Neon Dodge")
    username = show_main_menu(screen)
    game = Game(screen, username)
    game.game_loop()

if __name__ == "__main__":
    main()