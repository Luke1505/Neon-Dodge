import pygame
from player import Player #
from obstacle import Obstacle #
from powerups import PowerUp #
from utils import get_username, save_high_scores, update_high_scores, get_high_scores, get_high_score_value, WIDTH, HEIGHT #
from bullet import Bullet 
from companion import Companion 
from dataclasses import dataclass, field

# --- Constants for timed effects ---
SHRINK_DURATION_MS = 10000
SLOWMO_DURATION_MS = 5000
PICKUP_MESSAGE_DURATION_MS = 2000
PLAYER_INVINCIBILITY_DURATION_MS = 1500
COMPANION_DURATION_MS = 10000 
# ---

# --- Dataclasses for Game State Organization ---
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

@dataclass
class GameRunState:
    is_over: bool = False
    is_paused: bool = False
# ---

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
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.MOUSEBUTTONDOWN: active = input_box.collidepoint(event.pos)
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN: running = False
                    elif event.key == pygame.K_BACKSPACE: username = username[:-1]
                    else:
                        if len(username) < 16: username += event.unicode
                elif event.key == pygame.K_RETURN: running = False
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
    highscores = get_high_scores() #
    highscores.sort(key=lambda x: x["score"], reverse=True)
    y = y_start
    title = font.render("Top 10 Scores", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, y)); y += 28
    for i, entry in enumerate(highscores[:10]):
        hs_text = font.render(f"{i+1}. {entry['username']}: {entry['score']}", True, (200, 200, 200))
        screen.blit(hs_text, (WIDTH // 2 - hs_text.get_width() // 2, y)); y += 24

class Game:
    INITIAL_LIVES = 3
    def __init__(self, screen, username, ai_mode=False):
        self.ai_mode = ai_mode
        self.screen = screen
        self.username = username.strip() or "Guest"
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 28)
        self.small_font = pygame.font.SysFont("consolas", 22)
        self.reset_game_state()

    def reset_game_state(self):
        self.player = Player() #
        self.obstacles = pygame.sprite.Group() 
        self.powerups = pygame.sprite.Group()  
        
        self.score = 0
        self.high_score = get_high_score_value() #
        self.obstacle_speed = 4
        self.speed_multiplier = 1.0
        self.lives = self.INITIAL_LIVES

        self.timers = GameTimers()
        self.effects = ActiveEffects()
        self.run_state = GameRunState()

        self.companion = None 
        self.companion_bullets = pygame.sprite.Group() 

    def update_score(self):
        update_high_scores(self.username, self.score) #
        self.high_score = get_high_score_value() #

    @staticmethod
    def ai_decide_move(player, obstacles_group): 
        if not obstacles_group: return 0
        closest = None
        min_dist = float('inf')
        for obs in obstacles_group:
            dist = abs(obs.rect.centerx - player.rect.x) + abs(obs.rect.centery - player.rect.y) # Use player.rect.x/y
            if dist < min_dist:
                min_dist = dist
                closest = obs
        if not closest: return 0
        dx=0; dy=0
        if player.rect.x < closest.rect.centerx: dx = -1 # Use player.rect.x/y
        elif player.rect.x > closest.rect.centerx: dx = 1
        if player.rect.y < closest.rect.centery: dy = -1
        elif player.rect.y > closest.rect.centery: dy = 1
        if abs(player.rect.x - closest.rect.centerx) > abs(player.rect.y - closest.rect.centery):
            return 1 if dx > 0 else 2 if dx < 0 else 0
        else:
            return 3 if dy < 0 else 4 if dy > 0 else 0

    def game_loop(self):
        while True:
            self.screen.fill((15, 15, 30))
            self.handle_events()
            if not self.run_state.is_paused and not self.run_state.is_over:
                self.update_game_logic()
            self.render_game()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_events(self):
        keys = pygame.key.get_pressed()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); exit()
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_LEFT,pygame.K_RIGHT,pygame.K_a,pygame.K_d,pygame.K_w,pygame.K_s,pygame.K_UP,pygame.K_DOWN) and self.run_state.is_paused : self.run_state.is_paused = False
                if e.key == pygame.K_r and self.run_state.is_over:
                    new_username = show_main_menu(self.screen, self.username)
                    self.__init__(self.screen, new_username, ai_mode=self.ai_mode)
                if e.key == pygame.K_p and not self.run_state.is_over:
                    self.run_state.is_paused = not self.run_state.is_paused
        if not self.ai_mode and not self.run_state.is_paused and not self.run_state.is_over:
            self.player.move(keys)

    def update_game_logic(self):
        now = pygame.time.get_ticks()
        if self.ai_mode:
            move = self.ai_decide_move(self.player, self.obstacles)
            # self.player.ai_move(move) # Make sure player object has this method or adapt

        # Obstacle Spawning
        self.timers.spawn_obstacle += 1
        if self.timers.spawn_obstacle > 60:
            new_obstacle = Obstacle(self.obstacle_speed) #
            self.obstacles.add(new_obstacle) 
            self.timers.spawn_obstacle = 0
            if not self.run_state.is_over: self.score += 1
            if self.score > 0 and self.score % 20 == 0: self.obstacle_speed = min(self.obstacle_speed + 0.3, 8)

        # PowerUp Spawning logic call
        self.update_powerups() # <<< --- ADDED THIS CALL BACK

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
        self.powerups.update() # This updates existing powerups (movement, off-screen check via their own update)

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

        self.player.speed = 6 if is_shrink_active else 8 
        self.speed_multiplier = 0.5 if is_slowmo_active else 1.0
        if self.effects.pickup_message and now >= self.timers.pickup_message_end_tick:
            self.effects.pickup_message = ""

    def check_collisions(self, now):
        collided_obstacles = pygame.sprite.spritecollide(self.player, self.obstacles, False) 
        if collided_obstacles:
            is_player_invincible = now < self.timers.player_invincible_end_tick
            if not is_player_invincible:
                for obs in collided_obstacles: 
                    if self.effects.shield:
                        self.effects.shield = False
                        obs.kill() 
                        self.effects.pickup_message = "Shield Lost!"
                        self.timers.pickup_message_end_tick = now + PICKUP_MESSAGE_DURATION_MS
                    else:
                        self.lives -= 1
                        obs.kill()
                        if self.lives <= 0:
                            self.run_state.is_over = True
                            self.update_score()
                            break 
                        else:
                            self.timers.player_invincible_end_tick = now + PLAYER_INVINCIBILITY_DURATION_MS
                            self.effects.pickup_message = f"Life Lost! {self.lives} left"
                            self.timers.pickup_message_end_tick = now + PICKUP_MESSAGE_DURATION_MS
            elif collided_obstacles: # Player is invincible, remove obstacle on contact
                 for obs in collided_obstacles: 
                     obs.kill()


        bullet_hits = pygame.sprite.groupcollide(self.companion_bullets, self.obstacles, True, True)
        if bullet_hits:
            for bullet, obs_list in bullet_hits.items(): 
                self.score += len(obs_list) 
                # Potentially add sound/particle for hit later

        collided_powerups = pygame.sprite.spritecollide(self.player, self.powerups, True) 
        for p_up in collided_powerups:
            self.handle_powerup_pickup(p_up, now)


    def update_powerups(self): # This method IS for spawning powerups
        self.timers.spawn_powerup += 1
        if self.timers.spawn_powerup > 450: # Approx every 7.5 seconds at 60 FPS
            self.powerups.add(PowerUp()) #
            self.timers.spawn_powerup = 0
        # Individual powerup movement and off-screen checks are handled by PowerUp.update() via self.powerups.update()

    def handle_powerup_pickup(self, powerup, current_tick):
        self.timers.pickup_message_end_tick = current_tick + PICKUP_MESSAGE_DURATION_MS
        if powerup.type == "shield":
            self.effects.shield = True; self.effects.pickup_message = "Shield Activated!"
        elif powerup.type == "slowmo":
            self.timers.slowmo_effect_end_tick = current_tick + SLOWMO_DURATION_MS; self.effects.pickup_message = "Slow Motion!"
        elif powerup.type == "bomb":
            self.effects.bomb_ready = True; self.obstacles.empty(); self.effects.pickup_message = "Bomb Activated!" 
        elif powerup.type == "shrink":
            self.timers.shrink_effect_end_tick = current_tick + SHRINK_DURATION_MS; self.effects.pickup_message = "Shrink Activated!"
        elif powerup.type == "extralife":
            self.lives += 1; self.effects.pickup_message = f"Extra Life! ({self.lives} total)"
        elif powerup.type == "turret": 
            self.companion = Companion(self.player.rect)
            self.timers.companion_active_end_tick = current_tick + COMPANION_DURATION_MS
            self.effects.pickup_message = "Turret Activated!"


    def render_game(self):
        now = pygame.time.get_ticks()
        is_player_invincible_visual = now < self.timers.player_invincible_end_tick

        if is_player_invincible_visual and (now // 100) % 2 == 0 : pass 
        else: self.player.draw(self.screen)
            
        self.obstacles.draw(self.screen) 
        self.powerups.draw(self.screen)  
        
        if self.companion:
            self.companion.draw(self.screen)
        self.companion_bullets.draw(self.screen) 

        self.render_ui(now) 

        if self.run_state.is_paused: self.show_pause_or_gameover_screen("PAUSED")
        if self.run_state.is_over: self.show_pause_or_gameover_screen("GAME OVER")

    def render_ui(self, now): 
        self.screen.blit(self.font.render(f"Player: {self.username}", True, (255,255,255)), (10,10))
        self.screen.blit(self.font.render(f"Score: {self.score}", True, (255,255,255)), (10,40))
        self.screen.blit(self.font.render(f"Lives: {self.lives}", True, (255,255,255)), (10,70))
        hs_text = self.font.render(f"High Score: {self.high_score}", True, (255,255,255)); self.screen.blit(hs_text, (WIDTH - hs_text.get_width() - 10, 10))

        if self.companion and now < self.timers.companion_active_end_tick:
            time_left_turret = (self.timers.companion_active_end_tick - now) / 1000
            turret_timer_text = self.small_font.render(f"Turret: {time_left_turret:.1f}s", True, (200,200,200))
            self.screen.blit(turret_timer_text, (WIDTH - turret_timer_text.get_width() - 10, 40))

        if self.effects.pickup_message and now < self.timers.pickup_message_end_tick:
            msg_surface = self.font.render(self.effects.pickup_message, True, (255,255,100))
            self.screen.blit(msg_surface, (WIDTH // 2 - msg_surface.get_width() // 2, HEIGHT - 60))
        elif self.effects.pickup_message: self.effects.pickup_message = ""

        if self.effects.shield: pygame.draw.circle(self.screen, (0,255,255,100), self.player.rect.center, int(self.player.rect.width * 0.75) , 3) # Adjusted shield visual

    def show_pause_or_gameover_screen(self, message):
        overlay = pygame.Surface((WIDTH,HEIGHT)); overlay.set_alpha(180); overlay.fill((0,0,0)); self.screen.blit(overlay, (0,0))
        center_x = WIDTH // 2
        title_font = pygame.font.SysFont("consolas",48); info_font = self.font
        title_surf = title_font.render(message,True,(255,255,255)); self.screen.blit(title_surf,(center_x-title_surf.get_width()//2,160))
        score_surf = info_font.render(f"Your Score: {self.score}",True,(255,255,255)); self.screen.blit(score_surf,(center_x-score_surf.get_width()//2,230))
        prompt_text = "Press P to Resume" if message=="PAUSED" else "Press R to Restart"
        prompt_surf = info_font.render(prompt_text,True,(255,255,255)); self.screen.blit(prompt_surf,(center_x-prompt_surf.get_width()//2,270))
        if message=="GAME OVER" or message=="PAUSED": draw_high_scores(self.screen,self.small_font,y_start=340)