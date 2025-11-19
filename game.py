import pgzrun
import random
import math
from pygame import Rect

# --- CONSTANTS & CONFIGURATION ---
WIDTH = 800
HEIGHT = 600
TITLE = "Dungeon Escape: Tutor Test"

# Colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BUTTON = (60, 60, 110)
COLOR_TEXT_SHADOW = (0, 0, 0)
COLOR_GOLD = (255, 215, 0)

# Game States
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAMEOVER = "gameover"
STATE_WIN = "win" 

# --- GLOBAL VARIABLES ---
game_state = STATE_MENU
sound_enabled = True
current_music_playing = False
score = 0  # <--- VARIÁVEL DE PONTOS

# --- CLASSES ---

class AnimatedSprite:
    def __init__(self, img_prefix, pos, animation_speed=0.15):
        self.x, self.y = pos
        self.img_prefix = img_prefix
        self.animation_speed = animation_speed
        self.timer = 0
        self.frame_index = 1
        self.state = "idle"
        self.actor = Actor(f"{self.img_prefix}_{self.state}_1", pos)

    def animate(self, dt):
        self.timer += dt
        if self.timer > self.animation_speed:
            self.timer = 0
            self.frame_index += 1
            if self.frame_index > 2:
                self.frame_index = 1
            img_name = f"{self.img_prefix}_{self.state}_{self.frame_index}"
            self.actor.image = img_name

    def draw(self):
        self.actor.pos = (self.x, self.y)
        self.actor.draw()

class Character(AnimatedSprite):
    def __init__(self, img_prefix, pos, speed):
        super().__init__(img_prefix, pos)
        self.speed = speed
        self.velocity_x = 0
        self.velocity_y = 0

    def move(self, dt):
        if self.velocity_x != 0 or self.velocity_y != 0:
            self.state = "run"
            length = math.hypot(self.velocity_x, self.velocity_y)
            if length > 0:
                scale = self.speed * dt / length
                self.x += self.velocity_x * scale
                self.y += self.velocity_y * scale
        else:
            self.state = "idle"

        self.x = max(20, min(WIDTH - 20, self.x))
        self.y = max(20, min(HEIGHT - 20, self.y))

    def update(self, dt):
        self.move(dt)
        self.animate(dt)

class Hero(Character):
    def __init__(self, pos):
        super().__init__("hero", pos, speed=200)

    def handle_input(self):
        self.velocity_x = 0
        self.velocity_y = 0
        if keyboard.left: self.velocity_x = -1
        elif keyboard.right: self.velocity_x = 1
        if keyboard.up: self.velocity_y = -1
        elif keyboard.down: self.velocity_y = 1

class Enemy(Character):
    def __init__(self, pos, territory_radius=150):
        super().__init__("enemy", pos, speed=100)
        self.start_pos = pos
        self.territory_radius = territory_radius
        self.target_pos = self.get_new_target()
        self.wait_timer = 0

    def get_new_target(self):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, self.territory_radius)
        return (self.start_pos[0] + math.cos(angle) * distance, 
                self.start_pos[1] + math.sin(angle) * distance)

    def update_ai(self, dt):
        if self.wait_timer > 0:
            self.wait_timer -= dt
            self.velocity_x = 0
            self.velocity_y = 0
            return

        dx = self.target_pos[0] - self.x
        dy = self.target_pos[1] - self.y
        dist = math.hypot(dx, dy)

        if dist < 5:
            self.wait_timer = random.uniform(0.5, 1.5)
            self.target_pos = self.get_new_target()
        else:
            self.velocity_x = dx
            self.velocity_y = dy

    def update(self, dt):
        self.update_ai(dt)
        super().update(dt)

# --- NEW CLASS: COIN ---
class Coin:
    def __init__(self, pos):
        self.actor = Actor("coin", pos)
        
    def draw(self):
        self.actor.draw()

# --- GAME INSTANCES ---
hero = Hero((WIDTH // 2, HEIGHT // 2))
enemies = []
coins = []  # <--- LISTA DE MOEDAS

# Menu Buttons
btn_start = Rect((WIDTH//2 - 100, 250), (200, 50))
btn_sound = Rect((WIDTH//2 - 100, 320), (200, 50))
btn_exit = Rect((WIDTH//2 - 100, 390), (200, 50))

# --- HELPER FUNCTIONS ---

def setup_game():
    global enemies, hero, game_state, coins, score
    score = 0
    hero.x, hero.y = (100, 300)
    
    enemies = []
    enemies.append(Enemy((400, 150), territory_radius=100))
    enemies.append(Enemy((600, 300), territory_radius=120))
    enemies.append(Enemy((400, 500), territory_radius=100))
    
    # Criar 5 moedas em posições aleatórias 
    coins = []
    for _ in range(5):
        cx = random.randint(200, WIDTH - 50)
        cy = random.randint(50, HEIGHT - 50)
        coins.append(Coin((cx, cy)))
        
    game_state = STATE_PLAYING

def toggle_sound():
    global sound_enabled, current_music_playing
    sound_enabled = not sound_enabled
    if sound_enabled:
        if not current_music_playing:
            try: music.play("music"); current_music_playing = True
            except: pass
    else:
        music.stop(); current_music_playing = False

def play_sound_effect(name):
    if sound_enabled:
        try: sounds[name].play()
        except: pass

# --- PGZERO HOOKS ---

def update(dt):
    global game_state, score

    if game_state == STATE_PLAYING:
        hero.handle_input()
        hero.update(dt)

        # Update Enemies
        for enemy in enemies:
            enemy.update(dt)
            if hero.actor.colliderect(enemy.actor):
                play_sound_effect("click") 
                game_state = STATE_GAMEOVER
                if sound_enabled: music.stop()

        # Update Coins (Coleta)
        for coin in coins[:]: 
            if hero.actor.colliderect(coin.actor):
                coins.remove(coin)
                score += 10
                play_sound_effect("click")
                
        # Win condition (opcional)
        if len(coins) == 0 and len(enemies) > 0:
            pass

def draw():
    screen.clear()

    if game_state == STATE_MENU:
        try: screen.blit("menu_bg", (0, 0))
        except: screen.fill(COLOR_BUTTON)
        
        screen.draw.text(TITLE.upper(), center=(WIDTH//2, 150), fontsize=60, 
                         color=COLOR_WHITE, owidth=1, ocolor=COLOR_TEXT_SHADOW)

        for rect, text in [(btn_start, "START GAME"), 
                           (btn_sound, f"SOUND: {'ON' if sound_enabled else 'OFF'}"), 
                           (btn_exit, "EXIT")]:
            screen.draw.filled_rect(rect, COLOR_BUTTON)
            screen.draw.rect(rect, COLOR_WHITE)
            screen.draw.text(text, center=rect.center, fontsize=30, color=COLOR_WHITE)

    elif game_state == STATE_PLAYING:
        try: screen.blit("tile_floor", (0, 0))
        except: screen.fill((20, 20, 40))

        # Desenha itens
        for coin in coins:
            coin.draw()

        # Desenha personagens
        hero.draw()
        for enemy in enemies:
            enemy.draw()
            
        # --- DESENHA O SCORE (MARCADOR DE PONTOS) ---
        screen.draw.text(f"SCORE: {score}", (20, 20), fontsize=40, 
                         color=COLOR_GOLD, owidth=1.5, ocolor="black")

    elif game_state == STATE_GAMEOVER:
        screen.fill(COLOR_BLACK)
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2 - 50), 
                         fontsize=80, color="red")
        screen.draw.text(f"Final Score: {score}", center=(WIDTH//2, HEIGHT//2 + 20), 
                         fontsize=50, color=COLOR_GOLD)
        screen.draw.text("Click to Return to Menu", center=(WIDTH//2, HEIGHT//2 + 80), 
                         fontsize=30, color=COLOR_WHITE)

def on_mouse_down(pos):
    global game_state
    
    if game_state == STATE_MENU:
        if btn_start.collidepoint(pos):
            play_sound_effect("click")
            setup_game()
        elif btn_sound.collidepoint(pos):
            play_sound_effect("click")
            toggle_sound()
        elif btn_exit.collidepoint(pos):
            quit()
            
    elif game_state == STATE_GAMEOVER:
        game_state = STATE_MENU
        if sound_enabled: 
            try: music.play("music")
            except: pass

if sound_enabled:
    try: music.play("music")
    except: pass

pgzrun.go()
