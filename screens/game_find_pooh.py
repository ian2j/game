import pygame
import objects.sprite_sheets as sps
import constants.fonts as fnt
import constants.dimensions as dms
import constants.colors as clr
import constants.flags as flg
import constants.settings as stt
import functions.audio as aud
import functions.visual as viz
import screens.menu_pause
import screens.menu_end_minigame
import numpy as np
import sys


def show_game_find_pooh(screen, game_variables):
    # pygame.time.wait(300)
    if not flg.PYGAME_MIXER_INITIALIZED:
        aud.start_mixer()
    aud.load_music(filename="sounds/sample_music_3.mp3")
    aud.play_music_on_loop()

    tile_map = np.zeros(int(dms.SCREEN_HEIGHT / dms.TILE_SIZE) * int(dms.SCREEN_WIDTH / dms.TILE_SIZE)).reshape(
        int(dms.SCREEN_HEIGHT / dms.TILE_SIZE),
        int(dms.SCREEN_WIDTH / dms.TILE_SIZE)
    )
    tile_map[:, :2] = 1
    tile_map[:, -2:] = 1
    tile_map[:2, :] = 1
    tile_map[-2:, :] = 1

    def draw_tile_map():
        for row in range(len(tile_map)):
            for col in range(len(tile_map[row])):
                tile = tile_map[row][col]
                x = col * dms.TILE_SIZE
                y = row * dms.TILE_SIZE
                if tile == 1:  # Wall
                    pygame.draw.rect(screen, clr.DARK_GREEN, rect=(x, y, dms.TILE_SIZE, dms.TILE_SIZE))
                elif tile == 0:  # Floor
                    pygame.draw.rect(screen, clr.LIGHT_GREY, rect=(x, y, dms.TILE_SIZE, dms.TILE_SIZE))

    # Pooh
    POOH_WIDTH = 60
    POOH_HEIGHT = 100
    POOH = {
        'visible': True,
        'box': -1,
        'sprite_sheet': sps.SpriteSheet()
    }
    POOH['sprite_sheet'].set_sprite_sheet(sprite_sheet='sprites/characters/pooh.png')
    POOH['sprite_sheet'].set_frame_width(frame_width=POOH_WIDTH)
    POOH['sprite_sheet'].set_frame_height(frame_height=POOH_HEIGHT)
    POOH['sprite_sheet'].set_scale(scale=1.5)
    POOH_frame = viz.get_frame(
        sheet=POOH['sprite_sheet'].sprite_sheet,
        frame_width=POOH['sprite_sheet'].frame_width,
        frame_height=POOH['sprite_sheet'].frame_height,
        row=0,
        column=0,
        scale_factor=POOH['sprite_sheet'].scale
    )
    POOH_position = (dms.SCREEN_WIDTH/2-POOH_WIDTH/2*POOH['sprite_sheet'].scale, 80)
    POOH['sprite_sheet'].set_position(position=POOH_position)

    # Green circle
    GREEN_CIRCLE_WIDTH = 90
    GREEN_CIRCLE_HEIGHT = 90
    GREEN_CIRCLE = {
        'visible': False,
        'sprite_sheet': sps.SpriteSheet()
    }
    GREEN_CIRCLE['sprite_sheet'].set_sprite_sheet(sprite_sheet='sprites/shapes/circle_green.png')
    GREEN_CIRCLE['sprite_sheet'].set_frame_width(frame_width=GREEN_CIRCLE_WIDTH)
    GREEN_CIRCLE['sprite_sheet'].set_frame_height(frame_height=GREEN_CIRCLE_HEIGHT)
    GREEN_CIRCLE['sprite_sheet'].set_scale(scale=1)
    GREEN_CIRCLE_frame = viz.get_frame(
        sheet=GREEN_CIRCLE['sprite_sheet'].sprite_sheet,
        frame_width=GREEN_CIRCLE['sprite_sheet'].frame_width,
        frame_height=GREEN_CIRCLE['sprite_sheet'].frame_height,
        row=0,
        column=0,
        scale_factor=GREEN_CIRCLE['sprite_sheet'].scale
    )
    GREEN_CIRCLE_position = (dms.SCREEN_WIDTH / 2 - GREEN_CIRCLE_WIDTH / 2 * GREEN_CIRCLE['sprite_sheet'].scale, 500)
    GREEN_CIRCLE['sprite_sheet'].set_position(position=GREEN_CIRCLE_position)

    # Red X
    RED_X_WIDTH = 90
    RED_X_HEIGHT = 90
    RED_X = {
        'visible': False,
        'sprite_sheet': sps.SpriteSheet()
    }
    RED_X['sprite_sheet'].set_sprite_sheet(sprite_sheet='sprites/shapes/x_mark_red.png')
    RED_X['sprite_sheet'].set_frame_width(frame_width=RED_X_WIDTH)
    RED_X['sprite_sheet'].set_frame_height(frame_height=RED_X_HEIGHT)
    RED_X['sprite_sheet'].set_scale(scale=1)
    RED_X_frame = viz.get_frame(
        sheet=RED_X['sprite_sheet'].sprite_sheet,
        frame_width=RED_X['sprite_sheet'].frame_width,
        frame_height=RED_X['sprite_sheet'].frame_height,
        row=0,
        column=0,
        scale_factor=RED_X['sprite_sheet'].scale
    )
    RED_X_position = (dms.SCREEN_WIDTH / 2 - RED_X_WIDTH / 2 * RED_X['sprite_sheet'].scale, 550)
    RED_X['sprite_sheet'].set_position(position=RED_X_position)

    # Black arrow
    BLACK_ARROW_WIDTH = 90
    BLACK_ARROW_HEIGHT = 150
    BLACK_ARROW = {
        'visible': False,
        'box': 0,
        'sprite_sheet': sps.SpriteSheet()
    }
    BLACK_ARROW['sprite_sheet'].set_sprite_sheet(sprite_sheet='sprites/shapes/up_arrow_black.png')
    BLACK_ARROW['sprite_sheet'].set_frame_width(frame_width=BLACK_ARROW_WIDTH)
    BLACK_ARROW['sprite_sheet'].set_frame_height(frame_height=BLACK_ARROW_HEIGHT)
    BLACK_ARROW['sprite_sheet'].set_scale(scale=1)
    BLACK_ARROW_frame = viz.get_frame(
        sheet=BLACK_ARROW['sprite_sheet'].sprite_sheet,
        frame_width=BLACK_ARROW['sprite_sheet'].frame_width,
        frame_height=BLACK_ARROW['sprite_sheet'].frame_height,
        row=0,
        column=0,
        scale_factor=BLACK_ARROW['sprite_sheet'].scale
    )
    BLACK_ARROW_position = (dms.SCREEN_WIDTH / 2 - BLACK_ARROW_WIDTH / 2 * BLACK_ARROW['sprite_sheet'].scale, 550)
    BLACK_ARROW['sprite_sheet'].set_position(position=BLACK_ARROW_position)

    N_BOXES = 3
    BOX_WIDTH = 90
    BOX_HEIGHT = 150
    BOXES = {}
    BOX_SPACING = 200
    for i in range(N_BOXES):
        BOXES[i] = {
            'position_x': dms.SCREEN_WIDTH/2-POOH_WIDTH/2*POOH['sprite_sheet'].scale+BOX_SPACING*(i-(N_BOXES-1)/2),
            'position_y': 325,
        }

    def draw_green_circle():
        if GREEN_CIRCLE['visible'] and POOH['box'] > -1:
            box = BLACK_ARROW['box']
            box_x = BOXES[box]['position_x']
            GREEN_CIRCLE_position = (box_x, 500)
            GREEN_CIRCLE['sprite_sheet'].set_position(position=GREEN_CIRCLE_position)
            screen.blit(GREEN_CIRCLE_frame, GREEN_CIRCLE_position)
        return None

    def draw_red_x():
        if RED_X['visible'] and POOH['box'] > -1:
            box = BLACK_ARROW['box']
            box_x = BOXES[box]['position_x']
            RED_X_position = (box_x, 500)
            RED_X['sprite_sheet'].set_position(position=RED_X_position)
            screen.blit(RED_X_frame, RED_X_position)
        return None

    def draw_black_arrow():
        if BLACK_ARROW['visible']:
            box = BLACK_ARROW['box']
            box_x = BOXES[box]['position_x']
            BLACK_ARROW_position = (box_x, 500)
            BLACK_ARROW['sprite_sheet'].set_position(position=BLACK_ARROW_position)
            screen.blit(BLACK_ARROW_frame, BLACK_ARROW_position)
        return None

    def move_black_arrow(direction):
        BOX_X_POSITIONS = [(box, BOXES[box]['position_x']) for box in BOXES]
        BOX_X_POSITIONS = sorted(BOX_X_POSITIONS, key=lambda x: x[1])
        ORDER = {box: index for index, box in enumerate([x[0] for x in BOX_X_POSITIONS])}
        ORDER_LOOKUP = {index: box for index, box in enumerate([x[0] for x in BOX_X_POSITIONS])}

        if BLACK_ARROW['visible']:
            if direction == 'left' and ORDER[BLACK_ARROW['box']] == 0:
                BLACK_ARROW['box'] = ORDER_LOOKUP[N_BOXES - 1]
            elif direction == 'left' and ORDER[BLACK_ARROW['box']] > 0:
                BLACK_ARROW['box'] = ORDER_LOOKUP[ORDER[BLACK_ARROW['box']]-1]
            elif direction == 'right' and ORDER[BLACK_ARROW['box']] < N_BOXES - 1:
                BLACK_ARROW['box'] = ORDER_LOOKUP[ORDER[BLACK_ARROW['box']]+1]
            elif direction == 'right' and ORDER[BLACK_ARROW['box']] == N_BOXES - 1:
                BLACK_ARROW['box'] = ORDER_LOOKUP[0]
            else:
                pass
        return None

    def draw_boxes():
        for box in BOXES:
            viz.draw_rectangle(
                screen=screen,
                x=BOXES[box]['position_x'],
                y=BOXES[box]['position_y'],
                color=clr.NAVY,
                width=BOX_WIDTH,
                height=BOX_HEIGHT
            )
            viz.draw_rectangle(
                screen=screen,
                x=BOXES[box]['position_x']-5,
                y=BOXES[box]['position_y'],
                color=clr.BLACK,
                width=BOX_WIDTH+10,
                height=10
            )
        return None

    def move_pooh_into_box(box=None):
        if POOH['visible']:
            if not box:
                choice = np.random.choice(a=N_BOXES, size=1, replace=False).tolist()[0]
                BOX_X_POSITIONS = [(box, BOXES[box]['position_x']) for box in BOXES]
                BOX_X_POSITIONS = sorted(BOX_X_POSITIONS, key=lambda x: x[1])
                ORDER_LOOKUP = {index: box for index, box in enumerate([x[0] for x in BOX_X_POSITIONS])}
                box = ORDER_LOOKUP[choice]
            POOH['box'] = box
            POOH_position = POOH['sprite_sheet'].get_position()
            pooh_x = POOH_position[0]
            pooh_y = POOH_position[1]
            box_x = BOXES[box]['position_x']
            box_y = BOXES[box]['position_y']
            while np.abs(pooh_x - box_x) > 2:
                pooh_x = POOH_position[0]
                pooh_y = POOH_position[1]
                POOH['sprite_sheet'].set_position(position=(pooh_x + (box_x - pooh_x) / 10, pooh_y))
                POOH_position = POOH['sprite_sheet'].get_position()
                screen.fill(clr.WHITE)
                draw_tile_map()
                screen.blit(POOH_frame, POOH_position)
                draw_boxes()
                pygame.display.flip()
                clock.tick(30)
            while np.abs(pooh_y - box_y) > 5:
                pooh_x = POOH_position[0]
                pooh_y = POOH_position[1]
                POOH['sprite_sheet'].set_position(position=(pooh_x, pooh_y + (box_y - pooh_y) / 10))
                screen.fill(clr.WHITE)
                draw_tile_map()
                POOH_position = POOH['sprite_sheet'].get_position()
                screen.blit(POOH_frame, POOH_position)
                draw_boxes()
                pygame.display.flip()
                clock.tick(30)
            # Make Pooh invisible
            POOH['visible'] = False
            # Make black arrow visible
            BLACK_ARROW['visible'] = True
        return None

    def move_pooh_outside_box():
        if POOH['box'] > -1:
            box = POOH['box']
            if not POOH['visible']:
                POOH['visible'] = True
                BLACK_ARROW['visible'] = False
                if BLACK_ARROW['box'] == box:
                    GREEN_CIRCLE['visible'] = True
                else:
                    RED_X['visible'] = True
                final_POOH_position = (dms.SCREEN_WIDTH/2-POOH_WIDTH/2*POOH['sprite_sheet'].scale, 80)
                final_POOH_position_x = final_POOH_position[0]
                final_POOH_position_y = final_POOH_position[1]
                box_x = BOXES[box]['position_x']
                box_y = BOXES[box]['position_y']
                POOH_position = (box_x, box_y)
                POOH['sprite_sheet'].set_position(position=POOH_position)
                pooh_x = box_x
                pooh_y = box_y
                while np.abs(pooh_y - final_POOH_position_y) > 5:
                    pooh_x = POOH_position[0]
                    pooh_y = POOH_position[1]
                    POOH['sprite_sheet'].set_position(position=(pooh_x, pooh_y + (final_POOH_position_y - pooh_y) / 10))
                    screen.fill(clr.WHITE)
                    draw_tile_map()
                    POOH_position = POOH['sprite_sheet'].get_position()
                    screen.blit(POOH_frame, POOH_position)
                    draw_boxes()
                    draw_green_circle()
                    draw_red_x()
                    draw_black_arrow()
                    pygame.display.flip()
                    clock.tick(30)
                while np.abs(pooh_x - final_POOH_position_x) > 2:
                    pooh_x = POOH_position[0]
                    pooh_y = POOH_position[1]
                    POOH['sprite_sheet'].set_position(position=(pooh_x + (final_POOH_position_x - pooh_x) / 10, pooh_y))
                    POOH_position = POOH['sprite_sheet'].get_position()
                    screen.fill(clr.WHITE)
                    draw_tile_map()
                    screen.blit(POOH_frame, POOH_position)
                    draw_boxes()
                    draw_green_circle()
                    draw_red_x()
                    draw_black_arrow()
                    pygame.display.flip()
                    clock.tick(30)
                GREEN_CIRCLE['visible'] = False
                RED_X['visible'] = False
                BLACK_ARROW['visible'] = False
            return None

    def shuffle_boxes():
        if not POOH['visible']:
            n_shuffles = np.random.choice(a=[5, 10, 15], size=1, replace=False).tolist()[0]
            for _ in range(n_shuffles):
                boxes_to_shuffle = np.random.choice(a=list(BOXES), size=2, replace=False).tolist()
                initial_box_1_x = BOXES[boxes_to_shuffle[0]]['position_x']
                initial_box_1_y = BOXES[boxes_to_shuffle[0]]['position_y']
                initial_box_2_x = BOXES[boxes_to_shuffle[1]]['position_x']
                initial_box_2_y = BOXES[boxes_to_shuffle[1]]['position_y']
                box_1_y_movement = np.random.choice(a=['up', 'down'], size=1, replace=False).tolist()[0]
                speed = np.random.choice(a=[30, 60, 90], size=1, replace=False).tolist()[0]
                thetas_up_counterclockwise = np.linspace(start=0, stop=np.pi, num=speed)
                thetas_down_counterclockwise = np.linspace(start=np.pi, stop=2 * np.pi, num=speed)
                thetas_up_clockwise = np.linspace(start=np.pi, stop=0, num=speed)
                thetas_down_clockwise = np.linspace(start=2*np.pi, stop=np.pi, num=speed)
                center_x = 0.5 * (initial_box_1_x + initial_box_2_x)
                center_y = 0.5 * (initial_box_1_y + initial_box_2_y)
                radius = 0.5 * np.abs(initial_box_1_x - initial_box_2_x)
                if initial_box_1_x < initial_box_2_x:
                    if box_1_y_movement == 'up':
                        # Box 1 --- Box 2
                        # Box 1 ^, Box 2 v
                        # (Box 1 moves clockwise, Box 2 moves clockwise)
                        new_box_1_xs = radius * np.cos(thetas_up_clockwise) + center_x
                        new_box_1_ys = radius * np.sin(thetas_up_clockwise) + center_y
                        new_box_2_xs = radius * np.cos(thetas_down_clockwise) + center_x
                        new_box_2_ys = radius * np.sin(thetas_down_clockwise) + center_y
                    else:
                        # Box 1 --- Box 2
                        # Box 1 v, Box 2 ^
                        # (Box 1 moves counterclockwise, Box 2 moves counterclockwise)
                        new_box_1_xs = radius * np.cos(thetas_down_counterclockwise) + center_x
                        new_box_1_ys = radius * np.sin(thetas_down_counterclockwise) + center_y
                        new_box_2_xs = radius * np.cos(thetas_up_counterclockwise) + center_x
                        new_box_2_ys = radius * np.sin(thetas_up_counterclockwise) + center_y
                else:
                    if box_1_y_movement == 'up':
                        # Box 2 --- Box 1
                        # Box 2 v, Box 1 ^
                        # (Box 1 moves counterclockwise, Box 2 moves counterclockwise)
                        new_box_1_xs = radius * np.cos(thetas_up_counterclockwise) + center_x
                        new_box_1_ys = radius * np.sin(thetas_up_counterclockwise) + center_y
                        new_box_2_xs = radius * np.cos(thetas_down_counterclockwise) + center_x
                        new_box_2_ys = radius * np.sin(thetas_down_counterclockwise) + center_y
                    else:
                        # Box 2 --- Box 1
                        # Box 2 ^, Box 1 v
                        # (Box 1 moves clockwise, Box 2 moves clockwise)
                        new_box_1_xs = radius * np.cos(thetas_down_clockwise) + center_x
                        new_box_1_ys = radius * np.sin(thetas_down_clockwise) + center_y
                        new_box_2_xs = radius * np.cos(thetas_up_clockwise) + center_x
                        new_box_2_ys = radius * np.sin(thetas_up_clockwise) + center_y
                for b1x, b1y, b2x, b2y in zip(new_box_1_xs, new_box_1_ys, new_box_2_xs, new_box_2_ys):
                    BOXES[boxes_to_shuffle[0]]['position_x'] = b1x
                    BOXES[boxes_to_shuffle[0]]['position_y'] = b1y
                    BOXES[boxes_to_shuffle[1]]['position_x'] = b2x
                    BOXES[boxes_to_shuffle[1]]['position_y'] = b2y
                    screen.fill(clr.WHITE)
                    draw_tile_map()
                    draw_boxes()
                    pygame.display.flip()
                    clock.tick(60)
            BOX_X_POSITIONS = [(box, BOXES[box]['position_x']) for box in BOXES]
            BOX_X_POSITIONS = sorted(BOX_X_POSITIONS, key=lambda x: x[1])
            ORDER_LOOKUP = {index: box for index, box in enumerate([x[0] for x in BOX_X_POSITIONS])}
            box = ORDER_LOOKUP[0]
            BLACK_ARROW['box'] = box
        return None

    clock = pygame.time.Clock()

    screen.fill(clr.WHITE)
    draw_tile_map()
    if POOH['visible']:
        screen.blit(POOH_frame, POOH['sprite_sheet'].get_position())
    draw_boxes()
    draw_green_circle()

    running = True

    # POOH_box = np.random.choice(a=[0, 1, 2], size=1, replace=False).tolist()[0]
    POOH_box = None

    show_instructions = True

    def draw_instructions():
        if show_instructions:
            instructions = fnt.font.render("Press Space to Begin", True, clr.BLACK)
            screen.blit(instructions, (dms.SCREEN_WIDTH/2-len("Press Space to Begin")*13, 600))
        return None

    while running:

        screen.fill(clr.WHITE)
        draw_tile_map()
        if POOH['visible']:
            screen.blit(POOH_frame, POOH['sprite_sheet'].get_position())
        draw_boxes()
        draw_green_circle()
        draw_red_x()
        draw_black_arrow()
        draw_instructions()

        # Update the screen
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Get key states
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    screens.menu_pause.show_pause_menu(screen=screen, game_variables=game_variables)
                elif keys[pygame.K_SPACE]:
                    if show_instructions:
                        show_instructions = False
                    if POOH['visible']:
                        move_pooh_into_box(box=POOH_box)
                        shuffle_boxes()
                    else:
                        move_pooh_outside_box()
                elif keys[pygame.K_LEFT]:
                    move_black_arrow(direction='left')
                elif keys[pygame.K_RIGHT]:
                    move_black_arrow(direction='right')
                # elif keys[pygame.K_s]:
                #     shuffle_boxes()
                # elif keys[pygame.K_d]:
                #     move_pooh_outside_box()
                else:
                    pass

        # Update the display
        screen.fill(clr.WHITE)
        draw_tile_map()
        if POOH['visible']:
            screen.blit(POOH_frame, POOH['sprite_sheet'].get_position())
        draw_boxes()
        draw_green_circle()
        draw_red_x()
        draw_black_arrow()
        draw_instructions()
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(stt.FRAMES_PER_SECOND)

    screen.fill(clr.WHITE)
    draw_tile_map()
    congratulations_text = fnt.font.render('GREAT JOB!', True, clr.DARK_GREEN)
    screen.blit(congratulations_text, (dms.SCREEN_WIDTH/2-150, dms.SCREEN_HEIGHT/2-50))
    pygame.display.flip()
    pygame.time.wait(3000)
    aud.stop_music()
    screens.menu_end_minigame.show_end_minigame_menu(
        screen=screen,
        game_variables=game_variables,
        game_screen=show_game_find_pooh
    )
