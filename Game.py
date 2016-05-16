import pygame
import sys
from pygame import *
from Car import Car
from Menu import Menu
from Road import Road
from Objects import Object

GREY = (100, 100, 100)
FPS = 60


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((1000, 800))
        self.font = pygame.font.SysFont("Courier New", 18)
        self.font2 = pygame.font.SysFont("Courier New", 45)
        self.font_finish = pygame.font.SysFont("Courier New", 75)
        self.screen = pygame.display.get_surface()
        self.car = Car((325, 450), 'yellow_car.png')
        self.road = Road((100, 0), 'road.jpg', self.car)
        self.barrel = Object('barrels.png', self.car)
        self.barrel1 = Object('barrels.png', self.car)
        self.distance = 10 ** 5
        self.seconds = 0
        self.minutes = 0
        self.menu = Menu()
        self.clock = pygame.time.Clock()

    def render(self):
        self.screen.fill(GREY)
        self.road.render(self.screen)
        self.car.render(self.screen)
        self.barrel.render(self.screen)
        self.screen.blit(self.font.render('Speed - ', 7, (220, 50, 0)), (0, 0))
        self.screen.blit(self.font.render("Time -   min   sec", 7, (220, 50, 0)), (0, 40))
        self.screen.blit(self.font.render(str(self.minutes), 7, (220, 220, 220)), (80, 40))
        self.screen.blit(self.font.render(str(int(self.seconds)), 7, (220, 220, 220)), (140, 40))
        self.screen.blit(self.font.render(str(int(self.car.speed.len)), 7, (220, 220, 220)), (90, 0))
        self.screen.blit(self.font.render('Distance - ', 7, (220, 50, 0)), (0, 20))
        if self.distance < 0:
            self.screen.blit(self.font_finish.render("FINISH", 21, (220, 50, 0)), (250, 300))
            self.screen.blit(self.font.render('0', 7, (220, 80, 0)), (120, 20))
        else:
            self.seconds += self.clock.get_time() / 1000
            self.screen.blit(self.font.render(str(self.distance), 7, (220, 220, 220)), (120, 20))
        if self.road.pos.y > self.car.speed.y + self.road.pos.y:
            self.distance -= int(self.car.speed.len)
        elif self.road.pos.y < self.car.speed.y + self.road.pos.y:
            self.screen.blit(self.font_finish.render("Wrong way", 21, (220, 50, 0)), (250, 300))
            self.distance += int(self.car.speed.len)

    def update(self):
        self.clock.tick(FPS)
        self.road.update()
        self.car.update()
        self.barrel.update()
        if self.seconds > 60:
            self.seconds -= 60
            self.minutes += 1
        self.car.inside_rect(self.road.rect.move(self.road.pos.x, self.road.pos.y),
                             self.road.rect.move(self.road.pos2.x, self.road.pos2.y))
        self.car.in_rect(self.barrel.rect.move(self.barrel.pos.x, self.barrel.pos.y))
        self.barrel.in_rect(self.car.rect.move(self.car.pos.x, self.car.pos.y))

    def events(self, event):
        self.car.events(event)

    def run(self):
        while True:
            for event in pygame.event.get():
                self.events(event)
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu.run(self)

            self.update()
            self.render()
            pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    # game.run()
