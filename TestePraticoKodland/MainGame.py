import pgzrun
import random

TITLE = 'Teste Prático Kodland'
WIDTH = 1280
HEIGHT = 720

# 0 = Main menu; 1 = Game
game_state = 0
sound_active = 1

# Menu Principal:

class Button:
    def __init__(self,display_text,x,y):
        self.actor = Actor('grey_button')
        self.actor.pos = (x,y)
        self.text = display_text
    def draw(self):
        self.actor.draw()
        screen.draw.text(self.text, center=(self.actor.pos), fontsize=60,  color='black')

class MainMenu:
    def __init__(self):
        self.button_spacing = 80
        self.buttons_offset = 50
        self.play_button = Button('Jogar',WIDTH/2,(HEIGHT/2) - self.button_spacing + self.buttons_offset)
        self.sound_button = Button('Som: ON', WIDTH / 2, (HEIGHT / 2) + self.buttons_offset)
        self.quit_button = Button('Sair', WIDTH / 2, (HEIGHT / 2) + self.button_spacing + self.buttons_offset)
        self.instructions = 'A e D para se mover\nBarra de Espaço para pular, segure para pular mais alto\nPule na cabeça dos inimigos para derrotá-los\nInimigos terrestres dão 1 ponto, inimigos aéreos dão 2'

        global sound_active

    def is_hovering(self,actor, pos):
        if (pos[0] >= actor.midleft[0] and pos[0] <= actor.midright[0]) and pos[1] >= actor.midtop[1] and pos[1] <= actor.midbottom[1]:
            return True
        else:
            return False
    def mouse_click(self,pos):
        if game_state == 0:
            if self.is_hovering(self.play_button.actor,pos):
                start_game()
            if self.is_hovering(self.sound_button.actor,pos):
                toggle_sounds()
                if sound_active:
                    self.sound_button.text = 'Som: ON'
                else:
                    self.sound_button.text = 'Som: OFF'
            if self.is_hovering(self.quit_button.actor,pos):
                exit()
    def mouse_hover(self,pos):
        if game_state == 0:
            if self.is_hovering(self.play_button.actor,pos):
                self.play_button.actor.image = 'grey_button_hovered'
            else:
                self.play_button.actor.image = 'grey_button'
            if self.is_hovering(self.sound_button.actor, pos):
                self.sound_button.actor.image = 'grey_button_hovered'
            else:
                self.sound_button.actor.image = 'grey_button'
            if self.is_hovering(self.quit_button.actor,pos):
                self.quit_button.actor.image = 'grey_button_hovered'
            else:
                self.quit_button.actor.image = 'grey_button'
    def draw(self):
        screen.draw.text('Teste Prático Kodland', center=(WIDTH/2,200), fontsize=100, color='white',owidth = 1,ocolor = 'black')
        self.play_button.draw()
        self.sound_button.draw()
        self.quit_button.draw()
        screen.draw.text(self.instructions, bottomleft=(10, HEIGHT-10), fontsize=50, owidth=1, ocolor='black')

menu = MainMenu()
def on_mouse_down(pos):
    menu.mouse_click(pos)
    death_menu.mouse_click(pos)
def on_mouse_move(pos):
    menu.mouse_hover(pos)
    death_menu.mouse_hover(pos)

# Jogo Principal:

enemies_in_level = []
particles_in_level = []

class Level:
    def __init__(self):
        self.solid_blocks = []
        self.tile_size = 64
        self.tilemap = [
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', 'G', '.', 'G', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', 'R', 'R', 'R', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', 'G', 'G', 'G', 'G', '.', '.', '.', 'G', 'G', 'G', 'G', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['R', 'R', 'R', 'R', 'R', 'R', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'R', 'R', 'R', 'R', 'R', 'R'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', 'R', 'R', 'R', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', 'F', 'F', 'F', '.', '.', '.', '.', '.', '.', '.', 'F', 'F', 'F', '.', '.', '.', '.'],
            ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', '.', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F']
        ]
        self.build_tilemap()

    def build_tilemap(self):
        for row_index, row in enumerate(self.tilemap):
            for block_index, block in enumerate(row):
                if block == 'R':
                    box = Actor('red_block')
                    box.pos = (block_index * self.tile_size, row_index * self.tile_size)
                    self.solid_blocks.append(box)
                elif block == 'G':
                    box = Actor('green_block')
                    box.pos = (block_index * self.tile_size, row_index * self.tile_size)
                    self.solid_blocks.append(box)
                elif block == 'F':
                    previous_row = self.tilemap[row_index - 1]
                    if previous_row[block_index] == 'F':
                        ground = Actor('ground')
                    elif row[block_index-1] != 'F':
                        ground = Actor('top_left_ground')
                    elif block_index == len(row) - 1 or row[block_index+1] != 'F':
                        ground = Actor('top_right_ground')
                    else:
                        ground = Actor('top_ground')
                    ground.pos = (block_index * self.tile_size, row_index * self.tile_size)
                    self.solid_blocks.append(ground)
    def draw(self):
        for block in self.solid_blocks:
            block.draw()
level = Level()

class DeathMenu():
    def __init__(self):
        self.button_spacing = 80
        self.buttons_offset = 50
        self.menu_button = Button('Reiniciar', WIDTH / 2, (HEIGHT / 2) - self.button_spacing + self.buttons_offset)
        self.sound_button = Button('Som: ON', WIDTH / 2, (HEIGHT / 2) + self.buttons_offset)
        self.quit_button = Button('Sair', WIDTH / 2, (HEIGHT / 2) + self.button_spacing + self.buttons_offset)
    def is_hovering(self,actor, pos):
        if (pos[0] >= actor.midleft[0] and pos[0] <= actor.midright[0]) and pos[1] >= actor.midtop[1] and pos[1] <= actor.midbottom[1]:
            return True
        else:
            return False
    def mouse_click(self,pos):
        global game_state
        if game_state == 1 and player.life_state == 0:
            if self.is_hovering(self.menu_button.actor,pos):
                restart_game()
            if self.is_hovering(self.sound_button.actor,pos):
                toggle_sounds()
                if sound_active:
                    self.sound_button.text = 'Som: ON'
                else:
                    self.sound_button.text = 'Som: OFF'
            if self.is_hovering(self.quit_button.actor,pos):
                exit()
    def mouse_hover(self,pos):
        if game_state == 1 and player.life_state == 0:
            if self.is_hovering(self.menu_button.actor,pos):
                self.menu_button.actor.image = 'grey_button_hovered'
            else:
                self.menu_button.actor.image = 'grey_button'
            if self.is_hovering(self.sound_button.actor, pos):
                self.sound_button.actor.image = 'grey_button_hovered'
            else:
                self.sound_button.actor.image = 'grey_button'
            if self.is_hovering(self.quit_button.actor,pos):
                self.quit_button.actor.image = 'grey_button_hovered'
            else:
                self.quit_button.actor.image = 'grey_button'
    def draw(self):
        self.menu_button.draw()
        self.sound_button.draw()
        self.quit_button.draw()
        screen.draw.text('GAME OVER',center=(WIDTH/2,125), fontsize=50,owidth = 3,ocolor = 'black')
        screen.draw.text(str(player.points), center=(WIDTH / 2, 225), fontsize=150,owidth = 1,ocolor = 'black')
death_menu = DeathMenu()

class Player:
    def __init__(self,x,y):
        self.collision_threshold = 10
        self.actor = Actor('player_idle_01')
        self.actor.pos = (x,y)
        self.walk_speed = 6
        self.actor.velocity_y = 0
        self.gravity = 0.4
        self.jump_velocity = -13
        self.grounded = False
        # 0 = Defeated; 1 = Alive
        self.life_state = 1
        # Points
        self.points = 0
    def update(self):
        if self.life_state == 1:
            if self.actor.y > WIDTH + self.actor.height:
                self.defeat_player()
            if keyboard.D:
                animation.animator_state = 1
                self.actor.x = self.actor.x + self.walk_speed
                for block in level.solid_blocks:
                    if self.actor.colliderect(block):
                        if block.x > self.actor.x:
                            self.actor.x = (block.x - block.width / 2 - self.actor.width / 2)
            if self.actor.x > WIDTH + self.actor.width / 2:
                self.actor.x = -self.actor.width / 2
            if keyboard.A:
                animation.animator_state = 2
                self.actor.x = self.actor.x - self.walk_speed
                for block in level.solid_blocks:
                    if self.actor.colliderect(block):
                        if block.x < self.actor.x:
                            self.actor.x = (block.x + block.width / 2 + self.actor.width / 2)
                if self.actor.x < -self.actor.width / 2:
                    self.actor.x = WIDTH + self.actor.width / 2
            self.actor.y += self.actor.velocity_y

            for block in level.solid_blocks:
                if self.actor.colliderect(block):
                    if self.actor.velocity_y >= 1:
                        self.actor.velocity_y = 0
                    if (keyboard.A == False and keyboard.D == False) or (keyboard.A and keyboard.D):
                        animation.animator_state = 0
                        pass
                    if block.y > self.actor.y:
                        self.grounded = True
                        self.actor.y = block.y - block.height / 2 - self.actor.height / 2
                    elif block.y < self.actor.center[1]:
                        self.actor.y = block.y + block.height / 2 + self.actor.height / 2
                        self.actor.velocity_y = 0
                        self.actor.velocity_y += self.gravity
                    else:
                        self.grounded = False
                    break
                self.grounded = False
            if not self.grounded:
                animation.animator_state = 3
                self.actor.velocity_y += self.gravity
        else:
            animation.animator_state = 4
    def draw(self):
        self.actor.draw()
        if self.life_state == 1:
            screen.draw.text(str(player.points), center=(WIDTH/2,75),fontsize = 150,owidth = 1,ocolor = 'black')
    def defeat_player(self):
        self.life_state = 0
        animation.defeat_animation()
        if sound_active:
            sounds.defeat.play()
    def key_up(self,key):
        if key == key.SPACE and self.actor.velocity_y < -1:
            self.actor.velocity_y = self.jump_velocity / 4
    def key_down(self, key):
        if key == key.SPACE and self.grounded:
            self.jump()
    def jump(self):
        if sound_active:
            if self.grounded:
                sounds.jump.play()
        self.grounded = False
        self.actor.velocity_y = self.jump_velocity
    def bounce(self):
        self.grounded = False
        self.actor.velocity_y = self.jump_velocity / 2
starting_position = (WIDTH/2,455)
player = Player(starting_position[0],starting_position[1])
current_animate = None
class PlayerAnimation:
    def __init__(self):
        # 0 = Idle; 1 = Walk right; 2 = Walk left; 3 = Jump
        self.animator_state = 0
        self.old_state = 0
        self.frame_index = 0
        self.player_idle = ['player_idle_01', 'player_idle_02', 'player_idle_03', 'player_idle_04', 'player_idle_05',
                       'player_idle_06']
        self.player_walk_right = ['player_walk_right_01', 'player_walk_right_02', 'player_walk_right_03',
                             'player_walk_right_04']
        self.player_walk_left = ['player_walk_left_01', 'player_walk_left_02', 'player_walk_left_03', 'player_walk_left_04']
        self.player_jump = ['player_jump_01', 'player_jump_02', 'player_jump_03', 'player_jump_04']
        self.player_anim_speed = 0.2
    def update(self):
        if self.animator_state == 0:
            if self.old_state != 0:
                self.frame_index = 0
            self.old_state = 0
            self.frame_index += self.player_anim_speed
            if self.frame_index >= len(self.player_idle):
                self.frame_index = 0
            player.actor.image = self.player_idle[int(self.frame_index)]
        elif self.animator_state == 1:
            if self.old_state != 1:
                self.frame_index = 0
            self.old_state = 1
            self.frame_index += self.player_anim_speed
            if self.frame_index >= len(self.player_walk_right):
                self.frame_index = 0
            player.actor.image = self.player_walk_right[int(self.frame_index)]
        elif self.animator_state == 2:
            if self.old_state != 2:
                self.frame_index = 0
            self.old_state = 2
            self.frame_index += self.player_anim_speed
            if self.frame_index >= len(self.player_walk_left):
                self.frame_index = 0
            player.actor.image = self.player_walk_left[int(self.frame_index)]
        elif self.animator_state == 3:
            if self.old_state != 3:
                self.frame_index = 0
            self.old_state = 3
            if self.frame_index < len(self.player_jump) - 1:
                self.frame_index += self.player_anim_speed * 1.5
            player.actor.image = self.player_jump[int(self.frame_index)]
        elif self.animator_state == 4:
            self.frame_index = 0
            self.old_state = 4
            player.actor.image = ('player_dead')
    def defeat_animation(self):
        global current_animate
        if not current_animate:
            current_animate = animate(player.actor,tween = 'decelerate',duration = 0.3,on_finished = self.fall_animation, pos=(player.actor.x, player.actor.y - 100))
    def fall_animation(self):
        global current_animate
        current_animate = animate(player.actor,tween = 'accelerate',duration =1.0, pos=(player.actor.x, player.actor.y + HEIGHT))
animation = PlayerAnimation()

class Enemy:
    def __init__(self,x,y):
        self.actor = Actor('enemy_walk_01')
        self.actor.pos = (x,y)
        self.grounded = False
        self.gravity = 1
        self.actor.velocity_y = 0
        self.walk_speed = 3
        self.previous_x = self.actor.x
        self.actor.velocity_x = 0
        #---------------------
        self.frame_index = 0
        self.walk_frames = ['enemy_walk_01','enemy_walk_02']
        self.idle_frames = ['enemy_idle_01','enemy_idle_02','enemy_idle_03','enemy_idle_04','enemy_idle_05']
        # 0 = Idle; 1 = Walk; 2 = Jump
        self.animator_state = 0
    def update(self):
        self.actor.velocity_x = self.actor.x - self.previous_x
        self.previous_x = self.actor.x
        self.frame_index += 0.2
        if self.animator_state == 0:
            if self.frame_index >= len(self.idle_frames):
                self.frame_index = 0
            self.actor.image = self.idle_frames[int(self.frame_index)]
        if self.animator_state == 1:
            if self.frame_index >= len(self.walk_frames):
                self.frame_index = 0
            self.actor.image = self.walk_frames[int(self.frame_index)]
        elif self.animator_state == 2:
            self.actor.image = 'enemy_jump'
        if self.actor.y > HEIGHT:
            enemies_in_level.remove(self)
        if player.actor.colliderect(self.actor):
            if player.life_state == 1:
                if player.actor.midbottom[1] < self.actor.y:
                    if keyboard.SPACE:
                        player.jump()
                    else:
                        player.bounce()
                    particles_in_level.append(EnemyDefeatParticles(self.actor.x,self.actor.y))
                    if sound_active:
                        sounds.stomp_enemy.play()
                    player.points = player.points + 1
                    enemies_in_level.remove(self)
                else:
                    player.defeat_player()
        for block in level.solid_blocks:
            if block.midright[0] > self.actor.x > block.midleft[0] and block.midtop[1] < self.actor.y < block.midbottom[1]:
                self.actor.y = block.y - self.actor.height
            if self.actor.colliderect(block):
                if self.actor.velocity_y >= 1:
                    self.actor.velocity_y = 0
                if block.y > self.actor.y:
                    self.grounded = True
                    self.actor.y = block.y - block.height / 2 - self.actor.height / 2
                elif block.y < self.actor.center[1]:
                    self.actor.y = block.y + block.height / 2 + self.actor.height / 2
                    self.actor.velocity_y = 0
                    self.actor.velocity_y += self.gravity
                else:
                    self.grounded = False
                break
            self.grounded = False
        if self.actor.x <= 0 or self.actor.x > WIDTH:
            self.grounded = True
        if not self.grounded:
            self.actor.velocity_y += self.gravity
        if looped_direction(self.actor,player.actor) > 0:
            self.try_go_right()
        elif looped_direction(self.actor,player.actor) < 0:
            self.try_go_left()
        self.actor.y += self.actor.velocity_y
        if self.grounded:
            if self.actor.velocity_x == 0:
                self.animator_state = 0
            else:
                self.animator_state = 1
        if self.actor.velocity_y > 5 or self.actor.velocity_y < -5:
            self.animator_state = 2
        for enemy in enemies_in_level:
            if self.actor.colliderect(enemy.actor):
                if enemy != self:
                    if enemy.actor.x + 2 > self.actor.x > enemy.actor.x - 2:
                        if random.randint(1,2) == 1:
                            self.actor.x = self.actor.x - self.actor.width/2
                        else:
                            self.actor.x = self.actor.x + self.actor.width / 2


    def try_go_right(self):
        self.actor.x = self.actor.x + self.walk_speed
        for enemy in enemies_in_level:
            if self.actor.colliderect(enemy.actor):
                if enemy != self:
                    if enemy.actor.x > self.actor.x or enemy.actor.x == self.actor.x:
                        self.actor.x = (enemy.actor.x - enemy.actor.width / 2 - self.actor.width / 2)
                        break
        for block in level.solid_blocks:
            if self.actor.colliderect(block):
                if block.x > self.actor.x:
                    self.actor.x = (block.x - block.width / 2 - self.actor.width / 2)
                    if self.grounded:
                        self.jump()
                    break
        if self.actor.x > WIDTH + self.actor.width / 2:
            self.actor.x = -self.actor.width / 2
    def try_go_left(self):
        self.actor.x = self.actor.x - self.walk_speed
        for enemy in enemies_in_level:
            if self.actor.colliderect(enemy.actor):
                if enemy != self:
                    if enemy.actor.x < self.actor.x or enemy.actor.x == self.actor.x:
                        self.actor.x = (enemy.actor.x + enemy.actor.width / 2 + self.actor.width / 2)
                        break
        for block in level.solid_blocks:
            if self.actor.colliderect(block):
                if block.x < self.actor.x:
                    self.actor.x = (block.x + block.width / 2 + self.actor.width / 2)
                    if self.grounded:
                        self.jump()
                    break
        if self.actor.x < -self.actor.width / 2:
            self.actor.x = WIDTH + self.actor.width / 2
    def jump(self):
        self.actor.velocity_y = -15

    def draw(self):
        self.actor.draw()
class EnemyDefeatParticles:
    def __init__(self,x,y):
        self.frame_index = 0
        self.actor = Actor('enemy_defeated_01')
        self.actor.pos = (x,y)
        self.idle_frames = ['enemy_defeated_01','enemy_defeated_02','enemy_defeated_03','enemy_defeated_04','enemy_defeated_05','enemy_defeated_06']
    def update(self):
        self.frame_index += 0.5
        if self.frame_index >= len(self.idle_frames) - 1:
            particles_in_level.remove(self)
        self.actor.image = self.idle_frames[int(self.frame_index)]
    def draw(self):
        self.actor.draw()
class FlyingEnemy:
    def __init__(self,x,y):
        self.actor = Actor('flying_enemy_01')
        self.actor.pos = (x,y)
        self.grounded = False
        self.fly_speed = 5
        self.actor.angle = 0
        #-------------------
        self.frame_index = 0
        self.frames = ['flying_enemy_01', 'flying_enemy_02', 'flying_enemy_03', 'flying_enemy_04']
    def update(self):
        self.frame_index += 0.1
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.actor.image = self.frames[int(self.frame_index)]
        if self.actor.y > HEIGHT:
            enemies_in_level.remove(self)
        if player.actor.colliderect(self.actor):
            if player.life_state == 1:
                if player.actor.midbottom[1] < self.actor.y:
                    if keyboard.SPACE:
                        player.jump()
                    else:
                        player.bounce()
                    if sound_active:
                        sounds.stomp_enemy.play()
                    particles_in_level.append(FlyingEnemyDefeatParticles(self.actor.x, self.actor.y))
                    enemies_in_level.remove(self)
                    player.points = player.points + 2
                else:
                    player.defeat_player()
        if player.actor.y > self.actor.y:
            self.actor.y = self.actor.y + 1
        elif player.actor.y < self.actor.y:
            self.actor.y = self.actor.y - 1
        if looped_direction(self.actor, player.actor) > 0:
            self.actor.x = self.actor.x + 1
            if self.actor.x > WIDTH + self.actor.width / 2:
                self.actor.x = -self.actor.width / 2
        elif looped_direction(self.actor, player.actor) < 0:
            self.actor.x = self.actor.x - 1
            if self.actor.x < -self.actor.width / 2:
                self.actor.x = WIDTH + self.actor.width / 2
        self.actor.angle += 2

    def draw(self):
        self.actor.draw()
class FlyingEnemyDefeatParticles:
    def __init__(self,x,y):
        self.frame_index = 0
        self.actor = Actor('flying_enemy_defeated_01')
        self.actor.pos = (x,y)
        self.idle_frames = ['flying_enemy_defeated_01','flying_enemy_defeated_02','flying_enemy_defeated_03','flying_enemy_defeated_04','flying_enemy_defeated_05','flying_enemy_defeated_06']
    def update(self):
        self.frame_index += 0.5
        if self.frame_index >= len(self.idle_frames) - 1:
            particles_in_level.remove(self)
        self.actor.image = self.idle_frames[int(self.frame_index)]
    def draw(self):
        self.actor.draw()

def spawn_enemy():
    if game_state == 1 and player.life_state == 1:
        if len(enemies_in_level) < 15:
            if random.randint(1,10) < 4:
                enemies_in_level.append(FlyingEnemy(random.randint(0,WIDTH), -50))
            else:
                enemies_in_level.append(Enemy(WIDTH/2, -22))
def looped_direction(first_actor,second_actor):
    if second_actor.x > first_actor.x:
        if ((WIDTH - second_actor.x) + first_actor.x) < second_actor.x - first_actor.x:
            return -1
        else:
            return 1
    if second_actor.x < first_actor.x:
        if (second_actor.x + (WIDTH - first_actor.x)) < first_actor.x - second_actor.x:
            return 1
        else:
            return -1
    return 0

# Transição:

def start_game():
    global game_state
    game_state = 1
    player.life_state = 1
    player.actor.pos = (starting_position[0],starting_position[1])
    if sound_active:
        sounds.bg_music.set_volume(0.2)
        death_menu.sound_button.text = 'Som: ON'
    else:
        sounds.bg_music.set_volume(0)
        death_menu.sound_button.text = 'Som: OFF'
    sounds.bg_music.play(-1)
    #enemies_in_level.append(FlyingEnemy(600, 300))
    clock.schedule_interval(spawn_enemy, 1.0)

def restart_game():
    global current_animate
    if current_animate is not None and current_animate.running:
        current_animate.stop()
    current_animate = None
    sounds.defeat.stop()
    player.life_state = 1
    enemies_in_level.clear()
    player.actor.pos = (starting_position[0], starting_position[1])
    player.points = 0
# Genérico:

def update():
    if game_state == 0:
        pass
    elif game_state == 1:
        player.update()
        animation.update()
        for enemy in enemies_in_level:
            enemy.update()
        for particle in particles_in_level:
            particle.update()

def draw():
    screen.fill((84, 68, 123))
    if game_state == 0:
        menu.draw()
    elif game_state == 1:
        level.draw()
        for enemy in enemies_in_level:
            enemy.draw()
        for particle in particles_in_level:
            particle.draw()
        player.draw()
        if player.life_state == 0:
            death_menu.draw()

def on_key_up(key):
    if game_state == 1:
        player.key_up(key)

def on_key_down(key):
    global game_state
    if game_state == 0:
        if key == key.RETURN:
            start_game()
    if game_state == 1:
        player.key_down(key)

def toggle_sounds():
    global sound_active
    if sound_active:
        sound_active = False
        sounds.bg_music.set_volume(0)
        sounds.defeat.set_volume(0)
        sounds.jump.set_volume(0)
        sounds.stomp_enemy.set_volume(0)
    else:
        sound_active = True
        sounds.bg_music.set_volume(0.2)
        sounds.defeat.set_volume(0.3)
        sounds.jump.set_volume(1)
        sounds.stomp_enemy.set_volume(1)


pgzrun.go()