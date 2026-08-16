import pygame

import constants.colors as clr
import constants.dimensions as dms
import constants.fonts as fnt
import constants.settings as stt
import functions.visual as viz
import screens.scene_base as scb


class OptionsMenuScene(scb.Scene):
    """Currently just costume selection. return_scene is where "Back" sends
    the player - whichever scene opened the options menu."""

    def __init__(self, state, return_scene):
        super().__init__()
        self.state = state
        self.return_scene = return_scene
        self.costume_names = list(stt.COSTUMES)
        self.costume_index = self.costume_names.index(state.costume)
        self.selected_index = 0  # 0 = costume row, 1 = back button

    def _left_button_rect(self):
        return pygame.Rect(
            dms.SCREEN_WIDTH / 2 - dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH / 2 - 100, 250,
            dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH, dms.OPTIONS_MENU_SMALL_BUTTON_HEIGHT,
        )

    def _right_button_rect(self):
        return pygame.Rect(
            dms.SCREEN_WIDTH / 2 + dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH / 2 + 90, 250,
            dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH, dms.OPTIONS_MENU_SMALL_BUTTON_HEIGHT,
        )

    def _back_button_rect(self):
        return pygame.Rect(
            dms.SCREEN_WIDTH / 2 - dms.OPTIONS_MENU_BACK_BUTTON_WIDTH / 2, 400,
            dms.OPTIONS_MENU_BACK_BUTTON_WIDTH, dms.OPTIONS_MENU_SMALL_BUTTON_HEIGHT,
        )

    def _cycle_costume(self, direction):
        self.costume_index = (self.costume_index + direction) % len(self.costume_names)

    def _confirm_and_leave(self):
        self.state.costume = self.costume_names[self.costume_index]
        self.next_scene = self.return_scene

    def handle_event(self, event, screen):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._left_button_rect().collidepoint(event.pos):
                self._cycle_costume(-1)
            elif self._right_button_rect().collidepoint(event.pos):
                self._cycle_costume(1)
            elif self._back_button_rect().collidepoint(event.pos):
                self._confirm_and_leave()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and self.selected_index == 0:
                self._cycle_costume(-1)
            elif event.key == pygame.K_RIGHT and self.selected_index == 0:
                self._cycle_costume(1)
            elif event.key == pygame.K_UP and self.selected_index > 0:
                self.selected_index -= 1
            elif event.key == pygame.K_DOWN and self.selected_index < 1:
                self.selected_index += 1
            elif event.key == pygame.K_RETURN and self.selected_index == 1:
                self._confirm_and_leave()
            elif event.key == pygame.K_ESCAPE:
                self._confirm_and_leave()

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(clr.LIGHT_GREY)

        title_text = fnt.font.render("Options", True, clr.BLACK)
        screen.blit(title_text, (dms.SCREEN_WIDTH / 2 - 105, dms.SCREEN_HEIGHT / 10))

        if self.selected_index == 0:
            viz.draw_rectangle(
                screen=screen,
                x=dms.SCREEN_WIDTH / 2 - dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH / 2 - 120, y=240,
                width=dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH + 20, height=dms.OPTIONS_MENU_SMALL_BUTTON_HEIGHT + 20,
                color=clr.BLACK,
            )
            viz.draw_rectangle(
                screen=screen,
                x=dms.SCREEN_WIDTH / 2 + dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH / 2 + 80, y=240,
                width=dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH + 20, height=dms.OPTIONS_MENU_SMALL_BUTTON_HEIGHT + 20,
                color=clr.BLACK,
            )
        elif self.selected_index == 1:
            viz.draw_rectangle(
                screen=screen,
                x=dms.SCREEN_WIDTH / 2 - dms.OPTIONS_MENU_BACK_BUTTON_WIDTH / 2 - 10, y=390,
                width=dms.OPTIONS_MENU_BACK_BUTTON_WIDTH + 20, height=dms.OPTIONS_MENU_BACK_BUTTON_HEIGHT + 20,
                color=clr.BLACK,
            )

        viz.draw_button(
            screen=screen, font=fnt.small_font, text="<",
            x=dms.SCREEN_WIDTH / 2 - dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH / 2 - 110, y=250,
            width=dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH, height=dms.OPTIONS_MENU_SMALL_BUTTON_HEIGHT,
            button_color=clr.LIGHT_RED, text_color=clr.BLACK,
        )
        viz.draw_button(
            screen=screen, font=fnt.small_font, text=">",
            x=dms.SCREEN_WIDTH / 2 + dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH / 2 + 90, y=250,
            width=dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH, height=dms.OPTIONS_MENU_SMALL_BUTTON_HEIGHT,
            button_color=clr.LIGHT_RED, text_color=clr.BLACK,
        )

        costume_name = self.costume_names[self.costume_index]
        costume_option_label = fnt.small_font.render("Costume: ", True, clr.BLACK)
        screen.blit(costume_option_label, (dms.SCREEN_WIDTH / 2 - dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH / 2 - 275, 260))
        costume_text = fnt.small_font.render(costume_name, True, clr.BLACK)
        screen.blit(costume_text, (dms.SCREEN_WIDTH / 2 - 10 * len(costume_name) / 2, 260))

        viz.draw_button(
            screen=screen, font=fnt.small_font, text="Back",
            x=dms.SCREEN_WIDTH / 2 - dms.OPTIONS_MENU_BACK_BUTTON_WIDTH / 2, y=400,
            width=dms.OPTIONS_MENU_BACK_BUTTON_WIDTH, height=dms.OPTIONS_MENU_SMALL_BUTTON_HEIGHT,
            button_color=clr.LIGHT_BLUE, text_color=clr.NAVY,
        )
