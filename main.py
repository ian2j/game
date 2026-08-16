import constants.dimensions as dms
import screens.menu_start as sns
import pygame
pygame.init()

if __name__ == "__main__":

    screen = pygame.display.set_mode((dms.SCREEN_WIDTH, dms.SCREEN_HEIGHT))
    pygame.display.set_caption(title="Luna's Adventure")
    sns.show_start_menu(screen=screen)