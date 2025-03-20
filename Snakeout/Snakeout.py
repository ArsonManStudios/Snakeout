import pygame

# Color Constants
BLACK = (20, 20, 20)
BROWN = (61, 49, 47)
BROWN2 = (89, 74, 71)
GREEN = (92, 219, 126)
DGREEN = (37, 156, 69)
BLUE = (111, 178, 214)
WHITE = (245, 245, 245)

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

#Bullet Class
bullets = []
class Bullet():
    def __init__(self, speed, rect, pos):
        self.rect = rect
        self.speed = speed
        self.vect = pygame.math.Vector2([pos[0]-rect.x, pos[1]-rect.y]).normalize() * self.speed

    def move(self):
        self.rect.center += self.vect

    def draw(self):
        pygame.draw.circle(screen, WHITE, self.rect.center, self.rect.w/2)

# Player Class
class Player():
    def __init__(self, start_pos, nodes, length):
        self.length = length
        self.nodes = []
        for i in range(nodes):
            self.nodes.append(pygame.FRect([start_pos[0]-i*self.length, start_pos[1]], [15, 15]))
    
    def draw(self, node_color, segment_color):
        for i in range(1, len(self.nodes)):
            pygame.draw.line(screen, segment_color, self.nodes[i].center, self.nodes[i-1].center, 7)
        for i in range(len(self.nodes)):
            pygame.draw.circle(screen, node_color, self.nodes[i].center, self.nodes[i].w/2)
    
    def update(self, speed):
        for i in range(1, len(self.nodes)):
            vector = pygame.Vector2(self.nodes[i-1].centerx-self.nodes[i].centerx, self.nodes[i-1].centery-self.nodes[i].centery)
            if self.length*1.1 >= int(vector.length()) >= self.length/1.1:
                continue
            if int(vector.length()) > self.length:
                self.nodes[i].center += vector.normalize()*speed
            elif int(vector.length()) < self.length:
                self.nodes[i].center -= vector.normalize()*speed

player = Player([w/2, h/2], 7, 25)
speed = 3
dash_speed = speed*2
slow_speed = speed/2
rot_speed = 4
player_move = pygame.Vector2(speed, 0)
dash = False
dash_delay = 3000
next_dash = -3000
dashing_delay = 500
next_dashing = -500

while run:
    keys = pygame.key.get_pressed()
    curr_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and next_dash+dash_delay <= curr_time and not dash:
                dash = True
                next_dash = curr_time
                next_dashing = curr_time

    speed = 3
    dash_speed = speed*2
    slow_speed = speed/2
    if dash and next_dashing+dashing_delay > curr_time:
        speed = dash_speed
    else:
        dash = False

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_move.rotate_ip(rot_speed)
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_move.rotate_ip(-rot_speed)
    if keys[pygame.K_DOWN] or keys[pygame.K_s] and not dash:
        speed = slow_speed

    if player.nodes[0].right >= w or player.nodes[0].left <= 0:
        player_move.x *= -1
    if player.nodes[0].top <= 100 or player.nodes[0].bottom >= h:
        player_move.y *= -1

    if player_move.length() != 0:
        player_move = player_move.normalize()*speed
    player.nodes[0].center += player_move

    screen.fill(BLACK)
    player.draw(DGREEN, GREEN)
    player.update(speed)
    pygame.draw.rect(screen, BROWN2, pygame.FRect(0, 0, w, 100))
    pygame.draw.rect(screen, BROWN, pygame.FRect(0, 0, w, 100), 5)
    pygame.draw.rect(screen, BLUE, pygame.FRect(15, 15, 200*max(0,min(1,(curr_time-next_dash)/dash_delay)), 70))
    pygame.draw.rect(screen, BLACK, pygame.FRect(15, 15, 200, 70), 5)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()