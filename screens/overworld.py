import pygame
import objects.characters as crs
import objects.sprite_sheets as sps
import constants.dimensions as dms
import constants.colors as clr
import constants.flags as flg
import constants.fonts as fnt
import constants.settings as stt
import functions.audio as aud
import functions.visual as viz
import screens.menu_pause
import screens.game_letter_matching
import screens.game_find_pooh
import numpy as np
import sys


def show_overworld(screen, game_variables):
    # pygame.time.wait(300)
    if not flg.PYGAME_MIXER_INITIALIZED:
        aud.start_mixer()
    aud.load_music(filename="sounds/sample_music_2.mp3")
    aud.play_music_on_loop()

    player = crs.Player()
    player.set_sprite_sheet(sprite_sheet=game_variables['variables']['player_costume_sprite'])
    player.set_frame_width(frame_width=21)
    player.set_frame_height(frame_height=22)
    player.set_scale(scale=6)
    player.set_position(game_variables['variables']['player_position'])
    current_direction = game_variables['variables']['player_direction']
    frame_index = 0  # Current animation frame

    tile_map = np.zeros(int(dms.SCREEN_HEIGHT / dms.TILE_SIZE) * int(dms.SCREEN_WIDTH / dms.TILE_SIZE)).reshape(
        int(dms.SCREEN_HEIGHT / dms.TILE_SIZE),
        int(dms.SCREEN_WIDTH / dms.TILE_SIZE)
    )
    tile_map[:, :2] = 1
    tile_map[:, -2:] = 1
    tile_map[:2, :] = 1
    tile_map[-2:, :] = 1

    # Testing an idea
    tile_map[10:20, 10:20] = 1
    tile_map[10:20, -20:-11] = 1

    def draw_tile_map():
        for row in range(len(tile_map)):
            for col in range(len(tile_map[row])):
                tile = tile_map[row][col]
                x = col * dms.TILE_SIZE
                y = row * dms.TILE_SIZE
                if tile == 1:  # Wall
                    pygame.draw.rect(screen, clr.GREY, rect=(x, y, dms.TILE_SIZE, dms.TILE_SIZE))
                elif tile == 0:  # Floor
                    pygame.draw.rect(screen, clr.WHITE, rect=(x, y, dms.TILE_SIZE, dms.TILE_SIZE))

    def can_move(new_x, new_y):
        grid_x_left = int(new_x / dms.TILE_SIZE)
        grid_x_right = int((new_x + player.frame_width / 2 * player.scale * 2) / dms.TILE_SIZE)
        grid_y_up = int(new_y / dms.TILE_SIZE)
        grid_y_down = int((new_y + player.frame_height / 2 * player.scale * 2) / dms.TILE_SIZE)
        checksum = (
                tile_map[grid_y_up][grid_x_left] +
                tile_map[grid_y_up][grid_x_right] +
                tile_map[grid_y_down][grid_x_left] +
                tile_map[grid_y_down][grid_x_right]
        )
        if checksum > 0:
            return False
        return True

    # Create a dictionary for animations
    animations = {
        "down": [
            viz.get_frame(
                sheet=player.sprite_sheet,
                frame_width=player.frame_width,
                frame_height=player.frame_height,
                column=0,
                row=row,
                scale_factor=player.scale
            ) for row in range(4)
        ],
        "up": [
            viz.get_frame(
                sheet=player.sprite_sheet,
                frame_width=player.frame_width,
                frame_height=player.frame_height,
                column=1,
                row=row,
                scale_factor=player.scale
            ) for row in range(4)
        ],
        "left": [
            viz.get_frame(
                sheet=player.sprite_sheet,
                frame_width=player.frame_width,
                frame_height=player.frame_height,
                column=2,
                row=row,
                scale_factor=player.scale
            ) for row in range(4)
        ],
        "right": [
            viz.get_frame(
                sheet=player.sprite_sheet,
                frame_width=player.frame_width,
                frame_height=player.frame_height,
                column=3,
                row=row,
                scale_factor=player.scale
            ) for row in range(4)
        ],
    }

    clock = pygame.time.Clock()

    screen.fill(clr.WHITE)
    draw_tile_map()

    # Animation timing (milliseconds per frame)
    ANIMATION_SPEED = 100  # 100ms per frame = 10 frames per second

    # Initialize variables for time-based animation
    last_update_time = pygame.time.get_ticks()

    # Initialize mini-games
    MINIGAMES = {
        'Letter Matching': {
            'sprite_unselected': 'sprites/minigame_icons/letter_matching.png',
            'sprite_selected': 'sprites/minigame_icons/letter_matching_selected.png',
            'position_x': 200,
            'position_y': 200,
            'selected': False,
            'game_screen': screens.game_letter_matching.show_game_letter_matching
        },
        '    Find Pooh': {
            'sprite_unselected': 'sprites/minigame_icons/find_pooh.png',
            'sprite_selected': 'sprites/minigame_icons/find_pooh_selected.png',
            'position_x': 880,
            'position_y': 200,
            'selected': False,
            'game_screen': screens.game_find_pooh.show_game_find_pooh
        }
    }

    def draw_minigames(player_position):
        player_x = player_position[0]
        player_y = player_position[1]
        for minigame in MINIGAMES:
            center_x = MINIGAMES[minigame]['position_x']
            center_y = MINIGAMES[minigame]['position_y']
            close_x = True if np.abs(player_x - center_x) < 250 else False
            close_y = True if np.abs(player_y - center_y) < 250 else False
            if close_x and close_y:
                MINIGAMES[minigame]['selected'] = True
            else:
                MINIGAMES[minigame]['selected'] = False
            minigame_object = sps.SpriteSheet()
            sprite_sheet = MINIGAMES[minigame]['sprite_selected'] if MINIGAMES[minigame]['selected'] \
                else MINIGAMES[minigame]['sprite_unselected']
            minigame_object.set_sprite_sheet(sprite_sheet=sprite_sheet)
            minigame_object.set_frame_width(frame_width=200)
            minigame_object.set_frame_height(frame_height=200)
            minigame_object.set_scale(scale=1)
            minigame_frame = viz.get_frame(
                sheet=minigame_object.sprite_sheet,
                frame_width=minigame_object.frame_width,
                frame_height=minigame_object.frame_height,
                row=0,
                column=0,
                scale_factor=minigame_object.scale
            )
            minigame_position = (MINIGAMES[minigame]['position_x'], MINIGAMES[minigame]['position_y'])
            screen.blit(minigame_frame, minigame_position)
            minigame_title = fnt.small_font.render(
                minigame, True, clr.BLUE if MINIGAMES[minigame]['selected'] else clr.BLACK
            )
            title_position = (MINIGAMES[minigame]['position_x']+10, MINIGAMES[minigame]['position_y']-30)
            close_x = True if np.abs(player_x - title_position[0]) < 50 else False
            close_y = True if np.abs(player_y - title_position[1]) < 50 else False
            if not (close_x and close_y):
                screen.blit(minigame_title, title_position)

    running = True

    while running:

        player_position = player.get_position()
        player_x = player_position[0]
        player_y = player_position[1]

        draw_minigames(player_position=player_position)

        # Update the screen
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Get key states
        keys = pygame.key.get_pressed()

        # Update direction and position
        moving = False  # Track if the player is moving this frame
        new_x, new_y = player_x, player_y
        if keys[pygame.K_UP]:
            current_direction = "up"
            new_y -= 5
            moving = True
        elif keys[pygame.K_DOWN]:
            current_direction = "down"
            new_y += 5
            moving = True
        elif keys[pygame.K_LEFT]:
            current_direction = "left"
            new_x -= 5
            moving = True
        elif keys[pygame.K_RIGHT]:
            current_direction = "right"
            new_x += 5
            moving = True
        elif keys[pygame.K_ESCAPE]:
            screens.menu_pause.show_pause_menu(screen=screen, game_variables=game_variables)
            pygame.time.wait(100)
        elif keys[pygame.K_SPACE]:
            for minigame in MINIGAMES:
                if MINIGAMES[minigame]['selected']:
                    MINIGAMES[minigame]['game_screen'](screen=screen, game_variables=game_variables)
        else:
            pass

        if can_move(new_x=new_x, new_y=player_y):
            player_x = new_x
        if can_move(new_x=player_x, new_y=new_y):
            player_y = new_y

        player.set_position((player_x, player_y))
        game_variables['variables']['player_position'] = (player_x, player_y)
        game_variables['variables']['player_direction'] = current_direction
        player_position = player.get_position()

        # Update state based on movement
        if moving:
            current_state = "moving"
        else:
            current_state = "idle"

        # Get the current time
        current_time = pygame.time.get_ticks()

        # Update animation frame only if moving
        if current_state == "moving" and current_time - last_update_time > ANIMATION_SPEED:
            last_update_time = current_time
            frame_index = (frame_index + 1) % len(animations[current_direction])
        elif current_state == "idle":
            # Reset to the idle frame for the current direction
            frame_index = 0

        screen.fill(clr.WHITE)
        draw_tile_map()
        draw_minigames(player_position=player_position)

        # Draw the current frame
        current_frame = animations[current_direction][frame_index]
        screen.blit(current_frame, player_position)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(stt.FRAMES_PER_SECOND)
