import pygame

class Player():
    def __init__(self, start_pos, nodes, length):
        self.length = length
        self.nodes = []
        for i in range(nodes):
            self.nodes.append(pygame.FRect([start_pos[0]-i*self.length, start_pos[1]], [15, 15]))

        
        self.speed = 3
        self.dash_speed = self.speed*2
        self.slow_speed = self.speed/2
        self.curr_speed = self.speed
        self.rot_speed = 4
        self.vect = pygame.Vector2(self.speed, 0)
        
        self.dash = False
        self.dash_delay = 3000
        self.next_dash = -3000
        self.dashing_delay = 500
        self.next_dashing = -500

        self.fire_rate = 300
        self.next_fire = -300
        self.bullet_speed = 4
    
    def draw(self, screen, node_color, segment_color):
        for i in range(1, len(self.nodes)):
            pygame.draw.line(screen, segment_color, self.nodes[i].center, self.nodes[i-1].center, 7)
        for i in range(len(self.nodes)):
            pygame.draw.circle(screen, node_color, self.nodes[i].center, self.nodes[i].w/2)
    
    def update(self):
        for i in range(1, len(self.nodes)):
            vector = pygame.Vector2(self.nodes[i-1].centerx-self.nodes[i].centerx, self.nodes[i-1].centery-self.nodes[i].centery)
            if self.length*1.1 >= int(vector.length()) >= self.length/1.1:
                continue
            if int(vector.length()) > self.length:
                self.nodes[i].center += vector.normalize()*self.curr_speed
            elif int(vector.length()) < self.length:
                self.nodes[i].center -= vector.normalize()*self.curr_speed