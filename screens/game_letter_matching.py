import numpy as np
import pygame

import constants.colors as clr
import constants.dimensions as dms
import constants.fonts as fnt
import functions.audio as aud
import functions.visual as viz
import objects.tilemap as tmp
import screens.menu_end_minigame
import screens.menu_pause
import screens.scene_base as scb

LETTER_CARD_WIDTH = 24
LETTER_CARD_HEIGHT = 48
LETTERS = ["A", "B", "C", "D", "E", "F"]
N_CARDS_PER_ROW = 4
N_ROWS = 3
BUFFER_X = 180
BUFFER_Y = 90
FLIP_BACK_DELAY_MS = 500


def shuffle_pairs(letters, rng=None):
    """Return {card_index: letter} for a randomized pair layout. Kept as a
    pure function, separate from sprite loading, so the shuffle itself is
    unit-testable without pygame."""
    rng = rng if rng is not None else np.random
    n = len(letters)
    positions = rng.choice(a=list(range(2 * n)), size=2 * n, replace=False).tolist()
    layout = {}
    for idx, letter in enumerate(letters):
        layout[positions[2 * idx]] = letter
        layout[positions[2 * idx + 1]] = letter
    return layout


def is_match(letter_a, letter_b):
    return letter_a == letter_b


class LetterMatchingScene(scb.Scene):
    def __init__(self, state):
        super().__init__()
        self.state = state
        aud.play_looping_track(filename="sounds/sample_music_3.mp3")

        self.tile_map = tmp.TileMap(
            width=dms.SCREEN_WIDTH, height=dms.SCREEN_HEIGHT, tile_size=dms.TILE_SIZE,
            wall_color=clr.BLUE, floor_color=clr.WHITE,
        )

        letter_sprites = {
            letter: pygame.image.load(f"sprites/letter_cards/{letter}.png").convert_alpha()
            for letter in LETTERS
        }
        back_sprite = pygame.image.load("sprites/letter_cards/Back.png").convert_alpha()
        layout = shuffle_pairs(LETTERS)
        self.n_cards = len(layout)
        self.cards = {
            index: {
                "letter": letter,
                "visible_sprite": letter_sprites[letter],
                "hidden_sprite": back_sprite,
                "visible": False,
            }
            for index, letter in layout.items()
        }

        self.selected_index = 0
        self.inspected = []
        self.n_selected = 0
        self.n_correct = 0
        self.won = False

    def _card_position(self, index):
        row, col = divmod(index, N_CARDS_PER_ROW)
        x = BUFFER_X + (dms.SCREEN_WIDTH - BUFFER_X) / N_CARDS_PER_ROW * col
        y = BUFFER_Y + (dms.SCREEN_HEIGHT - BUFFER_Y) / N_ROWS * row
        return x, y

    def handle_event(self, event, screen):
        if event.type != pygame.KEYDOWN or self.won:
            return
        if event.key == pygame.K_ESCAPE:
            self.next_scene = screens.menu_pause.PauseMenuScene(resume_scene=self, state=self.state)
        elif event.key == pygame.K_SPACE:
            card = self.cards[self.selected_index]
            if not card["visible"] and self.n_selected < 2:
                card["visible"] = True
                self.inspected.append(self.selected_index)
                self.n_selected += 1
        elif event.key == pygame.K_UP:
            if self.selected_index // N_CARDS_PER_ROW > 0:
                self.selected_index -= N_CARDS_PER_ROW
        elif event.key == pygame.K_DOWN:
            if self.selected_index // N_CARDS_PER_ROW < N_ROWS - 1:
                self.selected_index += N_CARDS_PER_ROW
        elif event.key == pygame.K_RIGHT:
            if self.selected_index % N_CARDS_PER_ROW < N_CARDS_PER_ROW - 1:
                self.selected_index += 1
        elif event.key == pygame.K_LEFT:
            if self.selected_index % N_CARDS_PER_ROW > 0:
                self.selected_index -= 1

    def update(self, dt):
        if self.won:
            return

        if self.n_selected == 2:
            first, second = self.inspected
            if is_match(self.cards[first]["letter"], self.cards[second]["letter"]):
                self.n_correct += 2
            else:
                pygame.time.wait(FLIP_BACK_DELAY_MS)
                self.cards[first]["visible"] = False
                self.cards[second]["visible"] = False
            self.n_selected = 0
            self.inspected = []

        if self.n_correct == self.n_cards:
            self.won = True

    def draw(self, screen):
        self.tile_map.draw(screen)
        for index, card in self.cards.items():
            sprite = card["visible_sprite"] if card["visible"] else card["hidden_sprite"]
            frame = viz.get_frame(
                sheet=sprite, frame_width=LETTER_CARD_WIDTH, frame_height=LETTER_CARD_HEIGHT,
                column=0, row=0, scale_factor=3,
            )
            x, y = self._card_position(index)
            if index == self.selected_index:
                viz.draw_rectangle(
                    screen=screen, x=x - 5, y=y - 5, color=clr.LIGHT_RED,
                    width=3 * LETTER_CARD_WIDTH + 10, height=3 * LETTER_CARD_HEIGHT + 10,
                )
            screen.blit(frame, (x, y))

        if self.won:
            self._celebrate_and_finish(screen)

    def _celebrate_and_finish(self, screen):
        self.tile_map.draw(screen)
        congratulations_text = fnt.font.render("GREAT JOB!", True, clr.DARK_GREEN)
        screen.blit(congratulations_text, (dms.SCREEN_WIDTH / 2 - 150, dms.SCREEN_HEIGHT / 2 - 50))
        pygame.display.flip()
        pygame.time.wait(3000)
        aud.stop_music()
        self.state.save()
        self.next_scene = screens.menu_end_minigame.EndMinigameScene(
            minigame_factory=lambda: LetterMatchingScene(state=self.state), state=self.state,
        )
