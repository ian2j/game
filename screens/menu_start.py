import pygame

import constants.colors as clr
import constants.dimensions as dms
import constants.fonts as fnt
import functions.audio as aud
import functions.visual as viz
import screens.menu_options
import screens.overworld
import screens.scene_base as scb

BUTTONS = [
    ("Start Game", clr.LIGHT_BLUE, 250),
    ("Options", clr.LIGHT_GREEN, 320),
    ("Quit", clr.LIGHT_RED, 390),
]


class StartMenuScene(scb.Scene):
    def __init__(self, state):
        super().__init__()
        self.state = state
        self.selected_index = 0
        aud.play_looping_track(filename="sounds/sample_music_1.mp3")

    def _button_rect(self, index):
        _, _, y = BUTTONS[index]
        return pygame.Rect(
            dms.SCREEN_WIDTH / 2 - dms.MAIN_MENU_BUTTON_WIDTH / 2, y,
            dms.MAIN_MENU_BUTTON_WIDTH, dms.MAIN_MENU_BUTTON_HEIGHT,
        )

    def _activate(self, index):
        if index == 0:
            self.next_scene = screens.overworld.OverworldScene(state=self.state, room_id=self.state.current_room)
        elif index == 1:
            self.next_scene = screens.menu_options.OptionsMenuScene(state=self.state, return_scene=self)
        elif index == 2:
            self.next_scene = scb.QUIT

    def handle_event(self, event, screen):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(BUTTONS)):
                if self._button_rect(i).collidepoint(event.pos):
                    self._activate(i)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and self.selected_index < len(BUTTONS) - 1:
                self.selected_index += 1
            elif event.key == pygame.K_UP and self.selected_index > 0:
                self.selected_index -= 1
            elif event.key == pygame.K_RETURN:
                self._activate(self.selected_index)
            elif event.key == pygame.K_ESCAPE:
                self.next_scene = scb.QUIT

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(clr.LIGHT_GREY)

        title_text = fnt.font.render("Luna's Adventure", True, clr.BLACK)
        screen.blit(title_text, (dms.SCREEN_WIDTH / 2 - 210, dms.SCREEN_HEIGHT / 10))

        for i, (label, color, y) in enumerate(BUTTONS):
            if i == self.selected_index:
                viz.draw_rectangle(
                    screen=screen,
                    x=dms.SCREEN_WIDTH / 2 - dms.MAIN_MENU_BUTTON_WIDTH / 2 - 10,
                    y=y - 10,
                    width=dms.MAIN_MENU_BUTTON_WIDTH + 20,
                    height=dms.MAIN_MENU_BUTTON_HEIGHT + 20,
                    color=clr.BLACK,
                )
            viz.draw_button(
                screen=screen,
                font=fnt.small_font,
                text=label,
                x=dms.SCREEN_WIDTH / 2 - dms.MAIN_MENU_BUTTON_WIDTH / 2,
                y=y,
                width=dms.MAIN_MENU_BUTTON_WIDTH,
                height=dms.MAIN_MENU_BUTTON_HEIGHT,
                button_color=color,
                text_color=clr.NAVY if i == self.selected_index else clr.BLACK,
            )
