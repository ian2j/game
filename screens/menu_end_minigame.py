import pygame

import objects.menu_widgets as mnw
import screens.menu_start
import screens.overworld
import screens.scene_base as scb

OPTIONS = ["Play Again", "Luna's Room", "Main Menu", "Quit"]


class EndMinigameScene(scb.Scene):
    """Shown after a minigame ends. minigame_factory is a zero-arg callable
    that builds a fresh instance of the same minigame, for "Play Again"."""

    def __init__(self, minigame_factory, state):
        super().__init__()
        self.minigame_factory = minigame_factory
        self.state = state
        self.menu = mnw.VerticalMenu(OPTIONS)

    def _activate(self, option):
        if option == "Play Again":
            self.next_scene = self.minigame_factory()
        elif option == "Luna's Room":
            self.next_scene = screens.overworld.OverworldScene(state=self.state, room_id=self.state.current_room)
        elif option == "Main Menu":
            self.next_scene = screens.menu_start.StartMenuScene(state=self.state)
        elif option == "Quit":
            self.next_scene = scb.QUIT

    def handle_event(self, event, screen):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.menu.move_down()
            elif event.key == pygame.K_UP:
                self.menu.move_up()
            elif event.key == pygame.K_RETURN:
                self._activate(self.menu.selected_option)

    def update(self, dt):
        pass

    def draw(self, screen):
        self.menu.draw(screen)
