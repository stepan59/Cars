import sys

import pygame

GREY = (100, 100, 100)


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.mouse_pos = None

    def render(self, text_play, text_records, text_quit):
        self.mouse_pos = pygame.mouse.get_pos()
        self.screen.fill(GREY)
        self.screen.blit(text_play[0], text_play[1])
        self.screen.blit(text_records[0], text_records[1])
        self.screen.blit(text_quit[0], text_quit[1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if text_play[1][0] - 65 < self.mouse_pos[0] < text_play[1][0] + 65 \
                    and text_play[1][1] - 50 < self.mouse_pos[1] < text_play[1][1] + 50:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.M:
                        print('Play')
            elif text_records[1][0] - 65 < self.mouse_pos[0] < text_records[1][0] + 65 \
                    and text_records[1][1] - 50 < self.mouse_pos[1] < text_records[1][1] + 50:
                    print('Records')
            elif text_quit[1][0] - 65 < self.mouse_pos[0] < text_quit[1][0] + 65 \
                    and text_quit[1][1] - 50 < self.mouse_pos[1] < text_quit[1][1] + 50:
                    print('Quit')

        pygame.display.flip()
