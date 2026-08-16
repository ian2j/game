import pygame
pygame.init()

import constants.dimensions as dms
import objects.game_state as gst
import screens.menu_start as sms
import screens.scene_base as scb


if __name__ == "__main__":
    screen = pygame.display.set_mode((dms.SCREEN_WIDTH, dms.SCREEN_HEIGHT))
    pygame.display.set_caption(title="Luna's Adventure")
    state = gst.GameState.load_or_default()
    scb.run(screen, sms.StartMenuScene(state=state))
