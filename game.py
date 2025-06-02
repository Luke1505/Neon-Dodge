import pygame
from player import Player
from obstacle import Obstacle
from powerups import PowerUp
from utils import get_username, save_high_scores, update_high_scores, get_high_scores, get_high_score_value, WIDTH, HEIGHT

def show_main_menu(screen, username=""):
    font = pygame.font.SysFont("consolas", 36)
    small_font = pygame.font.SysFont("consolas", 22)
    input_font = pygame.font.SysFont("consolas", 28)
    clock = pygame.time.Clock()

    input_box = pygame.Rect(WIDTH // 2 - 100, 280, 200, 36)
    active = False
    running = True

    while running:
        screen.fill((20, 20, 40))
        draw_main_menu_ui(screen, font, small_font, input_font, input_box, username)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = input_box.collidepoint(event.pos)
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        running = False
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        if len(username) < 16:
                            username += event.unicode
                elif event.key == pygame.K_RETURN:
                    running = False

        pygame.display.flip()
        clock.tick(60)

    return username.strip() if username.strip() else "Guest"

def draw_main_menu_ui(screen, font, small_font, input_font, input_box, username):
    title = font.render("NEON DODGE", True, (0, 255, 180))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))

    label = small_font.render("Enter username (optional):", True, (255, 255, 255))
    screen.blit(label, (WIDTH // 2 - label.get_width() // 2, 250))

    pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
    text_surface = input_font.render(username, True, (255, 255, 255))
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

    prompt = small_font.render("Press ENTER to start", True, (255, 255, 255))
    screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 330))

    draw_high_scores(screen, small_font, y_start=390)

def draw_high_scores(screen, font, y_start):
    highscores = get_high_scores()
    highscores.sort(key=lambda x: x["score"], reverse=True)
    y = y_start
    title = font.render("Top 10 Scores", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, y))
    y += 28
    for i, entry in enumerate(highscores[:10]):
        hs_text = font.render(f"{i+1}. {entry['username']}: {entry['score']}", True, (200, 200, 200))
        screen.blit(hs_text, (WIDTH // 2 - hs_text.get_width() // 2, y))
        y += 24

class Game:
    def __init__(self, screen, username, ai_mode=False):
        self.ai_mode = ai_mode
        self.screen = screen
        self.username = username.strip() or "Guest"
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 28)

        self.reset_game_state()

    def reset_game_state(self):
        self.player = Player()
        self.obstacles = []
        self.powerups = []
        self.spawn_timer = 0
        self.powerup_timer = 0
        self.score = 0
        self.high_score = get_high_score_value()

        self.obstacle_speed = 4
        self.shield_active = False
        self.slowmo_active = False
        self.slowmo_timer = 0
        self.shrink_active = False
        self.shrink_timer = 0
        self.bomb_ready = False
        self.pickup_message = ""
        self.pickup_timer = 0
        self.game_over = False
        self.paused = False

    def update_score(self):
        update_high_scores(self.username, self.score)
        self.high_score = get_high_score_value()

    @staticmethod
    def ai_decide_move(player, obstacles):
        # For example, move away from closest obstacle in both x and y
        if not obstacles:
            return 0  # no move
    
        closest = min(obstacles, key=lambda o: (abs(o.rect.centerx - player.x) + abs(o.rect.centery - player.y)))
    
        dx = 0
        dy = 0
    
        if player.x < closest.rect.centerx:
            dx = -1
        elif player.x > closest.rect.centerx:
            dx = 1
    
        if player.y < closest.rect.centery:
            dy = -1
        elif player.y > closest.rect.centery:
            dy = 1
    
        # Choose dominant movement direction (prioritize horizontal or vertical)
        if abs(player.x - closest.rect.centerx) > abs(player.y - closest.rect.centery):
            return 1 if dx > 0 else 2 if dx < 0 else 0
        else:
            return 3 if dy < 0 else 4 if dy > 0 else 0


    def game_loop(self):
        while True:
            self.screen.fill((15, 15, 30))
            dt = self.clock.tick(60)

            self.handle_events()
            if not self.paused and not self.game_over:
                self.update_game_logic()
            self.render_game()
            pygame.display.flip()

    def handle_events(self):
        keys = pygame.key.get_pressed()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_LEFT, pygame.K_RIGHT) and self.paused:
                    self.paused = False
                if e.key == pygame.K_r and self.game_over:
                    new_username = show_main_menu(self.screen, self.username)
                    self.__init__(self.screen, new_username, ai_mode=self.ai_mode)
                if e.key == pygame.K_p and not self.game_over:
                    self.paused = not self.paused

        if not self.ai_mode and not self.paused and not self.game_over:
            self.player.move(keys)

    def update_game_logic(self):
        if self.ai_mode:
            move = self.ai_decide_move(self.player, self.obstacles)
            self.player.ai_move(move)

        self.spawn_timer += 1
        if self.spawn_timer > 60:
            self.obstacles.append(Obstacle(self.obstacle_speed))
            self.spawn_timer = 0
            self.score += 1
            if self.score % 20 == 0:
                self.obstacle_speed = min(self.obstacle_speed + 0.3, 6)

        self.update_effects()
        self.update_obstacles()
        self.update_powerups()

    def update_effects(self):
        now = pygame.time.get_ticks()

        self.player.width = 30 if self.shrink_active and now - self.shrink_timer < 10000 else 60
        self.player.speed = 6 if self.shrink_active and now - self.shrink_timer < 10000 else 8
        self.shrink_active &= now - self.shrink_timer < 10000

        self.slowmo_active &= now - self.slowmo_timer < 5000
        self.speed_multiplier = 0.5 if self.slowmo_active else 1

    def update_obstacles(self):
        for obs in self.obstacles:
            obs.update(self.speed_multiplier)

        for obs in self.obstacles[:]:
            for other in self.obstacles:
                if obs != other and obs.get_rect().colliderect(other.get_rect()):
                    self.obstacles.remove(obs)
                    break

            if self.player.get_rect().colliderect(obs.get_rect()):
                if self.shield_active:
                    self.shield_active = False
                    self.obstacles.remove(obs)
                else:
                    self.game_over = True
                    self.update_score()

        self.obstacles = [o for o in self.obstacles if not o.off_screen()]

    def update_powerups(self):
        self.powerup_timer += 1
        if self.powerup_timer > 300:
            self.powerups.append(PowerUp())
            self.powerup_timer = 0

        for p in self.powerups[:]:
            p.update()
            if p.rect.top > HEIGHT:
                self.powerups.remove(p)
            elif self.player.get_rect().colliderect(p.rect):
                self.handle_powerup_pickup(p)
                self.powerups.remove(p)

    def handle_powerup_pickup(self, powerup):
        self.pickup_timer = pygame.time.get_ticks()
        if powerup.type == "shield":
            self.shield_active = True
            self.pickup_message = "Shield Activated!"
        elif powerup.type == "slowmo":
            self.slowmo_active = True
            self.slowmo_timer = pygame.time.get_ticks()
            self.pickup_message = "Slow Motion!"
        elif powerup.type == "bomb":
            self.bomb_ready = True
            self.obstacles.clear()
            self.pickup_message = "Bomb Activated!"
        elif powerup.type == "shrink":
            self.shrink_active = True
            self.shrink_timer = pygame.time.get_ticks()
            self.pickup_message = "Shrink Activated!"

    def render_game(self):
        self.player.draw(self.screen)
        for obs in self.obstacles:
            obs.draw(self.screen)
        for p in self.powerups:
            p.draw(self.screen)

        self.render_ui()

        if self.paused:
            self.show_pause_or_gameover_screen("PAUSED")
        if self.game_over:
            self.show_pause_or_gameover_screen("GAME OVER")

    def render_ui(self):
        self.screen.blit(self.font.render(f"Player: {self.username}", True, (255, 255, 255)), (10, 10))
        self.screen.blit(self.font.render(f"Score: {self.score}", True, (255, 255, 255)), (10, 40))
        hs_text = self.font.render(f"High Score: {self.high_score}", True, (255, 255, 255))
        self.screen.blit(hs_text, (WIDTH - hs_text.get_width() - 10, 10))

        if self.pickup_message and pygame.time.get_ticks() - self.pickup_timer < 2000:
            msg = self.font.render(self.pickup_message, True, (255, 255, 100))
            self.screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT - 60))

        if self.shield_active:
            pygame.draw.circle(self.screen, (0, 255, 0), self.player.get_rect().center, 60, 2)

    def show_pause_or_gameover_screen(self, message):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        center = WIDTH // 2
        self.screen.blit(self.font.render(message, True, (255, 255, 255)), (center - 80, 160))
        self.screen.blit(self.font.render(f"Your Score: {self.score}", True, (255, 255, 255)), (center - 100, 210))

        prompt = "Press P to Resume" if message == "PAUSED" else "Press R to Restart"
        self.screen.blit(self.font.render(prompt, True, (255, 255, 255)), (center - 100, 250))

        draw_high_scores(self.screen, pygame.font.SysFont("consolas", 22), 320)
