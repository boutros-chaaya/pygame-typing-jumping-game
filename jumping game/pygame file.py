import pygame
import sys
import random


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load(
            'Graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load(
            'Graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load(
            'Graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('Audio/jump.mp3')
        self.jump_sound.set_volume(0.08)

    def player_input(self):
        global key
        keys = pygame.key.get_pressed()
        letters = 'abcdefghijklmnopqrstuvwxyz'

        # print(key[1])
        if keys[key[1]] and self.rect.bottom >= 300:
            self.gravity = -17
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('Graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('Graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            self.type = 'Fly'
            y_pos = 210
        else:
            snail_1 = pygame.image.load(
                'Graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load(
                'Graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            self.type = 'Snail'
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(
            midbottom=(random.randint(900, 1100), y_pos))
        self.key = self.get_key()

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def get_key(self):
        #global key
        values = [i for i in range(97, 122)]
        key = random.choice(values)
        letters = 'abcdefghijklmnopqrstuvwxyz'
        letter = letters[key - 97]

        return letter, key

    def update(self):
        self.animation_state()
        self.get_key()
        self.rect.x -= 7 + display_score() / 10
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def __repr__(self):
        return self.type


def draw_text(text, font, font_color, x, y):
    img = font.render(text, True, font_color)
    img_rect = img.get_rect(center=(x, y))
    screen.blit(img, img_rect)


def draw_image(img, x, y, scale=(0, 0)):
    # next line is so that if there is no scale parameter passed the image would not transform
    if scale != (0, 0):
        img = pygame.transform.scale(img, scale)
    rect = img.get_rect(center=(x, y))
    screen.blit(img, rect)


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, color2)
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_movement(obstacle_list):

    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 7

        if obstacle_rect.bottom == 300:
            screen.blit(snail_surf, obstacle_rect)
        else:
            screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [
            obstacle for obstacle in obstacle_list if obstacle.x > -100]


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]


pygame.init()
sw, sh = 800, 400
screen = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("Boutros' Jumping Game")
clock = pygame.time.Clock()
FPS = 60
test_font = pygame.font.Font(None, 50)
font_color = (111, 196, 169)
color2 = (64, 64, 64)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('Audio/24 Relaxxx.mp3')
bg_music.set_volume(0.08)
bg_music.play(loops = -1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('Graphics/Sky.png').convert()
ground_surface = pygame.image.load('Graphics/ground.png').convert()

# score_surf = test_font.render('My game', False, (64,64,64))
# score_rect = score_surf.get_rect(center = (400,50))

# Snail
snail_frame_1 = pygame.image.load('Graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('Graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# Fly
fly_frame1 = pygame.image.load('Graphics/fly/fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('Graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []


player_walk_1 = pygame.image.load(
    'Graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load(
    'Graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('Graphics/player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_gravity = 0

# Intro screen
player_stand = pygame.image.load(
    'Graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render('Boutros Jumping Game', False, font_color)
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render('Press space to start', False, font_color)
game_message_rect = game_message.get_rect(center=(400, 330))
scores = [0]
high_score = 0

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 2000)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

# keys

key = (0, 32)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -0

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True

                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(random.choice(
                    ['fly', 'snail', 'snail', 'snail'])))
                # print(obstacle_group.sprites())
                key = obstacle_group.sprites()[0].get_key()
                # print(key[0])
                # draw_text(str(key[0]), test_font, color2, 100, 100)

                # if random.randint(0,2):
                # 	obstacle_rect_list.append(snail_surf.get_rect(bottomright = (random.randint(900,1100),300)))
                # else:
                # 	obstacle_rect_list.append(fly_surf.get_rect(bottomright = (random.randint(900,1100),210)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        #screen.blit(ground_surface, (600, 300))
        
        # pygame.draw.rect(screen,'#c0e8ec',score_rect)
        # pygame.draw.rect(screen,'#c0e8ec',score_rect,10)
        # screen.blit(score_surf,score_rect)
        score = display_score()
        # rect_image = pygame.image.load('Graphics/rect3.png').convert_alpha()
        # draw_image(rect_image, 80, 80)
        draw_text(str(key[0]).upper(), test_font, color2, 80, 80)
        # rectangle = pygame.Rect(100, 100, 50, 75)
        # pygame.draw.rect(screen, (color2), rectangle)

        # snail_rect.x -= 4
        # if snail_rect.right <= 0: snail_rect.left = 800
        # screen.blit(snail_surf,snail_rect)

        # Player
        # player_gravity += 1
        # player_rect.y += player_gravity
        # if player_rect.bottom >= 300: player_rect.bottom = 300
        # player_animation()
        # screen.blit(player_surf,player_rect)
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()
        # player.player_input()

        # Obstacle movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collision
        game_active = collision_sprite()
        # game_active = collisions(player_rect,obstacle_rect_list)

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0
        

        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rect)
        
        if score > 0:
        	scores.append(score)
        	#score = 0
        	#print(scores)

        high_score = max(scores)
        #print(high_score)

        if score < 1:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
        draw_text(f'High Score: {str(high_score)}', test_font, font_color, 400, 375)

    pygame.display.update()
    clock.tick(FPS)
