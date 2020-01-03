import pygame
import numpy


class Painting:
    BASE_COLOUR = (255, 255, 255)
    ZOOM_RATE = 0.5
    MOVE_SPEED = 0.5

    def __init__(self, image, width=None, height=None):
        if not image:
            self.image = pygame.Surface((width, height))
            self.clear()
        else:
            self.image = image.convert(8)
        self.x_offset, self.y_offset = 0.0, 0.0
        self.zoom = 1
        self.reset_position_and_zoom()
        self.undone = None
        self.redone = None

    def get_rect(self):
        width = int(self.image.get_width() * self.zoom)
        height = int(self.image.get_height() * self.zoom)
        x = int(pygame.display.get_surface().get_width() / 2 - width / 2 + self.x_offset * self.zoom)
        y = int(pygame.display.get_surface().get_height() / 2 - height / 2 + self.y_offset * self.zoom)
        return pygame.Rect(x, y, width, height)

    def get_scaled_image(self):
        return pygame.transform.scale(self.image, self.get_rect().size)

    def draw_line(self, start, end, color):
        pygame.draw.line(self.image, color, start, end)

    def flood_fill(self, x, y, color):
        color = self.image.map_rgb(color)
        surface_arr = pygame.surfarray.pixels2d(self.image)
        color_to_replace = surface_arr[x, y]
        if color == color_to_replace:
            return
        self.undone = self.image.copy()

        coords = [(x, y)]
        while len(coords) > 0:
            x, y = coords.pop()
            try:
                if surface_arr[x, y] != color_to_replace:
                    continue
            except IndexError:
                continue
            surface_arr[x, y] = color
            coords.append((x + 1, y))
            coords.append((x - 1, y))
            coords.append((x, y + 1))
            coords.append((x, y - 1))

    def clear(self):
        after = self.image.copy()
        after.fill(self.BASE_COLOUR)
        if not numpy.array_equal(pygame.surfarray.array2d(after), pygame.surfarray.array2d(self.image)):
            self.save_state()
        self.image.fill(self.BASE_COLOUR)

    def scale_pos(self, pos):
        x = int(pos[0] / self.zoom)
        y = int(pos[1] / self.zoom)
        return x, y

    def zoom_in(self):
        self.zoom *= 1 + self.ZOOM_RATE

    def zoom_out(self):
        if self.get_rect().width <= 32 or self.get_rect().height <= 32:
            return
        self.zoom *= 1 - self.ZOOM_RATE

    def move_up(self):
        self.y_offset += self.MOVE_SPEED

    def move_right(self):
        self.x_offset -= self.MOVE_SPEED

    def move_down(self):
        self.y_offset -= self.MOVE_SPEED

    def move_left(self):
        self.x_offset += self.MOVE_SPEED

    def reset_position_and_zoom(self):
        self.x_offset, self.y_offset = 0.0, 0.0
        self.zoom = 0.1
        display_size = pygame.display.get_surface().get_size()
        while self.get_rect().height < display_size[1] / 2 and self.get_rect().width < display_size[0] / 2:
            self.zoom_in()

    def save_state(self):
        self.undone = self.image.copy()
        self.redone = None

    def undo(self):
        if self.undone:
            self.redone = self.image.copy()
            self.image = self.undone.copy()
            self.undone = None

    def redo(self):
        if self.redone:
            self.undone = self.image.copy()
            self.image = self.redone.copy()
            self.redone = None
