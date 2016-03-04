import os
import sys
import pygame
from Vector import Vector
FPS = 60
NORMAL = 0
TURN_LEFT = 1
TURN_RIGHT = 2
UP = 3
DOWN = 4


class Car:
    def __init__(self, pos):
        self.pos = Vector(pos)
        self.speed = Vector((1, 0))
        self.load_image('yellow_car.png')
        self.rect = pygame.Rect(self.pos.x, self.pos.y, 100, 100)
        self.draw()
        self.state = NORMAL

    def load_image(self, name):
        fullname = os.path.join('images', name)
        self.image = pygame.image.load(fullname)
        return self.image

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.state = TURN_LEFT
            if event.key == pygame.K_RIGHT:
                self.state = TURN_RIGHT
        if event.type == pygame.KEYUP:
            self.state = NORMAL

    def update(self):
        if self.state == TURN_LEFT:
            self.speed.rotate(-2)

        if self.state == TURN_RIGHT:
            self.speed.rotate(2)

    def draw(self):
        screen.blit(self.image, self.rect)

    def render(self, screen):
        image_rotate = pygame.transform.rotate(self.image, self.speed.angle)
        origin_rec = self.image.get_rect()
        rotate_rec = image_rotate.get_rect()
        rotate_rec.center = origin_rec.center
        rotate_rec.move_ip(self.pos.as_point())
        screen.blit(image_rotate, rotate_rec)


class Road:
    def __init__(self, pos, image):
        self.load_image(image)
        self.pos = Vector(pos)
        self.state = NORMAL
        self.speed = Vector((0, 3))
        self.direction = self.speed
        self.image = pygame.transform.scale(self.image, (600, 950))

    def load_image(self, name):
        fullname = os.path.join('images', name)
        self.image = pygame.image.load(fullname)
        return self.image

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.state = TURN_LEFT
            if event.key == pygame.K_RIGHT:
                self.state = TURN_RIGHT
            if event.key == pygame.K_UP:
                self.state = UP
            if event.key == pygame.K_DOWN:
                self.state = DOWN
        if event.type == pygame.KEYUP:
            self.state = NORMAL

    def update(self):
        if self.state == TURN_LEFT:
            self.speed.rotate(-2)

        if self.state == TURN_RIGHT:
            self.speed.rotate(2)

        if self.state == UP:
            self.speed += self.direction.normalize()

        if self.state == DOWN:
            self.speed -= self.speed.normalize()
            if self.speed.len < 1:
                self.direction = self.speed

        self.pos += self.speed

        if self.pos.y > 800:
            self.pos.y = -800

        if self.pos.y < -900:
            self.pos.y = 800

    def render(self, screen):
        screen.blit(self.image, self.pos.as_point())
        pygame.draw.line(screen, (0, 255, 0), self.pos.as_point(), (self.pos + self.speed*10).as_point())

pygame.init()
pygame.display.set_mode((800, 800))
screen = pygame.display.get_surface()
pygame.display.set_caption("Car")
car = Car((370, 250))
road = Road((100, 0), 'road.jpg')
road2 = Road((100, -915), 'road.jpg')
font = pygame.font.SysFont("Courier New", 18)
text2 = font.render('km/h - ', 7, (250, 250, 250))
clock = pygame.time.Clock()
while True:
    text = font.render(str(int(road.speed.len)*5), 7, (250, 250, 250))
    for event in pygame.event.get():
        road.events(event)
        road2.events(event)
        car.events(event)
        if event.type == pygame.QUIT:
            sys.exit()
    clock.tick(FPS)
    road.update()
    road2.update()
    car.update()
    screen.fill((0, 60, 80))
    road.render(screen)
    road2.render(screen)
    car.render(screen)
    screen.blit(text2, (0, 0))
    screen.blit(text, (70, 0))
    pygame.display.flip()

