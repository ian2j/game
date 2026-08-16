import pygame
import screens.menu_start
import screens.menu_options
import screens.overworld
import constants.dimensions as dms
import constants.colors as clr
import constants.fonts as fnt
import functions.audio as aud
import functions.visual as viz
import sys


def show_end_minigame_menu(screen, game_variables, game_screen):

    pause_menu_options = [
        'Play Again',
        "Luna's Room",
        'Main Menu',
        'Quit',
    ]
    n_indices = len(pause_menu_options)
    pause_menu_selected_index = 0
    clock = pygame.time.Clock()

    running = True

    while running:

        viz.draw_rectangle(
            screen=screen,
            x=dms.SCREEN_WIDTH/2-dms.PAUSE_MENU_WIDTH/2-10,
            y=140,
            width=dms.PAUSE_MENU_WIDTH + 20,
            height=dms.PAUSE_MENU_HEIGHT + 20,
            color=clr.BLACK
        )

        viz.draw_rectangle(
            screen=screen,
            x=dms.SCREEN_WIDTH/2-dms.PAUSE_MENU_WIDTH/2,
            y=150,
            width=dms.PAUSE_MENU_WIDTH,
            height=dms.PAUSE_MENU_HEIGHT,
            color=clr.WHITE
        )

        PAUSE_MENU_TEXT_RANGE_START = 190
        PAUSE_MENU_TEXT_RANGE_END = 190+dms.PAUSE_MENU_HEIGHT-40
        PAUSE_MENU_TEXT_RANGE = PAUSE_MENU_TEXT_RANGE_END - PAUSE_MENU_TEXT_RANGE_START
        PAUSE_MENU_TEXT_POSITIONS = [
            PAUSE_MENU_TEXT_RANGE_START + i/n_indices * PAUSE_MENU_TEXT_RANGE for i in range(n_indices)
        ]
        for i in range(n_indices):
            color_i = clr.BLACK if i != pause_menu_selected_index else clr.BLUE
            option_i_text = fnt.small_font.render(pause_menu_options[i], True, color_i)
            screen.blit(
                option_i_text,
                (dms.SCREEN_WIDTH/2-10*len(pause_menu_options[i])/2, PAUSE_MENU_TEXT_POSITIONS[i])
            )

        pygame.display.flip()  # Update the screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Close the window
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Get key states
                keys = pygame.key.get_pressed()

                if keys[pygame.K_DOWN]:
                    if pause_menu_selected_index < n_indices:
                        pause_menu_selected_index += 1

                if keys[pygame.K_UP]:
                    if pause_menu_selected_index > 0:
                        pause_menu_selected_index -= 1

                if keys[pygame.K_RETURN]:
                    if pause_menu_options[pause_menu_selected_index] == 'Play Again':
                        game_screen(screen=screen, game_variables=game_variables)
                    elif pause_menu_options[pause_menu_selected_index] == "Luna's Room":
                        aud.stop_music()
                        screens.overworld.show_overworld(screen=screen, game_variables=game_variables)
                    elif pause_menu_options[pause_menu_selected_index] == 'Main Menu':
                        aud.stop_music()
                        screens.menu_start.show_start_menu(screen=screen, game_variables=game_variables)
                    elif pause_menu_options[pause_menu_selected_index] == 'Quit':
                        pygame.mixer.music.stop()
                        pygame.quit()
                        sys.exit()

        clock.tick(60)
    return None
