import pygame

import objects.menu_widgets as mnw
import screens.menu_start
import screens.overworld
import screens.scene_base as scb

OPTIONS = ["Unpause", "Luna's Room", "Main Menu", "Quit"]


class PauseMenuScene(scb.Scene):
    """Overlays a menu on top of whatever scene called it. Draws no
    background of its own, so the paused scene's last frame stays visible
    underneath - matching how this always looked."""

    def __init__(self, resume_scene, state):
        super().__init__()
        self.resume_scene = resume_scene
        self.state = state
        self.menu = mnw.VerticalMenu(OPTIONS)

    def _activate(self, option):
        if option == "Unpause":
            self.next_scene = self.resume_scene
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
