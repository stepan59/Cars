import os
import random
import pygame
from Vector import Vector


class Object:
    def __init__(self, image, car):
        self.car = car
        self.pos = Vector((random.randint(self.car.pos.x-25, self.car.pos.x+25), random.randint(0, 800)))
        self.image = None
        self.load_image(image)
        self.rect = self.image.get_rect()

    def load_image(self, name):
        fullname = os.path.join('images', name)
        self.image = pygame.image.load(fullname)
        self.image = pygame.transform.scale(self.image, (195, 195))
        return self.image

    def update(self):
        self.pos += self.car.speed * -1

        if self.pos.y > 800:
            self.pos.y = -800
            self.pos.x = random.randint(self.car.pos.x-25, self.car.pos.x+25)

        if self.pos.y < -800:
            self.pos.y = 800
            self.pos.x = random.randint(self.car.pos.x-25, self.car.pos.x+25)

    def render(self, screen):
        screen.blit(self.image, self.pos.as_point())
        pygame.draw.rect(screen, (0, 0, 0), self.rect.move(self.pos.x, self.pos.y), 3)