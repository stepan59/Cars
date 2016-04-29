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


class Car:
    def __init__(self, pos, image):
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
        self.image = pygame.transform.scale(self.image, (195, 195))
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
            if self.speed.len > MAX_SPEED:
                self.speed = self.max_speed

        if self.state == DOWN:
            self.speed -= self.speed.normalize()
            if self.speed.len < 1 and self.speed.len != 0:
                self.direction = self.speed
                self.speed = Vector((0, 0))
        self.rect.move(self.speed.x, self.speed.y)

    def inside_rect(self, rect1, rect2):
        if not rect1.collidepoint(self.rect.move(self.pos.x, self.pos.y).topright) and \
                not rect2.collidepoint(self.rect.move(self.pos.x, self.pos.y).topright):
            # print('Столкновение topright')
            self.speed.x -= 0.5
        elif not rect1.collidepoint(self.rect.move(self.pos.x, self.pos.y).topleft) and \
                not rect2.collidepoint(self.rect.move(self.pos.x, self.pos.y).topleft):
            # print('Столкновение topleft')
            self.speed.x += 0.5
        if not rect1.collidepoint(self.rect.move(self.pos.x, self.pos.y).bottomright) and \
                not rect2.collidepoint(self.rect.move(self.pos.x, self.pos.y).bottomright):
            # print('Столкновение bottomright')
            self.speed.x -= 0.5
        elif not rect1.collidepoint(self.rect.move(self.pos.x, self.pos.y).bottomleft) and \
                not rect2.collidepoint(self.rect.move(self.pos.x, self.pos.y).bottomleft):
            # print('Столкновение bottomleft')
            self.speed.x += 0.5

    def render(self, screen):
        origin_rec = self.rect
        if self.speed.len > 1 or self.speed.len == 1:
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
        pygame.draw.rect(screen, (220, 220, 220), self.rect.move(self.pos.x, self.pos.y), 3)