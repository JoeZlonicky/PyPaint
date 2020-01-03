import pygame
from panel import Panel
from button import Button


class SaveMenu:
    def __init__(self):
        self.name = "Painting"
        self.font = pygame.font.Font("res/upheavtt.ttf", 36)
        self.panel = Panel(350, 150, centerx=int(pygame.display.get_surface().get_width() / 2),
                           centery=int(pygame.display.get_surface().get_height() / 2))
        self.label_rect = pygame.Rect(0, 0, 310, 40)
        self.label_rect.centerx = self.panel.rect.centerx
        self.label_rect.centery = self.panel.rect.centery
        self.close_button = Button("close", "close_hovered", self.close_window,
                                   top=self.panel.rect.top + 2, right = self.panel.rect.right - 2)
        self.close = False

    def loop(self, program):
        while not self.close:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    self.handle_keypress(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.close_button.check_for_click()
            program.draw()
            program.display.image.blit(self.panel.image, self.panel.rect)
            self.draw_label(program.display.image)
            self.close_button.draw(program.display.image)
            program.display.update()

    def draw_label(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.label_rect)
        label = self.font.render(self.name, True, (255, 255, 255))
        rect = label.get_rect(center=self.label_rect.center)
        screen.blit(label, rect)

    def close_window(self):
        self.close = True

    def handle_keypress(self, key):
        if key == pygame.K_BACKSPACE:
            if len(self.name) > 0:
                self.name = self.name[:-1]
        elif pygame.K_a <= key <= pygame.K_z or key == pygame.K_SPACE:
            if self.font.size(self.name + chr(key))[0] < self.label_rect.width - 2:
                self.name += chr(key)
