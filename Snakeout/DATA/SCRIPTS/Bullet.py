import pygame

class Bullet():
    def __init__(self, speed, rect, pos):
        self.rect = rect
        self.speed = speed
        self.vect = pygame.math.Vector2([pos[0]-rect.x, pos[1]-rect.y]).normalize() * self.speed

    def move(self):
        self.rect.center += self.vect

    def draw(self, screen, colour):
        pygame.draw.circle(screen, colour, self.rect.center, self.rect.w/2)