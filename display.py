import pygame


class Display:
    BACKGROUND_LINE_SPACING = 24
    BACKGROUND_LINE_COLOR = (100, 100, 100)
    BACKGROUND_COLOR = (50, 50, 50)
    FPS = 60

    def __init__(self, width, height):
        self.size = (width, height)
        self.image = pygame.display.set_mode(self.size)
        pygame.display.set_caption("PyPaint")
        icon = pygame.Surface((32, 32))
        pygame.draw.rect(icon, (255, 255, 255), pygame.Rect(0, 0, 32, 32))
        pygame.draw.rect(icon, (0, 0, 0), pygame.Rect(8, 8, 16, 16))
        icon = icon.convert_alpha()
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()

    def draw_background(self):
        self.image.fill(self.BACKGROUND_COLOR)
        spacing = self.BACKGROUND_LINE_SPACING

        for x in range(spacing, self.size[0], spacing):
            pygame.draw.line(self.image, self.BACKGROUND_LINE_COLOR, (x, 0), (x, self.size[1]))
        for y in range(spacing, self.size[1], spacing):
            pygame.draw.line(self.image, self.BACKGROUND_LINE_COLOR, (0, y), (self.size[0], y))

    def update(self):
        pygame.display.flip()
        self.clock.tick(self.FPS)
