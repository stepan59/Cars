import os
import random
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
        self.speed = Vector((0, -2))
        self.image = None
        self.load_image('yellow_car.png')
        self.rect = self.image.get_rect()
        self.state = NORMAL
        self.direction = self.speed
        self.max_speed = None

    def load_image(self, name):
        fullname = os.path.join('images', name)
        self.image = pygame.image.load(fullname)
        return self.image

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.state = TURN_LEFT
            elif event.key == pygame.K_RIGHT:
                self.state = TURN_RIGHT
            elif event.key == pygame.K_UP:
                self.state = UP
            elif event.key == pygame.K_DOWN:
                self.state = DOWN
            elif event.key == pygame.K_ESCAPE:
                sys.exit()
        if event.type == pygame.KEYUP:
            self.state = NORMAL

    def update(self):
        self.max_speed = self.speed
        if self.state == TURN_LEFT:
            self.speed.rotate(-2)

        if self.state == TURN_RIGHT:
            self.speed.rotate(2)

        if self.state == UP:
            if self.speed.len < 1:
                self.speed += self.direction.normalize()
            self.speed += self.speed.normalize()
            if self.speed.len > 46:
                self.speed = self.max_speed

        if self.state == DOWN:
            self.speed -= self.speed.normalize()
            if self.speed.len < 1 and self.speed.len != 0:
                self.direction = self.speed
                self.speed = Vector((0, 0))

    def render(self, screen):
        origin_rec = self.rect
        if self.speed.len > 1:
            image_rotate = pygame.transform.rotate(self.image, self.speed.angle - 90)
            rotate_rec = image_rotate.get_rect()
            rotate_rec.center = origin_rec.center
            rotate_rec.move_ip(self.pos.as_point())
            screen.blit(image_rotate, rotate_rec)
        if self.speed.len < 1:
            image_rotate = pygame.transform.rotate(self.image, self.direction.angle - 90)
            rotate_rec = image_rotate.get_rect()
            rotate_rec.center = origin_rec.center
            rotate_rec.move_ip(self.pos.as_point())
            screen.blit(image_rotate, rotate_rec)
        pygame.draw.line(screen, (0, 220, 0), self.pos.as_point(), (self.pos + self.speed * 10).as_point())


class Road:
    def __init__(self, pos, image, car):
        self.load_image(image)
        self.pos = Vector(pos)
        self.pos2 = self.pos + Vector((0, -800))
        self.car = car
        self.direction = car.speed
        self.image = pygame.transform.scale(self.image, (600, 900))
        self.image2 = pygame.transform.scale(self.image, (600, 900))

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
        pygame.draw.line(screen, (0, 220, 0), self.pos.as_point(), (self.pos + car.speed * 10).as_point())
        pygame.draw.line(screen, (0, 220, 0), self.pos2.as_point(), (self.pos2 + car.speed * 10).as_point())


class Enemy:
    def __init__(self, name):
        self.image = pygame.image.load(os.path.join('images', name))
        self.pos = Vector((random.randint(180, 460), random.randint(-800, 1600)))
        self.speed = Vector((0, random.randint(-10, -1)))
        self.rect = self.image.get_rect()
        self.car = car

    def update(self):
        if self.car.speed.len < self.speed.len:
            self.pos += self.speed
        elif self.car.speed.len > self.speed.len and self.car.speed.len > 0:
            self.pos -= self.speed

    def render(self, screen):
        screen.blit(self.image, self.pos.as_point())
        pygame.draw.line(screen, (0, 220, 0), self.pos.as_point(), (self.pos + self.speed * 10).as_point())


pygame.init()
pygame.display.set_mode((800, 800))
screen = pygame.display.get_surface()
pygame.display.set_caption("Great Race")

car = Car((325, 450))
road = Road((100, 0), 'road.jpg', car)
# enemy1 = Enemy('yellow_car.png')

font = pygame.font.SysFont("Courier New", 18)
font_finish = pygame.font.SysFont("Courier New", 90)

text_speed = font.render('speed - ', 7, (220, 220, 220))
text_distance = font.render('Distance - ', 7, (220, 220, 220))
text_finish = font_finish.render("FINISH", 21, (220, 0, 0))
text_wrong_way = font_finish.render("Wrong way", 21, (220, 0, 0))
text_exit = font.render("Press ESC for exit", 7, (250, 0, 0))
distance = 10 ** 5
clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        car.events(event)
        if event.type == pygame.QUIT:
            sys.exit()
    clock.tick(FPS)
    road.update()
    car.update()
    # enemy1.update()
    screen.fill((22, 90, 90))
    road.render(screen)
    # enemy1.render(screen)
    car.render(screen)

    text_speed2 = font.render(str(int(car.speed.len)), 7, (220, 220, 220))
    text_distance2 = font.render(str(distance), 7, (220, 220, 220))

    if distance < 0:
        text = font.render('0', 7, (220, 220, 220))
        screen.blit(text_finish, (250, 300))
        screen.blit(text, (120, 20))
        screen.blit(text_exit, (315, 380))
    else:
        screen.blit(text_distance2, (120, 20))

    screen.blit(text_speed, (0, 0))
    screen.blit(text_speed2, (80, 0))
    screen.blit(text_distance, (0, 20))

    if road.pos.y > car.speed.y + road.pos.y:
        distance -= int(car.speed.len)
    elif road.pos.y < car.speed.y + road.pos.y:
        screen.blit(text_wrong_way, (250, 300))
        distance += int(car.speed.len)

    pygame.display.flip()