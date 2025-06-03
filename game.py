import pygame
import random
import math
from player import Player #
from obstacle import Obstacle #
from powerups import PowerUp #
from utils import get_username, save_high_scores, update_high_scores, get_high_scores, get_high_score_value, WIDTH, HEIGHT #
from bullet import Bullet
from companion import Companion
from particle import Particle
from dataclasses import dataclass, field

# --- Constants for timed effects ---
SHRINK_DURATION_MS = 10000; SLOWMO_DURATION_MS = 5000; PICKUP_MESSAGE_DURATION_MS = 2000
PLAYER_INVINCIBILITY_DURATION_MS = 1500; COMPANION_DURATION_MS = 10000
# ---

# --- Dataclasses ---
@dataclass
class GameTimers:
    spawn_obstacle: int = 0; spawn_powerup: int = 0
    slowmo_effect_end_tick: int = 0; shrink_effect_end_tick: int = 0
    pickup_message_end_tick: int = 0; player_invincible_end_tick: int = 0
    companion_active_end_tick: int = 0
@dataclass
class ActiveEffects:
    shield: bool = False; bomb_ready: bool = False; pickup_message: str = ""
# ---

# --- Starfield Constants ---
NUM_STARS = 100; STAR_SPEED_MIN = 1; STAR_SPEED_MAX = 4
STAR_COLORS = [(100,100,100),(150,150,150),(200,200,200),(50,50,80),(70,70,100)]
STAR_SIZE_MIN = 1; STAR_SIZE_MAX = 3
# ---
PARTICLES_PER_OBSTACLE_EXPLOSION = 15
# ---
UI_TIMER_BAR_WIDTH = 100; UI_TIMER_BAR_HEIGHT = 8
UI_TIMER_BAR_BG_COLOR = (50,50,50); UI_SLOWMO_TIMER_COLOR = (255,255,0)
UI_SHRINK_TIMER_COLOR = (255,0,255)
# ---

# Constants for menu actions
ACTION_SHOW_INSTRUCTIONS = "SHOW_INSTRUCTIONS"
ACTION_QUIT_GAME = "QUIT_GAME"

# --- Menu Button Constants (can be reused or specified per menu) ---
BUTTON_WIDTH = 220
BUTTON_HEIGHT = 45 # Slightly smaller for pause/instructions menu
BUTTON_COLOR_NORMAL = (0, 100, 150)
BUTTON_COLOR_HOVER = (0, 150, 200)
BUTTON_TEXT_COLOR = (255, 255, 255)
INPUT_BOX_COLOR_ACTIVE = (0, 200, 255)
INPUT_BOX_COLOR_INACTIVE = (255, 255, 255)
MENU_TEXT_COLOR = (255, 255, 255)
MENU_SUBTEXT_COLOR = (200, 200, 200)
MENU_TITLE_COLOR = (0, 255, 180)
# ---

def draw_text_centered(screen, text, font, color, surface_rect):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=surface_rect.center)
    screen.blit(text_surf, text_rect)

def show_main_menu(screen, username=""): 
    menu_font = pygame.font.SysFont("consolas", 30) 
    title_font = pygame.font.SysFont("consolas", 48) 
    small_font = pygame.font.SysFont("consolas", 22)
    input_font = pygame.font.SysFont("consolas", 28)
    clock = pygame.time.Clock()
    input_box_rect = pygame.Rect(WIDTH // 2 - 150, 220, 300, 40)
    input_box_active = False 
    current_username = username 
    running = True
    button_y_start = input_box_rect.bottom + 40
    button_spacing = BUTTON_HEIGHT + 20 # Use global BUTTON_HEIGHT
    start_button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, button_y_start, BUTTON_WIDTH, BUTTON_HEIGHT)
    instructions_button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, button_y_start + button_spacing, BUTTON_WIDTH, BUTTON_HEIGHT)
    quit_button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, button_y_start + button_spacing * 2, BUTTON_WIDTH, BUTTON_HEIGHT)

    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill((20, 20, 40))
        draw_text_centered(screen, "NEON DODGE", title_font, MENU_TITLE_COLOR, pygame.Rect(0, 100, WIDTH, title_font.get_height()))
        username_label_surf = small_font.render("Enter Username:", True, MENU_TEXT_COLOR)
        screen.blit(username_label_surf, (input_box_rect.x, input_box_rect.y - username_label_surf.get_height() - 5))
        current_input_box_color = INPUT_BOX_COLOR_ACTIVE if input_box_active else INPUT_BOX_COLOR_INACTIVE
        pygame.draw.rect(screen, current_input_box_color, input_box_rect, 2, border_radius=5)
        username_text_surf = input_font.render(current_username, True, MENU_TEXT_COLOR)
        screen.blit(username_text_surf, (input_box_rect.x + 10, input_box_rect.y + (input_box_rect.height - username_text_surf.get_height()) // 2))
        
        start_color = BUTTON_COLOR_HOVER if start_button_rect.collidepoint(mouse_pos) else BUTTON_COLOR_NORMAL
        pygame.draw.rect(screen, start_color, start_button_rect, border_radius=10)
        draw_text_centered(screen, "START GAME", menu_font, BUTTON_TEXT_COLOR, start_button_rect)
        instr_color = BUTTON_COLOR_HOVER if instructions_button_rect.collidepoint(mouse_pos) else BUTTON_COLOR_NORMAL
        pygame.draw.rect(screen, instr_color, instructions_button_rect, border_radius=10)
        draw_text_centered(screen, "INSTRUCTIONS", menu_font, BUTTON_TEXT_COLOR, instructions_button_rect)
        quit_color = BUTTON_COLOR_HOVER if quit_button_rect.collidepoint(mouse_pos) else BUTTON_COLOR_NORMAL
        pygame.draw.rect(screen, quit_color, quit_button_rect, border_radius=10)
        draw_text_centered(screen, "QUIT", menu_font, BUTTON_TEXT_COLOR, quit_button_rect)
        hs_y_start = quit_button_rect.bottom + 20
        if hs_y_start + 150 > HEIGHT : hs_y_start = HEIGHT - 150
        draw_high_scores(screen, small_font, y_start=hs_y_start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return ACTION_QUIT_GAME
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    input_box_active = input_box_rect.collidepoint(mouse_pos)
                    if start_button_rect.collidepoint(mouse_pos): return current_username.strip() if current_username.strip() else "Guest"
                    if instructions_button_rect.collidepoint(mouse_pos): return ACTION_SHOW_INSTRUCTIONS
                    if quit_button_rect.collidepoint(mouse_pos): return ACTION_QUIT_GAME
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return ACTION_QUIT_GAME
                if event.key == pygame.K_i: return ACTION_SHOW_INSTRUCTIONS 
                if input_box_active:
                    if event.key == pygame.K_RETURN: return current_username.strip() if current_username.strip() else "Guest"
                    elif event.key == pygame.K_BACKSPACE: current_username = current_username[:-1]
                    else:
                        if len(current_username) < 16 and event.unicode.isprintable(): current_username += event.unicode
                else: 
                    if event.key == pygame.K_RETURN: return current_username.strip() if current_username.strip() else "Guest"
        pygame.display.flip(); clock.tick(60)
    return ACTION_QUIT_GAME

def draw_high_scores(screen,font,y_start):
    highscores = get_high_scores() #
    highscores.sort(key=lambda x:x["score"],reverse=True)
    y_pos=y_start
    title_text_surf=font.render("Top 10 Scores",True,(255,255,255)); screen.blit(title_text_surf,(WIDTH//2-title_text_surf.get_width()//2,y_pos)); y_pos+=28
    for i,entry in enumerate(highscores[:10]):
        hs_text_surf=font.render(f"{i+1}. {entry['username']}: {entry['score']}",True,(200,200,200)); screen.blit(hs_text_surf,(WIDTH//2-hs_text_surf.get_width()//2,y_pos)); y_pos+=24

class Game:
    STATE_PLAYING = "playing"; STATE_PAUSED = "paused"
    STATE_GAME_OVER = "game_over"; STATE_INSTRUCTIONS = "instructions"
    STATE_EXIT_TO_MENU = "exit_to_menu" 
    STATE_CONFIRM_QUIT = "confirm_quit"

    INITIAL_LIVES = 3; SPLITTABLE_OBSTACLE_CHANCE = 0.25
    BASE_OBSTACLE_SPAWN_INTERVAL = 60; MIN_OBSTACLE_SPAWN_INTERVAL = 25
    SCORE_TO_REACH_MIN_INTERVAL = 250

    def __init__(self, screen, username, ai_mode=False, start_state=STATE_PLAYING): 
        self.ai_mode=ai_mode; self.screen=screen; self.username=username.strip() or "Guest"
        self.clock=pygame.time.Clock()
        self.font=pygame.font.SysFont("consolas",28) 
        self.small_font=pygame.font.SysFont("consolas",20) 
        self.medium_font = pygame.font.SysFont("consolas", 24) 
        self.large_font=pygame.font.SysFont("consolas",32) 
        
        self.reset_game_state() 
        self.current_state = start_state 
        if not self.username and start_state == self.STATE_INSTRUCTIONS: self.username = "Player" 

        self.pause_resume_button = None
        self.pause_instructions_button = None
        self.pause_restart_button = None
        self.pause_main_menu_button = None
        self.instructions_back_button = None
        
        self.confirm_quit_yes_button = None 
        self.confirm_quit_no_button = None  
        self.previous_state_on_quit_request = None 
        self.quit_context_message = "Are you sure you want to quit?"


    def _create_star(self): 
        x=random.randint(0,WIDTH);y=random.randint(0,HEIGHT);speed=random.randint(STAR_SPEED_MIN,STAR_SPEED_MAX)
        color=random.choice(STAR_COLORS);size=random.randint(STAR_SIZE_MIN,STAR_SIZE_MAX)
        return [x,y,speed,color,size]

    def _create_explosion(self,position,base_color,num_particles=PARTICLES_PER_OBSTACLE_EXPLOSION): 
        for _ in range(num_particles): self.particles.add(Particle(position[0],position[1],base_color))

    def reset_game_state(self): 
        self.player=Player() #
        self.obstacles=pygame.sprite.Group(); self.powerups=pygame.sprite.Group()
        self.score=0; self.high_score=get_high_score_value() #
        self.obstacle_speed=4; self.speed_multiplier=1.0; self.lives=self.INITIAL_LIVES
        self.timers=GameTimers(); self.effects=ActiveEffects()
        self.companion=None; self.companion_bullets=pygame.sprite.Group()
        self.stars=[self._create_star() for _ in range(NUM_STARS)]
        self.particles=pygame.sprite.Group()
        self.previous_state_on_quit_request = self.STATE_PLAYING 


    def _update_stars(self): 
        for i in range(len(self.stars)):
            star=self.stars[i]; star[1]+=star[2]*self.speed_multiplier
            if star[1]>HEIGHT: self.stars[i]=[random.randint(0,WIDTH),random.randint(-20,-5),random.randint(STAR_SPEED_MIN,STAR_SPEED_MAX),random.choice(STAR_COLORS),random.randint(STAR_SIZE_MIN,STAR_SIZE_MAX)]

    def _draw_stars(self): 
        for star_data in self.stars: pygame.draw.rect(self.screen,star_data[3],(star_data[0],star_data[1],star_data[4],star_data[4]))

    def update_score(self): 
        update_high_scores(self.username,self.score) #
        self.high_score=get_high_score_value() #

    @staticmethod
    def ai_decide_move(player,obstacles_group): 
        if not obstacles_group: return 0
        closest=None;min_dist=float('inf')
        for obs in obstacles_group:
            dist=abs(obs.rect.centerx-player.rect.x)+abs(obs.rect.centery-player.rect.y)
            if dist<min_dist:min_dist=dist;closest=obs
        if not closest:return 0;dx=0;dy=0
        if player.rect.x<closest.rect.centerx:dx=-1
        elif player.rect.x>closest.rect.centerx:dx=1
        if player.rect.y<closest.rect.centery:dy=-1
        elif player.rect.y>closest.rect.centery:dy=1
        if abs(player.rect.x-closest.rect.centerx)>abs(player.rect.y-closest.rect.centery): return 1 if dx>0 else 2 if dx<0 else 0
        else: return 3 if dy<0 else 4 if dy>0 else 0
    
    def run_instructions_loop(self): 
        self.current_state = self.STATE_INSTRUCTIONS 
        instructions_running = True
        back_button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT)
        while instructions_running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); exit() 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p or event.key == pygame.K_i:
                        instructions_running = False 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and back_button_rect.collidepoint(mouse_pos):
                        instructions_running = False
            self.screen.fill((10, 10, 20)) 
            self._draw_stars() 
            self.render_instructions_screen(mouse_pos, back_button_rect) 
            pygame.display.flip(); self.clock.tick(30) 

    def game_loop(self): 
        while self.current_state not in [self.STATE_EXIT_TO_MENU, ACTION_QUIT_GAME]: 
            self.screen.fill((10,10,20))
            self.handle_events()
            if self.current_state == self.STATE_PLAYING: self.update_game_logic()
            self.render_game()
            pygame.display.flip(); self.clock.tick(60)
        if self.current_state == self.STATE_EXIT_TO_MENU: return self.STATE_EXIT_TO_MENU 
        return ACTION_QUIT_GAME 

    def handle_events(self):
        keys=pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos() 

        for e in pygame.event.get():
            if e.type == pygame.QUIT: 
                self.previous_state_on_quit_request = self.current_state 
                self.quit_context_message = "Quit Game?" 
                self.current_state = self.STATE_CONFIRM_QUIT
                return 
            
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1: 
                if self.current_state == self.STATE_PAUSED:
                    if self.pause_resume_button and self.pause_resume_button.collidepoint(mouse_pos): self.current_state = self.STATE_PLAYING
                    elif self.pause_instructions_button and self.pause_instructions_button.collidepoint(mouse_pos): self.current_state = self.STATE_INSTRUCTIONS
                    elif self.pause_restart_button and self.pause_restart_button.collidepoint(mouse_pos): self.current_state = self.STATE_EXIT_TO_MENU
                    elif self.pause_main_menu_button and self.pause_main_menu_button.collidepoint(mouse_pos): self.current_state = self.STATE_EXIT_TO_MENU
                elif self.current_state == self.STATE_INSTRUCTIONS: 
                    if self.instructions_back_button and self.instructions_back_button.collidepoint(mouse_pos):
                        self.current_state = self.STATE_PAUSED
                elif self.current_state == self.STATE_CONFIRM_QUIT:
                    if self.confirm_quit_yes_button and self.confirm_quit_yes_button.collidepoint(mouse_pos):
                        if self.quit_context_message == "Quit Game?":
                             self.current_state = ACTION_QUIT_GAME
                        else: 
                             self.current_state = self.STATE_EXIT_TO_MENU
                    elif self.confirm_quit_no_button and self.confirm_quit_no_button.collidepoint(mouse_pos):
                        self.current_state = self.previous_state_on_quit_request 
            
            if e.type == pygame.KEYDOWN:
                if self.current_state == self.STATE_PLAYING:
                    if e.key == pygame.K_p: self.current_state = self.STATE_PAUSED
                    elif e.key == pygame.K_ESCAPE: 
                        self.previous_state_on_quit_request = self.STATE_PLAYING 
                        self.quit_context_message = "Go to Pause Menu?" 
                        self.current_state = self.STATE_CONFIRM_QUIT
                elif self.current_state == self.STATE_PAUSED:
                    if e.key == pygame.K_p: self.current_state = self.STATE_PLAYING
                    elif e.key == pygame.K_i: self.current_state = self.STATE_INSTRUCTIONS
                    elif e.key == pygame.K_ESCAPE: 
                        self.previous_state_on_quit_request = self.STATE_PAUSED
                        self.quit_context_message = "Quit to Main Menu?"
                        self.current_state = self.STATE_CONFIRM_QUIT
                    elif e.key == pygame.K_r: 
                        self.previous_state_on_quit_request = self.STATE_PAUSED 
                        self.quit_context_message = "Restart (to Main Menu)?"
                        self.current_state = self.STATE_CONFIRM_QUIT
                elif self.current_state == self.STATE_GAME_OVER:
                    if e.key == pygame.K_r: 
                        self.previous_state_on_quit_request = self.STATE_GAME_OVER
                        self.quit_context_message = "Restart (to Main Menu)?"
                        self.current_state = self.STATE_CONFIRM_QUIT
                    elif e.key == pygame.K_ESCAPE: 
                        self.previous_state_on_quit_request = self.STATE_GAME_OVER
                        self.quit_context_message = "Quit to Main Menu?"
                        self.current_state = self.STATE_CONFIRM_QUIT
                elif self.current_state == self.STATE_INSTRUCTIONS: 
                    if e.key == pygame.K_p or e.key == pygame.K_ESCAPE or e.key == pygame.K_i:
                        self.current_state = self.STATE_PAUSED 
                elif self.current_state == self.STATE_CONFIRM_QUIT:
                    if e.key == pygame.K_y: 
                        if self.quit_context_message == "Quit Game?":
                             self.current_state = ACTION_QUIT_GAME
                        else:
                             self.current_state = self.STATE_EXIT_TO_MENU
                    elif e.key == pygame.K_n: 
                        self.current_state = self.previous_state_on_quit_request
        
        if not self.ai_mode and self.current_state == self.STATE_PLAYING: self.player.move(keys)

    def update_game_logic(self):
        now=pygame.time.get_ticks()
        if self.ai_mode:pass # AI move logic would go here
        self._update_stars()
        self.timers.spawn_obstacle+=1
        current_spawn_interval=self.BASE_OBSTACLE_SPAWN_INTERVAL
        if self.SCORE_TO_REACH_MIN_INTERVAL>0:
            if self.score>=self.SCORE_TO_REACH_MIN_INTERVAL:current_spawn_interval=self.MIN_OBSTACLE_SPAWN_INTERVAL
            else:
                progress=self.score/self.SCORE_TO_REACH_MIN_INTERVAL
                interval_reduction=(self.BASE_OBSTACLE_SPAWN_INTERVAL-self.MIN_OBSTACLE_SPAWN_INTERVAL)*progress
                current_spawn_interval=self.BASE_OBSTACLE_SPAWN_INTERVAL-interval_reduction
        current_spawn_interval=max(self.MIN_OBSTACLE_SPAWN_INTERVAL,int(current_spawn_interval))
        if self.timers.spawn_obstacle>current_spawn_interval:
            self.timers.spawn_obstacle=0;new_obstacle=None
            if random.random()<self.SPLITTABLE_OBSTACLE_CHANCE: new_obstacle=Obstacle(self.obstacle_speed,1,True,2)
            else: new_obstacle=Obstacle(self.obstacle_speed,1,False)
            if new_obstacle:self.obstacles.add(new_obstacle)
            self.score+=1 # Score per obstacle wave/spawn event
            if self.score>0 and self.score%20==0 and self.obstacle_speed<10: # Speed increase logic
                if(self.score//20)>((self.score-1)//20):self.obstacle_speed=min(self.obstacle_speed+0.3,10)
        self.update_powerups()
        self.update_effects(now)
        if self.companion:
            if now<self.timers.companion_active_end_tick:
                new_bullets=self.companion.update(self.player.rect)
                if new_bullets:self.companion_bullets.add(new_bullets)
            else:self.companion=None
        self.companion_bullets.update();self.obstacles.update(self.speed_multiplier);self.powerups.update();self.particles.update()
        self.check_collisions(now)

    def update_effects(self,now):
        # Corrected lines:
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

    def check_collisions(self,now): 
        collided_obs_player=pygame.sprite.spritecollide(self.player,self.obstacles,False)
        if collided_obs_player:
            is_player_invincible=now<self.timers.player_invincible_end_tick
            if not is_player_invincible:
                for obs in collided_obs_player:
                    if self.effects.shield:self.effects.shield=False;self._create_explosion(obs.rect.center,obs.color);obs.kill();self.effects.pickup_message="Shield Lost!";self.timers.pickup_message_end_tick=now+PICKUP_MESSAGE_DURATION_MS
                    else:
                        self.lives-=1;self._create_explosion(obs.rect.center,obs.color);obs.kill()
                        if self.lives<=0:self.current_state=self.STATE_GAME_OVER;self.update_score();break
                        else:self.timers.player_invincible_end_tick=now+PLAYER_INVINCIBILITY_DURATION_MS;self.effects.pickup_message=f"Life Lost! {self.lives} left";self.timers.pickup_message_end_tick=now+PICKUP_MESSAGE_DURATION_MS
            elif collided_obs_player:
                 for obs in collided_obs_player:self._create_explosion(obs.rect.center,obs.color);obs.kill()
        bullet_hits=pygame.sprite.groupcollide(self.companion_bullets,self.obstacles,True,False)
        for bullet,hit_obs_list in bullet_hits.items():
            for obs in hit_obs_list:self.score+=1;self._create_explosion(obs.rect.center,obs.color);obs.kill()
        collided_powerups_player=pygame.sprite.spritecollide(self.player,self.powerups,True)
        for p_up in collided_powerups_player:self.handle_powerup_pickup(p_up,now)

    def update_powerups(self): 
        self.timers.spawn_powerup+=1
        if self.timers.spawn_powerup>450:self.powerups.add(PowerUp());self.timers.spawn_powerup=0

    def handle_powerup_pickup(self,powerup,current_tick): 
        self.timers.pickup_message_end_tick=current_tick+PICKUP_MESSAGE_DURATION_MS
        if powerup.type=="shield":self.effects.shield=True;self.effects.pickup_message="Shield Activated!"
        elif powerup.type=="slowmo":self.timers.slowmo_effect_end_tick=current_tick+SLOWMO_DURATION_MS;self.effects.pickup_message="Slow Motion!"
        elif powerup.type=="bomb":
            self.effects.pickup_message="KABOOM!"
            newly_split_obstacles=[]
            for obs in list(self.obstacles.sprites()):
                self._create_explosion(obs.rect.center,obs.color,num_particles=PARTICLES_PER_OBSTACLE_EXPLOSION//2)
                if hasattr(obs,'can_split')and obs.can_split and hasattr(obs,'get_split_pieces'):pieces=obs.get_split_pieces();newly_split_obstacles.extend(pieces)
                obs.kill()
            self.obstacles.add(newly_split_obstacles)
        elif powerup.type=="shrink":self.timers.shrink_effect_end_tick=current_tick+SHRINK_DURATION_MS;self.effects.pickup_message="Shrink Activated!"
        elif powerup.type=="extralife":self.lives+=1;self.effects.pickup_message=f"Extra Life! ({self.lives} total)"
        elif powerup.type=="turret":self.companion=Companion(self.player.rect);self.timers.companion_active_end_tick=current_tick+COMPANION_DURATION_MS;self.effects.pickup_message="Turret Activated!"

    def render_instructions_screen(self, mouse_pos=None, back_button_override_rect=None): 
        overlay = pygame.Surface((WIDTH, HEIGHT)); overlay.set_alpha(230); overlay.fill((15,15,35)); self.screen.blit(overlay, (0,0))
        y_offset = 60
        title_surf = self.large_font.render("INSTRUCTIONS", True, MENU_TITLE_COLOR)
        self.screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, y_offset))
        y_offset += title_surf.get_height() + 30
        instructions = [("Controls:",True),(" Arrow Keys / WASD - Move Player",False),(" P - Pause / Resume Game",False),(" I - View Instructions (from Pause)", False),(" ESC - Return to Previous Menu / Pause", False),("",False),("Objective:",True),(" Dodge incoming obstacles!",False),(" Collect power-ups for help.",False),("",False),("Power-ups:",True),(" Shield (Blue) - One hit protection.",False),(" SlowMo (Yellow) - Slows obstacles.",False),(" Bomb (Red) - Clears obstacles (splits some).",False),(" Shrink (Magenta) - Player smaller & faster.",False),(" 1UP (Green) - Grants an extra life.",False),(" Turret (Grey) - Auto-shoots obstacles.",False)]
        line_height_title = self.font.get_height() + 8; line_height_text = self.small_font.get_height() + 5
        for text, is_title in instructions:
            if is_title: text_surf = self.font.render(text, True, (220,220,255)); y_offset += 10; line_h = line_height_title
            else: text_surf = self.small_font.render(text, True, (200,200,200)); line_h = line_height_text
            self.screen.blit(text_surf, (WIDTH//2-text_surf.get_width()//2, y_offset)); y_offset += line_h
        cbbr=back_button_override_rect if back_button_override_rect else self.instructions_back_button
        if not cbbr:self.instructions_back_button=pygame.Rect(WIDTH//2-BUTTON_WIDTH//2,HEIGHT-BUTTON_HEIGHT-40,BUTTON_WIDTH,BUTTON_HEIGHT);cbbr=self.instructions_back_button
        bc=BUTTON_COLOR_NORMAL;
        if mouse_pos and cbbr.collidepoint(mouse_pos):bc=BUTTON_COLOR_HOVER
        pygame.draw.rect(self.screen,bc,cbbr,border_radius=10);draw_text_centered(self.screen,"BACK (Esc/P/I)",self.medium_font,BUTTON_TEXT_COLOR,cbbr)

    def render_confirm_quit_screen(self, mouse_pos=None):
        overlay = pygame.Surface((WIDTH, HEIGHT)); overlay.set_alpha(230); overlay.fill((10,10,20)); self.screen.blit(overlay, (0,0))
        dialog_width = WIDTH * 0.7; dialog_height = HEIGHT * 0.4
        dialog_x = WIDTH//2-dialog_width//2; dialog_y = HEIGHT//2-dialog_height//2
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        pygame.draw.rect(self.screen, (30,30,50), dialog_rect, border_radius=15)
        pygame.draw.rect(self.screen, MENU_TITLE_COLOR, dialog_rect, 3, border_radius=15)
        title_surf = self.large_font.render("Confirm Exit", True, MENU_TEXT_COLOR)
        self.screen.blit(title_surf, (dialog_rect.centerx - title_surf.get_width()//2, dialog_rect.top + 30))
        query_surf = self.font.render(self.quit_context_message, True, MENU_SUBTEXT_COLOR)
        self.screen.blit(query_surf, (dialog_rect.centerx - query_surf.get_width()//2, dialog_rect.top + 90))
        button_w, button_h = 120, BUTTON_HEIGHT; gap = 30; total_buttons_width = button_w * 2 + gap
        self.confirm_quit_yes_button = pygame.Rect(dialog_rect.centerx - total_buttons_width//2, dialog_rect.bottom - button_h - 40, button_w, button_h)
        self.confirm_quit_no_button = pygame.Rect(self.confirm_quit_yes_button.right + gap, self.confirm_quit_yes_button.top, button_w, button_h)
        yes_color = BUTTON_COLOR_HOVER if mouse_pos and self.confirm_quit_yes_button.collidepoint(mouse_pos) else BUTTON_COLOR_NORMAL
        pygame.draw.rect(self.screen, yes_color, self.confirm_quit_yes_button, border_radius=10)
        draw_text_centered(self.screen, "YES (Y)", self.medium_font, BUTTON_TEXT_COLOR, self.confirm_quit_yes_button)
        no_color = BUTTON_COLOR_HOVER if mouse_pos and self.confirm_quit_no_button.collidepoint(mouse_pos) else BUTTON_COLOR_NORMAL
        pygame.draw.rect(self.screen, no_color, self.confirm_quit_no_button, border_radius=10)
        draw_text_centered(self.screen, "NO (N)", self.medium_font, BUTTON_TEXT_COLOR, self.confirm_quit_no_button)

    def render_game(self): 
        now=pygame.time.get_ticks(); self._draw_stars()
        mouse_pos = pygame.mouse.get_pos() 
        if self.current_state == self.STATE_PLAYING or self.current_state == self.STATE_PAUSED :
            is_player_invincible_visual=now<self.timers.player_invincible_end_tick
            if is_player_invincible_visual and(now//100)%2==0:pass
            else:self.player.draw(self.screen)
            self.obstacles.draw(self.screen);self.powerups.draw(self.screen)
            if self.companion:self.companion.draw(self.screen)
            self.companion_bullets.draw(self.screen);self.particles.draw(self.screen)
        self.render_ui(now)
        if self.current_state == self.STATE_PAUSED: self.show_pause_or_gameover_screen("PAUSED", mouse_pos)
        elif self.current_state == self.STATE_GAME_OVER: self.show_pause_or_gameover_screen("GAME OVER", mouse_pos)
        elif self.current_state == self.STATE_INSTRUCTIONS: self.render_instructions_screen(mouse_pos)
        elif self.current_state == self.STATE_CONFIRM_QUIT: self.render_confirm_quit_screen(mouse_pos)

    def render_ui(self,now): 
        self.screen.blit(self.font.render(f"Player: {self.username}",True,(255,255,255)),(10,10))
        self.screen.blit(self.font.render(f"Score: {self.score}",True,(255,255,255)),(10,40))
        self.screen.blit(self.font.render(f"Lives: {self.lives}",True,(255,255,255)),(10,70))
        hs_text_surf=self.font.render(f"High Score: {self.high_score}",True,(255,255,255));self.screen.blit(hs_text_surf,(WIDTH-hs_text_surf.get_width()-10,10))
        ui_timer_y_current=40;ui_timer_x_pos=WIDTH-UI_TIMER_BAR_WIDTH-10;label_padding=5;timer_spacing=15
        if self.companion and now<self.timers.companion_active_end_tick:
            time_left_turret=(self.timers.companion_active_end_tick-now)/1000
            turret_timer_text_surf=self.small_font.render(f"Turret: {time_left_turret:.1f}s",True,(200,200,200))
            self.screen.blit(turret_timer_text_surf,(WIDTH-turret_timer_text_surf.get_width()-10,ui_timer_y_current));ui_timer_y_current+=turret_timer_text_surf.get_height()+(timer_spacing//2)
        if now<self.timers.slowmo_effect_end_tick:
            time_left=self.timers.slowmo_effect_end_tick-now;percentage_left=max(0,time_left/SLOWMO_DURATION_MS)
            slowmo_label_surf=self.small_font.render("SlowMo",True,UI_SLOWMO_TIMER_COLOR);label_y=ui_timer_y_current+(UI_TIMER_BAR_HEIGHT-slowmo_label_surf.get_height())//2
            self.screen.blit(slowmo_label_surf,(ui_timer_x_pos-slowmo_label_surf.get_width()-label_padding,label_y))
            pygame.draw.rect(self.screen,UI_TIMER_BAR_BG_COLOR,(ui_timer_x_pos,ui_timer_y_current,UI_TIMER_BAR_WIDTH,UI_TIMER_BAR_HEIGHT))
            current_bar_width=int(UI_TIMER_BAR_WIDTH*percentage_left);pygame.draw.rect(self.screen,UI_SLOWMO_TIMER_COLOR,(ui_timer_x_pos,ui_timer_y_current,current_bar_width,UI_TIMER_BAR_HEIGHT));ui_timer_y_current+=UI_TIMER_BAR_HEIGHT+timer_spacing
        if now<self.timers.shrink_effect_end_tick:
            time_left=self.timers.shrink_effect_end_tick-now;percentage_left=max(0,time_left/SHRINK_DURATION_MS)
            shrink_label_surf=self.small_font.render("Shrink",True,UI_SHRINK_TIMER_COLOR);label_y=ui_timer_y_current+(UI_TIMER_BAR_HEIGHT-shrink_label_surf.get_height())//2
            self.screen.blit(shrink_label_surf,(ui_timer_x_pos-shrink_label_surf.get_width()-label_padding,label_y))
            pygame.draw.rect(self.screen,UI_TIMER_BAR_BG_COLOR,(ui_timer_x_pos,ui_timer_y_current,UI_TIMER_BAR_WIDTH,UI_TIMER_BAR_HEIGHT))
            current_bar_width=int(UI_TIMER_BAR_WIDTH*percentage_left);pygame.draw.rect(self.screen,UI_SHRINK_TIMER_COLOR,(ui_timer_x_pos,ui_timer_y_current,current_bar_width,UI_TIMER_BAR_HEIGHT))
        if self.effects.pickup_message and now<self.timers.pickup_message_end_tick:
            msg_surface=self.font.render(self.effects.pickup_message,True,(255,255,100));self.screen.blit(msg_surface,(WIDTH//2-msg_surface.get_width()//2,HEIGHT-60))
        elif self.effects.pickup_message:self.effects.pickup_message=""
        if self.effects.shield:pygame.draw.circle(self.screen,(0,255,255,100),self.player.rect.center,int(self.player.rect.width*0.75),3)

    def show_pause_or_gameover_screen(self, message, mouse_pos=None): 
        overlay=pygame.Surface((WIDTH,HEIGHT));overlay.set_alpha(180);overlay.fill((0,0,0));self.screen.blit(overlay,(0,0))
        center_x=WIDTH//2;title_font=pygame.font.SysFont("consolas",48); button_font = self.medium_font
        main_title_surf=title_font.render(message,True,(255,255,255));self.screen.blit(main_title_surf,(center_x-main_title_surf.get_width()//2,20))
        if message != "GAME OVER": 
            score_surf=self.font.render(f"Your Score: {self.score}",True,(255,255,255));self.screen.blit(score_surf,(center_x-score_surf.get_width()//2,90))
            y_button_start = 110
        else: 
            score_surf=self.font.render(f"Your Score: {self.score}",True,(255,255,255));self.screen.blit(score_surf,(center_x-score_surf.get_width()//2,90))
            y_button_start = 110
        button_y = y_button_start + 30; button_spacing_pause = BUTTON_HEIGHT + 15
        if message == "PAUSED":
            self.pause_resume_button = pygame.Rect(center_x - BUTTON_WIDTH // 2, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
            color = BUTTON_COLOR_HOVER if mouse_pos and self.pause_resume_button.collidepoint(mouse_pos) else BUTTON_COLOR_NORMAL
            pygame.draw.rect(self.screen, color, self.pause_resume_button, border_radius=10); draw_text_centered(self.screen, "RESUME (P)", button_font, BUTTON_TEXT_COLOR, self.pause_resume_button); button_y += button_spacing_pause
            self.pause_instructions_button = pygame.Rect(center_x - BUTTON_WIDTH // 2, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
            color = BUTTON_COLOR_HOVER if mouse_pos and self.pause_instructions_button.collidepoint(mouse_pos) else BUTTON_COLOR_NORMAL
            pygame.draw.rect(self.screen, color, self.pause_instructions_button, border_radius=10); draw_text_centered(self.screen, "INSTRUCTIONS (I)", button_font, BUTTON_TEXT_COLOR, self.pause_instructions_button); button_y += button_spacing_pause
            self.pause_restart_button = pygame.Rect(center_x - BUTTON_WIDTH // 2, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
            color = BUTTON_COLOR_HOVER if mouse_pos and self.pause_restart_button.collidepoint(mouse_pos) else BUTTON_COLOR_NORMAL
            pygame.draw.rect(self.screen, color, self.pause_restart_button, border_radius=10); draw_text_centered(self.screen, "RESTART (R)", button_font, BUTTON_TEXT_COLOR, self.pause_restart_button); button_y += button_spacing_pause
            self.pause_main_menu_button = pygame.Rect(center_x - BUTTON_WIDTH // 2, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
            color = BUTTON_COLOR_HOVER if mouse_pos and self.pause_main_menu_button.collidepoint(mouse_pos) else BUTTON_COLOR_NORMAL
            pygame.draw.rect(self.screen, color, self.pause_main_menu_button, border_radius=10); draw_text_centered(self.screen, "MAIN MENU (Esc)", button_font, BUTTON_TEXT_COLOR, self.pause_main_menu_button); button_y += button_spacing_pause
        elif message == "GAME OVER":
            self.pause_restart_button = pygame.Rect(center_x - BUTTON_WIDTH // 2, button_y, BUTTON_WIDTH, BUTTON_HEIGHT) 
            color = BUTTON_COLOR_HOVER if mouse_pos and self.pause_restart_button.collidepoint(mouse_pos) else BUTTON_COLOR_NORMAL
            pygame.draw.rect(self.screen, color, self.pause_restart_button, border_radius=10); draw_text_centered(self.screen, "RESTART (R)", button_font, BUTTON_TEXT_COLOR, self.pause_restart_button); button_y += button_spacing_pause
            self.pause_main_menu_button = pygame.Rect(center_x - BUTTON_WIDTH // 2, button_y, BUTTON_WIDTH, BUTTON_HEIGHT) 
            color = BUTTON_COLOR_HOVER if mouse_pos and self.pause_main_menu_button.collidepoint(mouse_pos) else BUTTON_COLOR_NORMAL
            pygame.draw.rect(self.screen, color, self.pause_main_menu_button, border_radius=10); draw_text_centered(self.screen, "MAIN MENU (Esc)", button_font, BUTTON_TEXT_COLOR, self.pause_main_menu_button); button_y += button_spacing_pause
        if message=="GAME OVER" or message=="PAUSED":draw_high_scores(self.screen,self.small_font,y_start=button_y + 10)