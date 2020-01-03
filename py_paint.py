import pygame
from painting import Painting
from display import Display
from tool import Tool
from panel import Panel
from button import Button
from save_menu import SaveMenu


# TODO: Add more buttons: Zoom, colors, new, clear, save
# TODO: Work on zooming-in lag

class PyPaint:
    DISPLAY_SIZE = (720, 720)
    COLORS = [(0, 0, 0), (128, 128, 128), (255, 255, 255), (255, 0, 0), (0, 255, 0),
              (0, 0, 255), (255, 255, 0), (255, 0, 255)]

    def __init__(self):
        pygame.init()
        self.display = Display(self.DISPLAY_SIZE[0], self.DISPLAY_SIZE[1])
        self.painting = Painting(pygame.image.load("paintings/pic.png"))
        self.panel = Panel(self.DISPLAY_SIZE[0], 100)
        self.color = (255, 255, 255)
        self.tool = Tool.brush
        self.mouse_pos = pygame.mouse.get_pos()
        self.brush_started = False
        self.menu_switch_delay = 0

        brush_button = Button("brush", "brush_hovered", self.change_tool, Tool.brush,
                              centery=self.panel.rect.centery, left=self.panel.rect.left + 16)

        bucket_button = Button("bucket", "bucket_hovered", self.change_tool, Tool.bucket,
                               centery=self.panel.rect.centery, left=self.panel.rect.left + 96)

        home_button = Button("home", "home_hovered", self.painting.reset_position_and_zoom,
                             centery=self.panel.rect.centery, right=self.panel.rect.right - 16)

        clear_button = Button("clear", "clear_hovered", self.painting.clear,
                              bottom=self.panel.rect.centery - 3, left=self.panel.rect.centerx + 102)

        new_button = Button("new", "new_hovered", self.go_to_save_menu, top=self.panel.rect.centery + 3,
                            left=self.panel.rect.centerx + 102)

        undo_button = Button("undo", "undo_hovered", self.painting.undo,
                             left=clear_button.rect.right + 24, bottom=self.panel.rect.centery - 3)

        redo_button = Button("redo", "redo_hovered", self.painting.redo,
                             left=new_button.rect.right + 24, top=self.panel.rect.centery + 3)

        self.buttons = [brush_button, bucket_button, home_button, clear_button,
                        new_button, undo_button, redo_button]
        self.make_color_buttons()

    def loop(self):
        while True:
            self.handle_events()
            if self.tool == Tool.brush and pygame.mouse.get_pressed()[0]:
                self.draw_with_brush()
            else:
                self.brush_started = False
            self.handle_move_keys()
            self.mouse_pos = pygame.mouse.get_pos()
            self.draw()
            self.display.update()
            self.menu_switch_delay = max(self.menu_switch_delay - 1, 0)

    def draw(self):
        self.display.draw_background()
        self.display.image.blit(self.painting.get_scaled_image(), self.painting.get_rect())
        self.display.image.blit(self.panel.image, self.panel.rect)
        for button in self.buttons:
            button.draw(self.display.image)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_EQUALS:
                    self.painting.zoom_in()
                elif event.key == pygame.K_MINUS:
                    self.painting.zoom_out()
                elif event.key == pygame.K_s:
                    self.save()
                elif event.key == pygame.K_ESCAPE:
                    self.painting.clear()
                elif event.key == pygame.K_z and pygame.KMOD_CTRL:
                    self.painting.undo()
                elif event.key == pygame.K_y and pygame.KMOD_CTRL:
                    self.painting.redo()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.tool == Tool.bucket:
                        self.use_bucket()
                    for button in self.buttons:
                        button.check_for_click()
                elif event.button == 4:
                    self.painting.zoom_in()
                elif event.button == 5:
                    self.painting.zoom_out()

    def handle_move_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.painting.move_up()
        if keys[pygame.K_RIGHT]:
            self.painting.move_right()
        if keys[pygame.K_DOWN]:
            self.painting.move_down()
        if keys[pygame.K_LEFT]:
            self.painting.move_left()

    def draw_with_brush(self):
        if not self.mouse_is_over_panel() and self.menu_switch_delay == 0:
            if not self.brush_started:
                self.painting.save_state()
            painting_rect = self.painting.get_rect()
            old_pos = self.painting.scale_pos((self.mouse_pos[0] - painting_rect.x,
                                              self.mouse_pos[1] - painting_rect.y))
            new_pos = self.painting.scale_pos((pygame.mouse.get_pos()[0] - painting_rect.x,
                                               pygame.mouse.get_pos()[1] - painting_rect.y))
            self.painting.draw_line(old_pos, new_pos, self.color)
            self.brush_started = True

    def use_bucket(self):
        if not self.mouse_is_over_panel() and self.menu_switch_delay == 0:
            painting_rect = self.painting.get_rect()
            mouse_pos = pygame.mouse.get_pos()
            pos = self.painting.scale_pos((mouse_pos[0] - painting_rect.x, mouse_pos[1] - painting_rect.y))
            if painting_rect.collidepoint(mouse_pos):
                self.painting.flood_fill(pos[0], pos[1], self.color)

    def mouse_is_over_panel(self):
        return self.panel.rect.collidepoint(pygame.mouse.get_pos())

    def save(self):
        pygame.image.save(self.painting.image, "painting.png")

    def go_to_save_menu(self):
        SaveMenu().loop(self)
        self.menu_switch_delay = 30

    def change_tool(self, tool):
        self.tool = tool

    def change_color(self, color):
        self.color = color

    def make_color_buttons(self):
        hover_change = 40
        size = 32
        offset = 3
        for y in range(2):
            for x in range(4):
                color = self.COLORS[y*4 + x]

                if color[0] > 128 or color[1] > 128 or color[2] > 128:
                    r = max(color[0] - hover_change, 0)
                    g = max(color[1] - hover_change, 0)
                    b = max(color[2] - hover_change, 0)
                else:
                    r = min(color[0] + hover_change, 255)
                    g = min(color[1] + hover_change, 255)
                    b = min(color[2] + hover_change, 255)
                image = pygame.Surface((size, size))
                hovered_image = image.copy()
                image.fill(color)
                hovered_image.fill((r, g, b))
                rect_x = int(self.DISPLAY_SIZE[0] / 2) - 2 * size - int(offset * 1.5)
                rect_x += x * size + x * offset
                rect_y = int(self.panel.rect.height / 2) - offset - size
                if y == 1:
                    rect_y += size + offset*2
                self.buttons.append(Button(image, hovered_image, self.change_color,
                                           color, x=rect_x, y=rect_y))


if __name__ == "__main__":
    PyPaint().loop()
