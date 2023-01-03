import pygame
from sys import exit
from random import randint

# initialize
pygame.init()
pygame.display.set_caption("Boutros' Jumping Game")
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
original_font = pygame.font.Font(None, 50)
controls_font = pygame.font.Font(None, 30)
game_active = False
start_time = 0
obstacle_speed = 10


# score
def display_score():
    current_time = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surface = original_font.render(str(current_time), True, "Black")
    score_rectangle_ = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rectangle_)
    return current_time


def obstacle_movement(obstacle_list, speed):
    if obstacle_list:

        for obstacle_rect in obstacle_list:

            obstacle_rect.x -= speed
            if (int((pygame.time.get_ticks() - start_time) / 1000)) % 5 == 0:
                speed += 1
            # print(speed)
            # screen.blit(snail_surface, obstacle_rect)

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)

            else:
                screen.blit(fly_surface, obstacle_rect)

            obstacle_list = [
                obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


def player_animation():
    global player_surface, player_index
    if player_rectangle.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]
    # Player walking animation if player is on the floor
    # Display the player jumping in player is not on the floor


#  score_count = 0
# score_surface = original_font.render(str(current_time), True, (64, 64, 64))
# score_rectangle = score_surface.get_rect(center=(400, 50))


score = display_score()

# sky and ground origin
sky_surface = pygame.image.load("Graphics/sky.png").convert()
ground_surface = pygame.image.load("Graphics/ground.png").convert()

# obstacles
# snail
snail_frame_1 = pygame.image.load("Graphics/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("Graphics/snail2.png").convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

# fly
fly_frame_1 = pygame.image.load("Graphics/Fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("Graphics/Fly2.png").convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rect_list = []


# player walking animation
player_walk_1 = pygame.image.load(
    "Graphics/Player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load(
    "Graphics/Player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load("Graphics/Player/jump.png").convert_alpha()

player_surface = player_walk[player_index]
player_gravity = 0
player_rectangle = player_surface.get_rect(midbottom=(80, 300+player_gravity))

# player intro screen
player_stand = pygame.image.load(
    "Graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rectangle = player_stand.get_rect(center=(400, 200))

# game name
game_name_surface = original_font.render(
    "Boutros' Jumping Game", True, (111, 196, 169))
game_name_rectangle = game_name_surface.get_rect(center=(400, 75))

# controls n1
controls_surface = controls_font.render(
    "Press S to start, W, UP or SPACE to jump", True, (111, 196, 169))
controls_rectangle = controls_surface.get_rect(center=(400, 320))

# controls n2
controls2_surface = original_font.render(
    "Press S to restart!", True, (111, 196, 169))
controls2_rectangle = controls_surface.get_rect(center=(450, 350))

# game over image
dancing_dragons_surface = pygame.image.load(
    "Graphics/Player/dancing dragons.jpg").convert_alpha()
dancing_dragons_rectangle = dancing_dragons_surface.get_rect(center=(400, 200))

# game over
game_over_surface = original_font.render("Game Over", True, "Brown")
game_over_rectangle = game_over_surface.get_rect(midbottom=(400, 200))

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rectangle.collidepoint(event.pos):
                    player_gravity = -20

            if event.type == pygame.KEYDOWN and player_rectangle.bottom >= 300:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                    player_gravity = -17

            if game_active:
                if event.type == obstacle_timer:
                    if randint(0, 2):
                        obstacle_rect_list.append(snail_surface.get_rect(
                            midbottom=(randint(900, 1100), 300)))
                    else:
                        obstacle_rect_list.append(fly_surface.get_rect(
                            midbottom=(randint(900, 1100), 210)))
                if event.type == snail_animation_timer:
                    if snail_frame_index == 0:
                        snail_frame_index = 1
                    else:
                        snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    game_active = True

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        # pygame.draw.rect(screen, "#c0e8ec", score_rectangle)
        # pygame.draw.rect(screen, "#c0e8ec", score_rectangle, 10)
        score = display_score()

        # ground
        player_gravity += 1
        player_rectangle.y += player_gravity
        # player
        if player_rectangle.bottom >= 300:
            player_rectangle.bottom = 300
        player_animation()
        screen.blit(player_surface, player_rectangle)

        # obstacle moving to the left
        obstacle_rect_list = obstacle_movement(obstacle_rect_list, obstacle_speed)

        # collision
        game_active = collisions(player_rectangle, obstacle_rect_list)

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rectangle)
        obstacle_rect_list.clear()
        player_rectangle.midbottom = (80, 300)
        player_gravity = 0
        score_message = original_font.render(f"Your Score: {score}", True, (111, 196, 169))
        score_rectangle = score_message.get_rect(center=(400, 320))
        if score != 0:
            screen.blit(score_message, score_rectangle)
            screen.blit(controls2_surface, controls2_rectangle)
        else:
            screen.blit(controls_surface, controls_rectangle)

        # screen.blit(dancing_dragons_surface, dancing_dragons_rectangle)
        # screen.blit(game_over_surface, game_over_rectangle)
        screen.blit(game_name_surface, game_name_rectangle)
        start_time = pygame.time.get_ticks()
        snail_speed = 10

    pygame.display.update()
    clock.tick(60)
