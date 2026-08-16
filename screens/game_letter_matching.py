import pygame
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


def show_game_letter_matching(screen, game_variables):
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
                    pygame.draw.rect(screen, clr.BLUE, rect=(x, y, dms.TILE_SIZE, dms.TILE_SIZE))
                elif tile == 0:  # Floor
                    pygame.draw.rect(screen, clr.WHITE, rect=(x, y, dms.TILE_SIZE, dms.TILE_SIZE))

    LETTER_CARD_WIDTH = 24
    LETTER_CARD_HEIGHT = 48
    LETTERS = {
        'A': pygame.image.load('sprites/letter_cards/A.png').convert_alpha(),
        'B': pygame.image.load('sprites/letter_cards/B.png').convert_alpha(),
        'C': pygame.image.load('sprites/letter_cards/C.png').convert_alpha(),
        'D': pygame.image.load('sprites/letter_cards/D.png').convert_alpha(),
        'E': pygame.image.load('sprites/letter_cards/E.png').convert_alpha(),
        'F': pygame.image.load('sprites/letter_cards/F.png').convert_alpha(),
    }
    N_LETTERS = len(LETTERS)
    N_CARDS = 2 * N_LETTERS
    N_CARDS_PER_ROW = 4
    N_ROWS = 3
    BUFFER_X = 180
    BUFFER_Y = 90

    SHUFFLE = np.random.choice(a=[_ for _ in range(N_CARDS)], size=N_CARDS, replace=False).tolist()
    CARDS = {}
    for idx, letter in enumerate(LETTERS):
        CARDS[SHUFFLE[2*idx]] = {
            'Letter': letter,
            'Visible Sprite': LETTERS[letter],
            'Not Visible Sprite': pygame.image.load('sprites/letter_cards/Back.png').convert_alpha(),
            'Visible': False
        }
        CARDS[SHUFFLE[2*idx+1]] = {
            'Letter': letter,
            'Visible Sprite': LETTERS[letter],
            'Not Visible Sprite': pygame.image.load('sprites/letter_cards/Back.png').convert_alpha(),
            'Visible': False
        }

    def draw_cards(selected_index=0):
        card_index = 0
        for row in range(N_ROWS):
            for col in range(N_CARDS_PER_ROW):
                card = CARDS[card_index]
                card_viz = viz.get_frame(
                    sheet=card['Visible Sprite'] if card['Visible'] else card['Not Visible Sprite'],
                    frame_width=LETTER_CARD_WIDTH,
                    frame_height=LETTER_CARD_HEIGHT,
                    column=0,
                    row=0,
                    scale_factor=3
                )
                card_position_x = BUFFER_X + (dms.SCREEN_WIDTH - 1 * BUFFER_X) / N_CARDS_PER_ROW * col
                card_position_y = BUFFER_Y + (dms.SCREEN_HEIGHT - 1 * BUFFER_Y) / N_ROWS * row
                card_position = (card_position_x, card_position_y)
                if card_index == selected_index:
                    viz.draw_rectangle(
                        screen=screen,
                        x=card_position_x-5,
                        y=card_position_y-5,
                        color=clr.LIGHT_RED,
                        width=3 * LETTER_CARD_WIDTH+10,
                        height=3 * LETTER_CARD_HEIGHT+10
                    )
                screen.blit(card_viz, card_position)
                card_index += 1
        return None


    clock = pygame.time.Clock()

    screen.fill(clr.WHITE)
    draw_tile_map()
    draw_cards()

    running = True

    N_SELECTED = 0
    SELECTED_INDEX = 0
    INSPECTED = []
    N_CORRECT = 0

    while running:

        screen.fill(clr.WHITE)
        draw_tile_map()
        draw_cards(selected_index=SELECTED_INDEX)

        # Update the screen
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Get key states
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    if not CARDS[SELECTED_INDEX]['Visible'] and N_SELECTED < 2:
                        CARDS[SELECTED_INDEX]['Visible'] = True
                        INSPECTED.append(SELECTED_INDEX)
                        N_SELECTED += 1
                elif keys[pygame.K_UP]:
                    row = int(SELECTED_INDEX / N_CARDS_PER_ROW)
                    if row - 1 >= 0:
                        SELECTED_INDEX -= N_CARDS_PER_ROW
                elif keys[pygame.K_DOWN]:
                    row = int(SELECTED_INDEX / N_CARDS_PER_ROW)
                    if row + 1 < N_ROWS:
                        SELECTED_INDEX += N_CARDS_PER_ROW
                elif keys[pygame.K_RIGHT]:
                    if SELECTED_INDEX % N_CARDS_PER_ROW < N_CARDS_PER_ROW - 1:
                        SELECTED_INDEX += 1
                elif keys[pygame.K_LEFT]:
                    if SELECTED_INDEX % N_CARDS_PER_ROW > 0:
                        SELECTED_INDEX -= 1
                elif keys[pygame.K_ESCAPE]:
                    screens.menu_pause.show_pause_menu(screen=screen, game_variables=game_variables)
                else:
                    pass

        # Update the display
        screen.fill(clr.WHITE)
        draw_tile_map()
        draw_cards(selected_index=SELECTED_INDEX)
        pygame.display.flip()

        if N_SELECTED == 2:
            if CARDS[INSPECTED[0]]['Letter'] == CARDS[INSPECTED[1]]['Letter']:
                N_CORRECT += 2
                N_SELECTED = 0
                INSPECTED = []
            else:
                pygame.time.wait(500)
                CARDS[INSPECTED[0]]['Visible'] = False
                CARDS[INSPECTED[1]]['Visible'] = False
                N_SELECTED = 0
                INSPECTED = []

        if N_CORRECT == N_CARDS:
            running = False

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
        game_screen=show_game_letter_matching
    )
