import constants.colors as clr
import constants.dimensions as dms
import constants.fonts as fnt
import functions.visual as viz


class VerticalMenu:
    """A boxed, vertically-stacked list of text options with keyboard
    navigation and a highlighted selection. Shared by the pause menu and the
    end-of-minigame menu, which were previously two copies of the same
    rendering code."""

    def __init__(self, options, box_y=140, box_width=dms.PAUSE_MENU_WIDTH, box_height=dms.PAUSE_MENU_HEIGHT):
        self.options = options
        self.selected_index = 0
        self.box_x = dms.SCREEN_WIDTH / 2 - box_width / 2
        self.box_y = box_y
        self.box_width = box_width
        self.box_height = box_height

    def move_up(self):
        if self.selected_index > 0:
            self.selected_index -= 1

    def move_down(self):
        if self.selected_index < len(self.options) - 1:
            self.selected_index += 1

    @property
    def selected_option(self):
        return self.options[self.selected_index]

    def draw(self, screen):
        viz.draw_rectangle(
            screen=screen,
            x=self.box_x - 10, y=self.box_y - 10,
            width=self.box_width + 20, height=self.box_height + 20,
            color=clr.BLACK,
        )
        viz.draw_rectangle(
            screen=screen,
            x=self.box_x, y=self.box_y,
            width=self.box_width, height=self.box_height,
            color=clr.WHITE,
        )

        n = len(self.options)
        text_range_start = self.box_y + 40
        text_range_end = self.box_y + self.box_height
        text_range = text_range_end - text_range_start
        positions = [text_range_start + i / n * text_range for i in range(n)]

        for i, option in enumerate(self.options):
            color = clr.BLUE if i == self.selected_index else clr.BLACK
            text_surface = fnt.small_font.render(option, True, color)
            screen.blit(text_surface, (dms.SCREEN_WIDTH / 2 - 10 * len(option) / 2, positions[i]))
