import pygame


class Button:
    def __init__(self, image, hovered_image, func, *args, **kwargs):
        self.image = self.load(image)
        self.hovered_image = self.load(hovered_image)
        self.rect = self.image.get_rect(**kwargs)
        self.pressed = func
        self.args = args

    @staticmethod
    def load(image):
        if isinstance(image, str):
            return pygame.image.load("res/" + image + ".png").convert_alpha()
        return image

    def draw(self, screen):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(self.hovered_image, self.rect)
        else:
            screen.blit(self.image, self.rect)

    def check_for_click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.pressed(*self.args)

    def pressed(self, *args):
        pass
