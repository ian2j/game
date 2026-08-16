import pygame
import screens.menu_options
import screens.overworld
import screens.game_letter_matching
import constants.dimensions as dms
import constants.colors as clr
import constants.fonts as fnt
import constants.flags as flg
import constants.settings as stt
import functions.audio as aud
import functions.visual as viz
from datetime import datetime
import numpy as np
import sys


def show_start_menu(screen, game_variables=None):

    today = datetime.today()
    ymd = int(f"{today.year}{today.month}{today.day}")
    np.random.seed(ymd)
    # np.random.seed(1118)

    if game_variables is None:
        game_variables = {
            'options': {
                'costume': stt.DEFAULT_COSTUME
            },
            'variables': {
                'player_costume_sprite': stt.COSTUMES[stt.DEFAULT_COSTUME],
                'player_scale': stt.PLAYER_SCALE,
                'player_position': (
                    dms.SCREEN_WIDTH / 2 - stt.PLAYER_FRAME_WIDTH * stt.PLAYER_SCALE / 2,
                    dms.SCREEN_HEIGHT / 2 - stt.PLAYER_FRAME_HEIGHT * stt.PLAYER_SCALE / 2
                ),
                'player_direction': 'down'
            }
        }

    if not flg.PYGAME_MIXER_INITIALIZED:
        aud.start_mixer()
    aud.load_music(filename="sounds/sample_music_1.mp3")
    aud.play_music_on_loop()
    clock = pygame.time.Clock()

    # The Start Menu currently has 3 selections:
    # > Start Game
    # > Options
    # > Quit
    selected_index = 0
    n_indices = 3

    running = True

    while running:


        screen.fill(clr.LIGHT_GREY)

        title_text = fnt.font.render("Luna's Adventure", True, clr.BLACK)
        screen.blit(title_text, (dms.SCREEN_WIDTH/2-210, dms.SCREEN_HEIGHT/10))

        start_button = pygame.Rect(
            dms.SCREEN_WIDTH/2-dms.MAIN_MENU_BUTTON_WIDTH/2,
            250,
            dms.MAIN_MENU_BUTTON_WIDTH,
            dms.MAIN_MENU_BUTTON_HEIGHT
        )
        options_button = pygame.Rect(
            dms.SCREEN_WIDTH/2-dms.MAIN_MENU_BUTTON_WIDTH/2,
            320,
            dms.MAIN_MENU_BUTTON_WIDTH,
            dms.MAIN_MENU_BUTTON_HEIGHT
        )
        quit_button = pygame.Rect(
            dms.SCREEN_WIDTH/2-dms.MAIN_MENU_BUTTON_WIDTH/2,
            390,
            dms.MAIN_MENU_BUTTON_WIDTH,
            dms.MAIN_MENU_BUTTON_HEIGHT
        )

        if selected_index == 0:
            viz.draw_rectangle(
                screen=screen,
                x=dms.SCREEN_WIDTH / 2 - dms.MAIN_MENU_BUTTON_WIDTH / 2 - 10,
                y=240,
                width=dms.MAIN_MENU_BUTTON_WIDTH + 20,
                height=dms.MAIN_MENU_BUTTON_HEIGHT + 20,
                color=clr.BLACK
            )
        elif selected_index == 1:
            viz.draw_rectangle(
                screen=screen,
                x=dms.SCREEN_WIDTH / 2 - dms.MAIN_MENU_BUTTON_WIDTH / 2 - 10,
                y=310,
                width=dms.MAIN_MENU_BUTTON_WIDTH + 20,
                height=dms.MAIN_MENU_BUTTON_HEIGHT + 20,
                color=clr.BLACK
            )
        elif selected_index == 2:
            viz.draw_rectangle(
                screen=screen,
                x=dms.SCREEN_WIDTH / 2 - dms.MAIN_MENU_BUTTON_WIDTH / 2 - 10,
                y=380,
                width=dms.MAIN_MENU_BUTTON_WIDTH + 20,
                height=dms.MAIN_MENU_BUTTON_HEIGHT + 20,
                color=clr.BLACK
            )

        viz.draw_button(
            screen=screen,
            font=fnt.small_font,
            text="Start Game",
            x=dms.SCREEN_WIDTH/2-dms.MAIN_MENU_BUTTON_WIDTH/2,
            y=250,
            width=dms.MAIN_MENU_BUTTON_WIDTH,
            height=dms.MAIN_MENU_BUTTON_HEIGHT,
            button_color=clr.LIGHT_BLUE,
            text_color=clr.BLACK if selected_index != 0 else clr.NAVY
        )
        viz.draw_button(
            screen=screen,
            font=fnt.small_font,
            text="Options",
            x=dms.SCREEN_WIDTH/2-dms.MAIN_MENU_BUTTON_WIDTH/2,
            y=320,
            width=dms.MAIN_MENU_BUTTON_WIDTH,
            height=dms.MAIN_MENU_BUTTON_HEIGHT,
            button_color=clr.LIGHT_GREEN,
            text_color=clr.BLACK if selected_index != 1 else clr.NAVY
        )
        viz.draw_button(
            screen=screen,
            text="Quit",
            font=fnt.small_font,
            x=dms.SCREEN_WIDTH/2-dms.MAIN_MENU_BUTTON_WIDTH/2,
            y=390,
            width=dms.MAIN_MENU_BUTTON_WIDTH,
            height=dms.MAIN_MENU_BUTTON_HEIGHT,
            button_color=clr.LIGHT_RED,
            text_color=clr.BLACK if selected_index != 2 else clr.NAVY
        )

        pygame.display.flip()  # Update the screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Close the window
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Handle mouse clicks
                if start_button.collidepoint(event.pos):
                    aud.stop_music()
                    screens.overworld.show_overworld(screen=screen, game_variables=game_variables)
                elif options_button.collidepoint(event.pos):
                    game_variables = screens.menu_options.show_options_menu(
                        screen=screen, game_variables=game_variables
                    )
                elif quit_button.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                # Get key states
                keys = pygame.key.get_pressed()
                if keys[pygame.K_DOWN] and selected_index < n_indices - 1:
                    selected_index += 1
                elif keys[pygame.K_UP] and selected_index > 0:
                    selected_index -= 1
                elif keys[pygame.K_RETURN]:
                    if selected_index == 0:
                        aud.stop_music()
                        screens.overworld.show_overworld(screen=screen, game_variables=game_variables)
                    elif selected_index == 1:
                        game_variables = screens.menu_options.show_options_menu(
                            screen=screen, game_variables=game_variables
                        )
                    elif selected_index == 2:
                        pygame.mixer.music.stop()
                        pygame.quit()
                        sys.exit()
                elif keys[pygame.K_ESCAPE]:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()

        clock.tick(stt.FRAMES_PER_SECOND)
