import pygame
from pygame import *
from Car import Car
from Road import Road

GREY = (100, 100, 100)

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
        self.distance = 10 ** 5
        self.seconds = 0
        self.minutes = 0
        self.clock = pygame.time.Clock()

    def render(self):
        self.screen.fill(GREY)
        self.car.render(self.screen)
        self.road.render(self.screen)

    def update(self):
        self.road.update()
        self.car.update()
        if self.distance < 0:
            self.screen.blit(self.font_finish.render("FINISH", 21, (220, 50, 0)), (250, 300))
            self.screen.blit(self.font.render('0', 7, (220, 80, 0)), (120, 20))
        else:
            self.seconds += self.clock.get_time()/1000
            self.screen.blit(self.font.render(str(self.distance), 7, (220, 220, 220)), (120, 20))
        if self.seconds > 60:
            self.seconds -= 60
            self.minutes += 1
        if self.road.pos.y > self.car.speed.y + self.road.pos.y:
            self.distance -= int(self.car.speed.len)
        elif self.road.pos.y < self.car.speed.y + self.road.pos.y:
            self.screen.blit(self.font_finish.render("Wrong way", 21, (220, 50, 0)), (250, 300))
            self.distance += int(self.car.speed.len)

    def events(self, event):
        self.car.events(event)

    def run(self):
        while True:
            for event in pygame.event.get():
                self.events(event)
                if event.type == pygame.QUIT:
                    sys.exit()
            self.update()
            self.render()
            pygame.display.flip()
