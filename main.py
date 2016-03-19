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
        self.speed = Vector((0, -2))
        self.image = None
        self.load_image('yellow_car.png')
        self.rect = self.image.get_rect()
        self.state = NORMAL
        self.direction = self.speed
        # self.max_speed = Vector((0, 43))

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
        if event.type == pygame.KEYUP:
            self.state = NORMAL

    def update(self):
        if self.state == TURN_LEFT:
            self.speed.rotate(-2)

        if self.state == TURN_RIGHT:
            self.speed.rotate(2)

        if self.state == UP:
            self.speed += self.direction.normalize()
            # # FIXME: неправильно работает ограничение скорости
            # if self.speed.len > 45.0:
            #     self.speed = self.max_speed

        if self.state == DOWN:
            self.speed -= self.speed.normalize()
            # FIXME: при нулевой скорости, неверное направление картинки автомобиля
            if self.speed.len < 1 and self.speed.len != 0:
                self.direction = self.speed
                self.speed = Vector((0, 0))

    def render(self, screen):
        image_rotate = pygame.transform.rotate(self.image, self.speed.angle - 90)
        origin_rec = self.image.get_rect()
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


pygame.init()
pygame.display.set_mode((800, 800))
screen = pygame.display.get_surface()
pygame.display.set_caption("Great Race")

car = Car((325, 450))
road = Road((100, 0), 'road.jpg', car)

font = pygame.font.SysFont("Courier New", 18)
font_finish = pygame.font.SysFont("Courier New", 90)

# text2 = font.render('speed -   km/h ', 7, (220, 220, 220))
# text3 = font.render('Distance - ', 7, (220, 220, 220))
# text5 = font_finish.render("FINISH", 21, (220, 0, 0))
# text6 = font_finish.render("Wrong way", 21, (220, 0, 0))
distance = 10 ** 5
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        car.events(event)
        if event.type == pygame.QUIT:
            sys.exit()
    clock.tick(FPS)
    road.update()
    # if road.speed.len > 1:
    #     car.update()
    car.update()
    screen.fill((22, 90, 90))
    road.render(screen)
    car.render(screen)

    # if distance < 0:
    #     screen.blit(text5, (250, 300))
    #     distance2 = '0'
    # else:
    #     distance2 = str(distance)

    # text4 = font.render(distance2, 7, (220, 220, 220))
    # screen.blit(text4, (120, 20))
    # screen.blit(text2, (0, 0))
    # # screen.blit(text, (80, 0))
    # screen.blit(text3, (0, 20))

    # if road.pos.y < road.speed.y + road.pos.y:
    #     distance -= int(road.speed.len)*5
    # elif road.pos.y > road.speed.y + road.pos.y:
    #     screen.blit(text6, (250, 300))
    #     distance += int(road.speed.len)*5

    pygame.display.flip()