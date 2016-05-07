import os
import sys
import pygame
from Vector import Vector


NORMAL = 0
TURN_LEFT = 1
TURN_RIGHT = 2
UP = 3
DOWN = 4
MAX_SPEED = 20
ROTATE_ANGLE = 2
WHITE = (220, 220, 220)
GREEN = (0, 220, 0)


class Car:
    def __init__(self, pos, image):
        self.size = (195, 195)
        self.pos = Vector(pos)
        self.speed = Vector((0, -2))
        self.image = None
        self.load_image(image)
        self.rect = self.image.get_rect()
        self.state = NORMAL
        self.direction = self.speed
        self.max_speed = None

    def load_image(self, name):
        fullname = os.path.join('images', name)
        self.image = pygame.image.load(fullname)
        self.image = pygame.transform.scale(self.image, self.size)
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

    def update(self):  # поворот и изменение скорости автомобиля
        self.max_speed = self.speed
        if self.state == TURN_LEFT:
            self.speed.rotate(-ROTATE_ANGLE)

        if self.state == TURN_RIGHT:
            self.speed.rotate(ROTATE_ANGLE)

        if self.state == UP:
            if self.speed.len < 1:
                self.speed += self.direction.normalize()
            self.speed += self.speed.normalize()
            if self.speed.len > MAX_SPEED:
                self.speed = self.max_speed

        if self.state == DOWN:
            self.speed -= self.speed.normalize()
            if self.speed.len < 1 and self.speed.len != 0:
                self.direction = self.speed
                self.speed = Vector((0, 0))
        self.rect.move(self.speed.x, self.speed.y)

    def inside_rect(self, rect1, rect2):  # обработка столкновений с дорогой
        dx = -1
        if not rect1.collidepoint(self.rect.move(self.pos.x, self.pos.y).topright) and \
                not rect2.collidepoint(self.rect.move(self.pos.x, self.pos.y).topright):
            self.speed.x *= dx
        elif not rect1.collidepoint(self.rect.move(self.pos.x, self.pos.y).topleft) and \
                not rect2.collidepoint(self.rect.move(self.pos.x, self.pos.y).topleft):
            self.speed.x *= dx
        if not rect1.collidepoint(self.rect.move(self.pos.x, self.pos.y).bottomright) and \
                not rect2.collidepoint(self.rect.move(self.pos.x, self.pos.y).bottomright):
            self.speed.x *= -dx
        elif not rect1.collidepoint(self.rect.move(self.pos.x, self.pos.y).bottomleft) and \
                not rect2.collidepoint(self.rect.move(self.pos.x, self.pos.y).bottomleft):
            self.speed.x *= -dx

    def render(self, screen):
        origin_rec = self.rect
        # dspeed =
        if self.speed.len >= 1:
            image_rotate = pygame.transform.rotate(self.image, self.speed.angle - 90)
        else:
            image_rotate = pygame.transform.rotate(self.image, self.direction.angle - 90)
        rotate_rec = image_rotate.get_rect()
        rotate_rec.center = origin_rec.center
        rotate_rec.move_ip(self.pos.as_point())
        screen.blit(image_rotate, rotate_rec)
        pygame.draw.line(screen, GREEN, self.pos.as_point(), (self.pos + self.speed * 10).as_point())
        pygame.draw.rect(screen, WHITE, self.rect.move(self.pos.x, self.pos.y), 3)