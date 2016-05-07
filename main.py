import sys
import pygame
from Car import Car
from Road import Road
from Objects import Object
from Vector import Vector

FPS = 60

pygame.init()
pygame.display.set_mode((1000, 800))
screen = pygame.display.get_surface()
pygame.display.set_caption("Great Race")

car = Car((325, 450), 'yellow_car.png')
road = Road((100, 0), 'road.jpg', car)
# barrel = Object('barrels.png', car)
font = pygame.font.SysFont("Courier New", 18)
font2 = pygame.font.SysFont("Courier New", 45)
font_finish = pygame.font.SysFont("Courier New", 75)

text_speed = font.render('Speed - ', 7, (220, 50, 0))
text_distance = font.render('Distance - ', 7, (220, 50, 0))
text_finish = font_finish.render("FINISH", 21, (220, 50, 0))
text_wrong_way = font_finish.render("Wrong way", 21, (220, 50, 0))
text_exit = font.render("Press ESC for exit", 7, (220, 50, 0))
text_time = font.render("Time -   min   sec", 7, (220, 50, 0))
text_play = font_finish.render("Play", 21, (220, 50, 0))
text_records = font_finish.render("Records", 21, (220, 50, 0))
text_quit = font_finish.render("Quit", 21, (220, 50, 0))
distance = 10 ** 5
clock = pygame.time.Clock()
seconds = 0
minutes = 0

while True:
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #             sys.exit()
    # done = False
    # screen.fill((100, 100, 100))
    # screen.blit(text_play, (300, 200))
    # screen.blit(text_records, (300, 300))
    # screen.blit(text_quit, (300, 400))
    # mouse_pos = pygame.mouse.get_pos()
    # if (300 < mouse_pos[0] < 400) and (200 < mouse_pos[1] < 255):
    #     text_play = font_finish.render("Play", 21, (220, 250, 0))
    #     # done = True
    # else:
    #     text_play = font_finish.render("Play", 21, (220, 50, 0))
    #
    # if (300 < mouse_pos[0] < 400) and (300 < mouse_pos[1] < 455):
    #     text_quit = font_finish.render("Records", 21, (220, 250, 0))
    #
    # else:
    #     text_quit = font_finish.render("Records", 21, (220, 50, 0))
    #
    # if (300 < mouse_pos[0] < 400) and (400 < mouse_pos[1] < 555):
    #     text_quit = font_finish.render("Quit", 21, (220, 250, 0))
    #     # sys.exit()
    # else:
    #     text_quit = font_finish.render("Quit", 21, (220, 50, 0))
    # pygame.display.flip()
    # while done:
        for event in pygame.event.get():
            car.events(event)
            if event.type == pygame.QUIT:
                sys.exit()
        clock.tick(FPS)
        road.update()
        # barrel.update()
        car.update()
        screen.fill((70, 70, 70))
        road.render(screen)
        # barrel.render(screen)
        car.render(screen)
        car.inside_rect(road.rect.move(road.pos.x, road.pos.y), road.rect.move(road.pos2.x, road.pos2.y))

        text_speed2 = font.render(str(int(car.speed.len)), 7, (220, 220, 220))
        text_distance2 = font.render(str(distance), 7, (220, 220, 220))
        text_seconds = font.render(str(int(seconds)), 7, (220, 220, 220))
        text_minutes = font.render(str(minutes), 7, (220, 220, 220))
        if seconds > 60:
            seconds -= 60
            minutes += 1

        # if car.rect.move(car.pos.x, car.pos.y).colliderect(barrel.rect.move(barrel.pos.x, barrel.pos.y)):
        #     print("Столкновение")

        if distance < 0:
            text = font.render('0', 7, (220, 80, 0))
            screen.blit(text_finish, (250, 300))
            screen.blit(text, (120, 20))
            screen.blit(text_exit, (315, 380))
        else:
            seconds += clock.get_time()/1000
            screen.blit(text_distance2, (120, 20))

        screen.blit(text_speed, (0, 0))
        screen.blit(text_time, (0, 40))
        screen.blit(text_minutes, (80, 40))
        screen.blit(text_seconds, (140, 40))
        screen.blit(text_speed2, (90, 0))
        screen.blit(text_distance, (0, 20))
        screen.blit(text_exit, (790, 0))

        if road.pos.y > car.speed.y + road.pos.y:
            distance -= int(car.speed.len)
        elif road.pos.y < car.speed.y + road.pos.y:
            screen.blit(text_wrong_way, (250, 300))
            distance += int(car.speed.len)
        pygame.display.flip()
