import os
import pygame
from Vector import Vector


class Road:
    def __init__(self, pos, image, car):
        self.load_image(image)
        self.pos = Vector(pos)
        self.pos2 = self.pos + Vector((0, -800))
        self.size = (600, 900)
        self.car = car
        self.direction = car.speed
        self.image = pygame.transform.scale(self.image, self.size)
        self.image2 = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()

    def load_image(self, name):
        fullname = os.path.join('images', name)
        self.image = pygame.image.load(fullname)
        self.image2 = pygame.image.load(fullname)
        return self.image, self.image2

    def update(self):
        self.pos += self.car.speed * -1
        self.pos2 += self.car.speed * -1

        if self.pos.y > 800:
            self.pos.y = -800

        if self.pos.y < -800:
            self.pos.y = 800

        if self.pos2.y > 800:
            self.pos2.y = -800

        if self.pos2.y < -800:
            self.pos2.y = 800


    def render(self, screen):
        screen.blit(self.image, self.pos.as_point())
        screen.blit(self.image2, self.pos2.as_point())
