import pygame
from DATA.SCRIPTS.Player import*
from DATA.SCRIPTS.Bullet import*

# Color Constants
BLACK = (20, 20, 20)
BROWN = (61, 49, 47)
BROWN2 = (89, 74, 71)
GREEN = (92, 219, 126)
DGREEN = (37, 156, 69)
BLUE = (111, 178, 214)
WHITE = (245, 245, 245)
RED = (227, 82, 82)

# Initaization
pygame.init()
clock = pygame.time.Clock()
run = True

# Screen
size = (1200, 800)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Snakeout')
h = screen.get_height()
w = screen.get_width()

bullets = []
enemies = []
player = Player([w/2, h/2], 7, 25)

while run:
    keys = pygame.key.get_pressed()
    mouse_but = pygame.mouse.get_pressed()
    curr_time = pygame.time.get_ticks()
    mos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and player.next_dash+player.dash_delay <= curr_time and not player.dash:
                player.dash = True
                player.next_dash = curr_time
                player.next_dashing = curr_time

    player.curr_speed = player.speed
    if player.dash and player.next_dashing+player.dashing_delay > curr_time:
        player.curr_speed = player.dash_speed
    else:
        player.dash = False
    
    if mouse_but[0]:
        if player.next_fire+player.fire_rate <= curr_time:
            bullets.append(Bullet(player.bullet_speed, pygame.FRect(player.nodes[0].center, (10, 10)), mos))
            player.next_fire = curr_time

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.vect.rotate_ip(player.rot_speed)
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.vect.rotate_ip(-player.rot_speed)
    if keys[pygame.K_DOWN] or keys[pygame.K_s] and not player.dash:
        player.curr_speed = player.slow_speed

    if player.nodes[0].right >= w or player.nodes[0].left <= 0:
        player.vect.x *= -1
    if player.nodes[0].top <= 100 or player.nodes[0].bottom >= h:
        player.vect.y *= -1

    if player.vect.length() != 0:
        player.vect = player.vect.normalize()*player.curr_speed
    player.nodes[0].center += player.vect

    screen.fill(BLACK)
    player.draw(screen, DGREEN, GREEN)
    player.update()

    for bullet in bullets:
        bullet.move()
        bullet.draw(screen, WHITE)
        if not bullet.rect.colliderect(pygame.FRect(0, 100, w, h-100)):
            bullets.remove(bullet)

    pygame.draw.rect(screen, BROWN2, pygame.FRect(0, 0, w, 100))
    pygame.draw.rect(screen, BROWN, pygame.FRect(0, 0, w, 100), 5)
    pygame.draw.rect(screen, BLUE, pygame.FRect(15, 15, 200*max(0,min(1,(curr_time-player.next_dash)/player.dash_delay)), 70))
    pygame.draw.rect(screen, BLACK, pygame.FRect(15, 15, 200, 70), 5)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()