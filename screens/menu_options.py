import pygame
import constants.dimensions as dms
import constants.colors as clr
import constants.settings as stt
import constants.fonts as fnt
import functions.visual as viz
import sys


costume_indices = {
    label: index for index, label in enumerate(stt.COSTUMES)
}
costume_indices_reverse = {
    index: label for index, label in enumerate(stt.COSTUMES)
}
n_costume_indices = len(costume_indices)


def show_options_menu(screen, game_variables):

    running = True
    costume_selection_index = costume_indices[game_variables['options']['costume']]

    selected_index = 0
    n_indices = 2  # Currently we only have the costume selection and the back button

    while running:
        screen.fill(clr.LIGHT_GREY)

        title_text = fnt.font.render("Options", True, clr.BLACK)
        screen.blit(title_text, (dms.SCREEN_WIDTH/2-105, dms.SCREEN_HEIGHT/10))

        costume_left_button = pygame.Rect(
            dms.SCREEN_WIDTH/2-dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH/2-100,
            250,
            dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH,
            dms.OPTIONS_MENU_SMALL_BUTTON_HEIGHT
        )

        costume_right_button = pygame.Rect(
            dms.SCREEN_WIDTH/2+dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH/2+90,
            250,
            dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH,
            dms.OPTIONS_MENU_SMALL_BUTTON_HEIGHT
        )

        back_button = pygame.Rect(
            dms.SCREEN_WIDTH / 2 - dms.OPTIONS_MENU_BACK_BUTTON_WIDTH / 2,
            400,
            dms.OPTIONS_MENU_BACK_BUTTON_WIDTH,
            dms.OPTIONS_MENU_SMALL_BUTTON_HEIGHT
        )

        if selected_index == 0:
            viz.draw_rectangle(
                screen=screen,
                x=dms.SCREEN_WIDTH/2-dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH/2-120,
                y=240,
                width=dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH + 20,
                height=dms.OPTIONS_MENU_SMALL_BUTTON_HEIGHT + 20,
                color=clr.BLACK
            )
            viz.draw_rectangle(
                screen=screen,
                x=dms.SCREEN_WIDTH/2+dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH/2+80,
                y=240,
                width=dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH + 20,
                height=dms.OPTIONS_MENU_SMALL_BUTTON_HEIGHT + 20,
                color=clr.BLACK
            )
        elif selected_index == 1:
            viz.draw_rectangle(
                screen=screen,
                x=dms.SCREEN_WIDTH / 2 - dms.OPTIONS_MENU_BACK_BUTTON_WIDTH / 2 - 10,
                y=390,
                width=dms.OPTIONS_MENU_BACK_BUTTON_WIDTH + 20,
                height=dms.OPTIONS_MENU_BACK_BUTTON_HEIGHT + 20,
                color=clr.BLACK
            )

        viz.draw_button(
            screen=screen,
            font=fnt.small_font,
            text="<",
            x=dms.SCREEN_WIDTH/2-dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH/2-110,
            y=250,
            width=dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH,
            height=dms.OPTIONS_MENU_SMALL_BUTTON_HEIGHT,
            button_color=clr.LIGHT_RED,
            text_color=clr.BLACK
        )

        viz.draw_button(
            screen=screen,
            font=fnt.small_font,
            text=">",
            x=dms.SCREEN_WIDTH/2+dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH/2+90,
            y=250,
            width=dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH,
            height=dms.OPTIONS_MENU_SMALL_BUTTON_HEIGHT,
            button_color=clr.LIGHT_RED,
            text_color=clr.BLACK
        )

        costume_option_label = fnt.small_font.render("Costume: ", True, clr.BLACK)
        screen.blit(costume_option_label, (dms.SCREEN_WIDTH/2-dms.OPTIONS_MENU_SMALL_BUTTON_WIDTH/2-275, 260))
        costume_text = fnt.small_font.render(
            f"{costume_indices_reverse[costume_selection_index]}", True, clr.BLACK
        )
        costume_text_len = len(costume_indices_reverse[costume_selection_index])
        screen.blit(costume_text, (dms.SCREEN_WIDTH/2-10*costume_text_len/2, 260))

        viz.draw_button(
            screen=screen,
            font=fnt.small_font,
            text="Back",
            x=dms.SCREEN_WIDTH/2-dms.OPTIONS_MENU_BACK_BUTTON_WIDTH/2,
            y=400,
            width=dms.OPTIONS_MENU_BACK_BUTTON_WIDTH,
            height=dms.OPTIONS_MENU_SMALL_BUTTON_HEIGHT,
            button_color=clr.LIGHT_BLUE,
            text_color=clr.NAVY
        )
        pygame.display.flip()  # Update the screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Close the window
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Handle mouse clicks
                if costume_left_button.collidepoint(event.pos) and costume_selection_index == 0:
                    costume_selection_index = n_costume_indices - 1
                elif costume_left_button.collidepoint(event.pos) and costume_selection_index > 0:
                    costume_selection_index -= 1
                elif costume_right_button.collidepoint(event.pos) and costume_selection_index < n_costume_indices - 1:
                    costume_selection_index += 1
                elif costume_right_button.collidepoint(event.pos) and costume_selection_index == n_costume_indices - 1:
                    costume_selection_index = 0
                if back_button.collidepoint(event.pos):
                    game_variables['options']['costume'] = costume_indices_reverse[costume_selection_index]
                    game_variables['variables']['player_costume_sprite'] = stt.COSTUMES[
                        costume_indices_reverse[costume_selection_index]
                    ]
                    running = False
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and selected_index == 0:
                    if costume_selection_index == 0:
                        costume_selection_index = n_costume_indices - 1
                    elif costume_selection_index > 0:
                        costume_selection_index -= 1
                if keys[pygame.K_RIGHT] and selected_index == 0:
                    if costume_selection_index < n_costume_indices - 1:
                        costume_selection_index += 1
                    elif costume_selection_index == n_costume_indices - 1:
                        costume_selection_index = 0
                if keys[pygame.K_UP] and selected_index > 0:
                    selected_index -= 1
                if keys[pygame.K_DOWN] and selected_index < n_indices - 1:
                    selected_index += 1
                if (keys[pygame.K_RETURN] and selected_index == 1) or keys[pygame.K_ESCAPE]:
                    game_variables['options']['costume'] = costume_indices_reverse[costume_selection_index]
                    game_variables['variables']['player_costume_sprite'] = stt.COSTUMES[
                        costume_indices_reverse[costume_selection_index]
                    ]
                    running = False
    return game_variables
