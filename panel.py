import pygame


class Panel:
    COLOR = (50, 50, 50)
    OUTLINE_COLOR = (160, 160, 160)

    def __init__(self, width, height, **kwargs):
        self.image = pygame.Surface((width, height))
        self.image.fill(self.COLOR)
        self.rect = self.image.get_rect(**kwargs)
        pygame.draw.rect(self.image, self.OUTLINE_COLOR,
                         (0, 0, self.rect.width, self.rect.height), 1)
