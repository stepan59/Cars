import sys
import pygame
from Car import Car
from Road import Road
from Menu import Menu
from Objects import Object
from Vector import Vector

FPS = 60


# def menu(text1, text2, text3, text_1, text_2, text_3, screen):
#     global done
#     screen.fill((100, 100, 100))
#     screen.blit(text1, (300, 200))
#     screen.blit(text2, (300, 300))
#     screen.blit(text3, (300, 400))
#     mouse_pos = pygame.mouse.get_pos()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#                     sys.exit()
#         if (300 < mouse_pos[0] < 400) and (200 < mouse_pos[1] < 280):
#             text1 = font_finish.render(text_1, 21, (220, 250, 250))
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_SPACE:
#                     done = True
#                     return done
#         else:
#             text1 = font_finish.render(text_1, 21, (220, 50, 0))
#
#         if (300 < mouse_pos[0] < 400) and (300 < mouse_pos[1] < 380):
#             text2 = font_finish.render(text_2, 21, (220, 250, 0))
#
#         else:
#             text2 = font_finish.render(text_2, 21, (220, 50, 0))
#
#         if (300 < mouse_pos[0] < 400) and (400 < mouse_pos[1] < 480):
#             text3 = font_finish.render(text_3, 21, (220, 250, 0))
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_SPACE:
#                     sys.exit()
#         else:
#             text3 = font_finish.render(text_3, 21, (220, 50, 0))
#     pygame.display.flip()

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
text_play = (font_finish.render("Play", 21, (220, 50, 0)), (300, 200))
text_records = (font_finish.render("Records", 21, (220, 50, 0)), (300, 300))
text_quit = (font_finish.render("Quit", 21, (220, 50, 0)), (300, 400))
menu = Menu(screen)
distance = 10 ** 5
clock = pygame.time.Clock()
seconds = 0
minutes = 0
done = False
while True:
    menu.render(text_play, text_records, text_quit)
    while done:
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
