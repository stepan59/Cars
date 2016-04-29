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
barrel = Object('barrels.png', car)
font = pygame.font.SysFont("Courier New", 18)
font2 = pygame.font.SysFont("Courier New", 45)
font_finish = pygame.font.SysFont("Courier New", 75)

text_speed = font.render('Speed - ', 7, (220, 50, 0))
text_distance = font.render('Distance - ', 7, (220, 50, 0))
text_finish = font_finish.render("FINISH", 21, (220, 50, 0))
text_wrong_way = font_finish.render("Wrong way", 21, (220, 50, 0))
text_exit = font.render("Press ESC for exit", 7, (220, 50, 0))
# background_image = pygame.image.load('images/sand.png')
distance = 10 ** 5
# car_hp = 500
clock = pygame.time.Clock()

while True:
    # screen.blit(background_image, (0,0))

    for event in pygame.event.get():
        car.events(event)
        if event.type == pygame.QUIT:
            sys.exit()
    clock.tick(FPS)
    road.update()
    barrel.update()
    car.update()
    screen.fill((70, 70, 70))
    road.render(screen)
    barrel.render(screen)
    car.render(screen)
    car.inside_rect(road.rect.move(road.pos.x, road.pos.y), road.rect.move(road.pos2.x, road.pos2.y))

    text_speed2 = font.render(str(int(car.speed.len)), 7, (220, 220, 220))
    text_distance2 = font.render(str(distance), 7, (220, 220, 220))

    if car.rect.move(car.pos.x, car.pos.y).colliderect(barrel.rect.move(barrel.pos.x, barrel.pos.y)):
        print("Столкновение")

    if distance < 0:
        text = font.render('0', 7, (220, 80, 0))
        screen.blit(text_finish, (250, 300))
        screen.blit(text, (120, 20))
        screen.blit(text_exit, (315, 380))
    else:
        screen.blit(text_distance2, (120, 20))

    screen.blit(text_speed, (0, 0))
    screen.blit(text_speed2, (90, 0))
    screen.blit(text_distance, (0, 20))
    screen.blit(text_exit, (790, 0))

    if road.pos.y > car.speed.y + road.pos.y:
        distance -= int(car.speed.len)
    elif road.pos.y < car.speed.y + road.pos.y:
        screen.blit(text_wrong_way, (250, 300))
        distance += int(car.speed.len)
    pygame.display.flip()
