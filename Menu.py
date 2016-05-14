import sys

import pygame

GREY = (100, 100, 100)


class Menu:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((1000, 800))
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.SysFont("Courier New", 75)
        self.screen.fill(GREY)
        self.text_play_pos = (300, 200)
        self.text_records_pos = (300, 325)
        self.text_quit_pos = (300, 450)

    def render(self):
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if self.text_play_pos[0] - 25 < mouse_pos[0] < self.text_play_pos[0] + 160 \
                    and self.text_play_pos[1] - 50 < mouse_pos[1] < self.text_play_pos[1] + 100:
                self.screen.blit(self.font.render("Play", 21, (0, 0, 0)), self.text_play_pos)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    print('Play')
            else:
                self.screen.blit(self.font.render("Play", 21, (220, 50, 0)), self.text_play_pos)

            if self.text_records_pos[0] - 25 < mouse_pos[0] < self.text_records_pos[0] + 330 \
                    and self.text_records_pos[1] < mouse_pos[1] < self.text_records_pos[1] + 70:
                self.screen.blit(self.font.render("Records", 21, (0, 0, 0)), self.text_records_pos)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    print('Records')
            else:
                self.screen.blit(self.font.render("Records", 21, (220, 50, 0)), self.text_records_pos)

            if self.text_quit_pos[0] - 25 < mouse_pos[0] < self.text_quit_pos[0] + 160\
                    and self.text_quit_pos[1] - 20 < mouse_pos[1] < self.text_quit_pos[1] + 60:
                self.screen.blit(self.font.render("Quit", 21, (0, 0, 0)), self.text_quit_pos)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    print('Quit')
                    # sys.exit()
            else:
                self.screen.blit(self.font.render("Quit", 21, (220, 50, 0)), self.text_quit_pos)
        pygame.display.flip()

    def run(self):
        while True:
            self.render()

if __name__ == '__main__':
    menu = Menu()
    menu.run()
